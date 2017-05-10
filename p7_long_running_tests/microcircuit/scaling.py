#############################################################################
### Functions for computing and adjusting connection and input parameters ###   
#############################################################################

import numpy as np
from network_params import *

def get_indegrees():
    '''Get in-degrees for each connection for the full-scale (1 mm^2) model'''
    K = np.zeros([n_layers*n_pops_per_layer, n_layers*n_pops_per_layer])
    for target_layer in layers:
        for target_pop in pops:
            for source_layer in layers:
                for source_pop in pops:
                    target_index = structure[target_layer][target_pop]
                    source_index = structure[source_layer][source_pop]
                    n_target = N_full[target_layer][target_pop]
                    n_source = N_full[source_layer][source_pop]
                    K[target_index][source_index] = round(np.log(1. - \
                        conn_probs[target_index][source_index]) / np.log( \
                        (n_target * n_source - 1.) / (n_target * n_source))) / n_target
    return K


def adjust_w_and_ext_to_K(K_full, K_scaling, w, DC):
    '''Adjust synaptic weights and external drive to the in-degrees
     to preserve mean and variance of inputs in the diffusion approximation'''

    if simulator == 'hardware.brainscales':
        internal_scaling = K_scaling * (1. - expected_internal_synapse_loss)
    else :
        internal_scaling = K_scaling
   
    w_new = w / np.sqrt(internal_scaling)
    I_ext = {}
    for target_layer in layers:
        I_ext[target_layer] = {}
        for target_pop in pops:
            target_index = structure[target_layer][target_pop]
            x1 = 0
            for source_layer in layers:
                for source_pop in pops:
                    source_index = structure[source_layer][source_pop]
                    x1 += w[target_index][source_index] * K_full[target_index][source_index] * \
                        full_mean_rates[source_layer][source_pop]

            if input_type == 'poisson':
                x1_ext = w_mean * K_ext[target_layer][target_pop] * bg_rate
                if simulator == 'hardware.brainscales':
                    external_scaling = K_scaling * (1. - expected_external_synapse_loss)
                else :
                    external_scaling = K_scaling
                w_ext_new = w_mean / np.sqrt(external_scaling)
                I_ext[target_layer][target_pop] = 0.001 * neuron_params['tau_syn_E'] * \
                    ((1. - np.sqrt(internal_scaling)) * x1 + \
                    (1. - np.sqrt(external_scaling)) * x1_ext) + DC[target_layer][target_pop]
            else :
                w_ext_new = np.nan
                I_ext[target_layer][target_pop] = 0.001 * neuron_params['tau_syn_E'] * \
                    ((1. - np.sqrt(internal_scaling)) * x1) + DC[target_layer][target_pop]

    return w_new, w_ext_new, I_ext    



def adjust_w_and_g_to_K(K_full, K_scaling, w):
    ''' Calculate target-population-specific synaptic weights that approximately preserve 
        the mean and variance of the population activities for the given full-scale in-degrees,
        making all excitatory weights equal for the given target population'''
    g_new = {}
    w_new = {}
    w_m_matrix = np.zeros([n_layers * n_pops_per_layer, n_layers * n_pops_per_layer])
    for target_layer in layers:
        g_new[target_layer] = {}
        w_new[target_layer] = {}
        for target_pop in pops:
            target_index = structure[target_layer][target_pop]
            x0 = {'E': 0, 'I': 0}
            x1 = {'E': 0, 'I': 0}
            x2 = {'E': 0, 'I': 0}
            for source_layer in layers:
                for source_pop in pops:
                    source_index = structure[source_layer][source_pop]
                    x0[source_pop] += K_full[target_index][source_index] * full_mean_rates[source_layer][source_pop]
                    x1[source_pop] += w[target_index][source_index] * K_full[target_index][source_index] * \
                        full_mean_rates[source_layer][source_pop]
                    x2[source_pop] += (w[target_index][source_index])**2 * K_full[target_index][source_index] * \
                        full_mean_rates[source_layer][source_pop]

            N_min = (x1['E'] + x1['I'])**2 / ((x0['E'] + x0['I']) * (x2['E'] + x2['I']))
            w_new[target_layer][target_pop] = (np.sqrt(x0['E']) * (x1['E'] + x1['I']) \
                + np.sqrt(x0['I'] * K_scaling * (x0['E'] + x0['I']) * (x2['E'] + x2['I']) \
                - x0['I'] * (x1['E'] + x1['I'])**2)) / (K_scaling * np.sqrt(x0['E']) * (x0['E'] + x0['I']))
            g_new[target_layer][target_pop] = (x1['E'] + x1['I'] - w_new[target_layer][target_pop] \
                * K_scaling * x0['E']) / (w_new[target_layer][target_pop] * K_scaling * x0['I'])

    for target_layer in layers:
        for target_pop in pops:
            target_index = structure[target_layer][target_pop]
            x2_new = {'E' : 0, 'I' : 0}
            for source_layer in layers:
                for source_pop in pops:
                    source_index = structure[source_layer][source_pop]
                    if source_pop == 'E':
                        w_m_matrix[target_index][source_index] = w_new[target_layer][target_pop]
                    else:
                        w_m_matrix[target_index][source_index] = g_new[target_layer][target_pop] * \
                            w_new[target_layer][target_pop]
                    # test if new variance equals old variance
                    x2_new[source_pop] += (w_m_matrix[target_index][source_index])**2 * K_scaling * \
                        K_full[target_index][source_index] * full_mean_rates[source_layer][source_pop]

    return w_m_matrix

