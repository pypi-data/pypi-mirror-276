from .fit_mixture_model import fit_mixture_model
from .lpa import lpa_model

def fit_lpa(x, n_workers = 4, kmeans = False, restarts = 20, T = 20, prior_w1 = 3.0, prior_w2 = 1.0, prior_lambda_mu = 0.5, prior_strength_for_xi = 10.0, seed = 1234, tolerance = 1e-05, max_iter = 1000, min_iter = 10):
    """
    Fit a Dirichlet process latent profile analysis (DPM-LPA) model using mean field
    variational Bayes.
    
    Parameters
    ----------
    x: data frame or array
        Observed data (data frame or matrix).  If a matrix then rows are variables and columns
        are observations; if a data frame then rows are observations and columns are variables.
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
    prior_w1: float, optional
        First prior hyperparameter on alpha.
    prior_w2: float, optional
        Second prior hyperparameter on alpha.
    prior_lambda_mu: float, optional
        Controls the width of the prior distribution on mu: 
        higher values -> tighter prior around 0.
    prior_strength_for_xi: float, optional
        Controls the strength of the gamma prior distribution on xi.
        This prior is assumed to have a mean of 1, with alpha = prior_strength_for_xi/2
        and beta = prior_strength_for_xi/2.
    seed: int, optional
        Random seed (determines starting conditions of each optimization).
    tolerance: float, optional
        Relative change in the ELBO at which the optimization should stop.
    max_iter: integer, optional
        Maximum number of iterations to run the optimization.
    min_iter: integer, optional
        Minimum number of iterations to run the optimization.
    
    Notes
    -----
    This is a wrapper for the fit_mixture_model function.
    
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
    return fit_mixture_model(x = x, model_class = lpa_model, n_workers = n_workers, kmeans = kmeans, restarts = restarts, T = T, prior_w1 = prior_w1, prior_w2 = prior_w2, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, seed = seed, tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)