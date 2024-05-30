import numpy as np
from numpy.testing import *
from vbayesfa.fit_lpa import fit_lpa
from vbayesfa import simulate_data

# to run all tests: pytest /Users/sampaskewitz/Documents/vbayesfa/src/vbayesfa/tests

def test_fit_lpa():
    # create simple synthetic data
    sim_data = simulate_data.latent_profile(n = 20, 
                                            m = 5,
                                            separation = 3.0,
                                            n_profiles = 2,
                                            sample_z = True,
                                            seed = 1234,
                                            mu = None,
                                            pi = None)

    # fit the model
    model = fit_lpa(sim_data['x'], 
                    prior_w1 = 3.0,
                    prior_w2 = 1.0,
                    prior_lambda_mu = 0.5,
                    prior_strength_for_xi = 10.0,
                    max_iter = 50, 
                    min_iter = 30, 
                    restarts = 4, 
                    T = 20, 
                    tolerance = 1e-5, 
                    seed = 1234)['best_model']
    model.print_summary()
    assert_equal(model.z_hat, np.array([0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1]))
    assert_almost_equal(model.sorted_m_mu[:,0], np.array([1.49505099, 1.27884819, -2.37783417, -2.19846618, -1.26139709]))
    assert_almost_equal(model.sorted_m_mu[:,1], np.array([1.01461892, 4.74435739, 1.54366584, 0.70047062, 2.47352321]))
    assert_almost_equal(model.elbo_list[-1], -116.39303540575003)