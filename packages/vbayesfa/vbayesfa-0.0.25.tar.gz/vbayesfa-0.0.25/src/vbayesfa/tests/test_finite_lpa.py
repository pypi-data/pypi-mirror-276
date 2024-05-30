import numpy as np
from numpy.testing import *
from vbayesfa.fit_finite_lpa import fit_finite_lpa
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
    model = fit_finite_lpa(sim_data['x'],
                           prior_alpha_pi = 1.0,
                           prior_lambda_mu = 0.5,
                           prior_strength_for_xi = 10.0,
                           max_iter = 50, 
                           min_iter = 30, 
                           restarts = 4,
                           T = 20,
                           tolerance = 1e-5, 
                           seed = 1234)['best_model']
    
    assert_equal(model.z_hat, np.array([0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1]))
    assert_almost_equal(model.sorted_m_mu[:,0], np.array([1.49512785, 1.27882941, -2.37791281, -2.19847068, -1.26148931]))
    assert_almost_equal(model.sorted_m_mu[:,1], np.array([1.01462039, 4.74435135, 1.54365648, 0.70046747, 2.47351813]))
    assert_almost_equal(model.elbo_list[-1], -117.26549798604742)