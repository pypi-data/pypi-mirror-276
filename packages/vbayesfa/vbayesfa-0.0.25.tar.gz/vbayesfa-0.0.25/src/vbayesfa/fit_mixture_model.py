import numpy as np
import pandas as pd
import functools
import multiprocessing
from time import perf_counter
from .lpa import lpa_model
from scipy.cluster.vq import kmeans2

def fit_mixture_model(x,
                      model_class = lpa_model,
                      n_workers = 4,
                      kmeans = False,
                      restarts = 20, 
                      T = 20,
                      seed = 1234, 
                      tolerance = 1e-05, 
                      max_iter = 1000, 
                      min_iter = 10,
                      **prior_hpar):
    """
    Fit a mixture model using mean field variational Bayes.
    
    Parameters
    ----------
    x: data frame or array
        Observed data (data frame or matrix).  If a matrix then rows are variables and columns
        are observations; if a data frame then rows are observations and columns are variables.
    model_class: class, optional
        Class of mixture model to fit.
    n_workers: int, optional
        Number of workers in the pool for parallel processing; should be less than
        or equal to the number of available CPUs.
    kmeans: logical, optional
        Should the k-means++ algorithm be used for initial starting points?
        If so, then k-means clusterings of different sizes are produced and used.
    restarts: int, optional
        Number of random restarts.
    T: integer, optional
        Truncation level of the variational approximation.
    seed: int, optional
        Random seed (determines starting conditions of each optimization).
    tolerance: float, optional
        Relative change in the ELBO at which the optimization should stop.
    max_iter: integer, optional
        Maximum number of iterations to run the optimization.
    min_iter: integer, optional
        Minimum number of iterations to run the optimization.
    prior_hpar:
        Prior hyperparameters (specified with keywords).
        
    Notes
    -----
    One fits a statistical model using variational Bayes by maximizing a quantity called
    the ELBO (evidence lower bound). The best variational Bayes approximation of the true
    model posterior distribution is the one with the highest ELBO. The algorithm for maximizing
    the ELBO unfortunately only finds local maxima, so to have a decent chance of finding the
    global maximum (truly best approximation to the real model posterior distribution) we need
    different starting points of the variational model hyperparameters. This function provides two
    ways to choose starting points. First, the k-means++ algorithm (a simple clustering algorithm)
    can be used to produce initial clustering of participants. Second, participants can be randomly
    assigned (in a 'soft' way) to different mixture components/latent classes/latent profiles. These
    two methods are not exclusive: both types of starting point will be used if 'kmeans' is set to
    True and 'restarts' > 0. The function creates a separate mixture model object with each starting
    point and fits them using parallel processing for speed.
    
    Output
    ------
    A dictionary with the following:
    
    final_elbo: list
        Final ELBO (evidence lower bound) values of each model.
    model_list: list
        Fitted model objects.
    best_model: mixture_model object
        Best fitted model (i.e. the one with the highest ELBO).
    fit_time: float
        Total time used to fit.
    """
    tic = perf_counter()

    model_list = []
    final_elbo = []
    
    # run using starting points initialized with k-means
    if kmeans:
        if isinstance(x, pd.DataFrame):
            x = x.values.copy().transpose()
        n = x.shape[1]
        phi_list = []
        for Tval in range(2, T + 1, 3):
            centroid, label = kmeans2(x.T, k = Tval, minit = '++', seed = seed)
            #phi = np.zeros([Tval, n])
            phi = np.ones([Tval, n])*0.3/(Tval - 1)
            for i in range(n):
                #phi[label[i], i] = 1.0
                phi[label[i], i] = 0.7
            phi_list += [phi]
            
        with multiprocessing.Pool(n_workers) as pool:
            fun = functools.partial(_model_fit_wrapper_phi, x = x, T = T, model_class = model_class, tolerance = tolerance, max_iter = max_iter, min_iter = min_iter, **prior_hpar)        
            results = pool.map(fun, phi_list)
            for result in results:
                model_list += [result]
                final_elbo += [result.elbo_list[-1]]
    
    # run using random starting points
    if restarts > 0:
        with multiprocessing.Pool(n_workers) as pool:
            fun = functools.partial(_model_fit_wrapper_seed, x = x, T = T, model_class = model_class, tolerance = tolerance, max_iter = max_iter, min_iter = min_iter, **prior_hpar)

            # generate random seeds for each model based on the seed parameter
            seed_list = []
            rng = np.random.default_rng(seed)
            for i in range(restarts):
                seed_list += [rng.integers(low = 1000, high = 9999)]

            results = pool.map(fun, seed_list)
            for result in results:
                model_list += [result]
                final_elbo += [result.elbo_list[-1]]
        
    final_elbo = np.array(final_elbo)
    toc = perf_counter()
    
    return {'final_elbo': final_elbo, 'model_list': model_list, 'best_model': model_list[final_elbo.argmax()], 'fit_time': toc - tic}

def _model_fit_wrapper_seed(seed, x, T, model_class, tolerance, max_iter, min_iter, **prior_hpar):
    """
    Defines a mixture model and fits it to the data with specified random seed, returning the result.
    This function is only defined in order to get the parallelization to work.
    """
    new_model = model_class(x = x, T = T, seed = seed, **prior_hpar)
    new_model.fit(tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
    return new_model

def _model_fit_wrapper_phi(phi, x, T, model_class, tolerance, max_iter, min_iter, **prior_hpar):
    """
    Defines an LPA model and fits it to the data with specified starting value of phi, returning the result.
    This function is only defined in order to get the parallelization to work.
    """
    new_model = model_class(x = x, phi = phi, T = T, seed = None, **prior_hpar)
    new_model.fit(tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
    return new_model