import pyNN
import time
import numpy as np
import spynnaker7.pyNN as sim
from pyNN.random import NumpyRNG

# Random number seed
seed = 2563297

# Input type - "DC" or "Poisson"
input_type = "DC"

# Background rate per synapse in spikes / s (Hz)
bg_rate = 8.

# Mean synaptic weight for all excitatory projections except L4e->L2/3e in nA
w_mean = 87.8e-3

# Mean synaptic weight for L4e->L2/3e connections in nA
w_234 = 2 * w_mean

neuron_params = {'cm': 0.25,  # nF
                 'i_offset': 0.0,  # nA
                 'tau_m': 10.0,  # ms
                 'tau_refrac': 2.0,  # ms
                 'tau_syn_E': 0.5,  # ms
                 'tau_syn_I': 0.5,  # ms
                 'v_reset': -65.0,  # mV
                 'v_rest': -65.0,  # mV
                 'v_thresh': -50.0  # mV
                 }


layers = {'L23': 0, 'L4': 1, 'L5': 2, 'L6': 3}
n_layers = len(layers)
pops = {'E': 0, 'I': 1}
n_pops_per_layer = len(pops)
structure = {'L23': {'E': 0, 'I': 1},
             'L4': {'E': 2, 'I': 3},
             'L5': {'E': 4, 'I': 5},
             'L6': {'E': 6, 'I': 7}}

# Numbers of neurons in full-scale model
N_full = {
    'L23': {'E': 20683, 'I': 5834},
    'L4': {'E': 21915, 'I': 5479},
    'L5': {'E': 4850, 'I': 1065},
    'L6': {'E': 14395, 'I': 2948}
}

# Probabilities for >=1 connection between neurons in the given populations.
# The first index is for the target population; the second for the source
# population
conn_probs = [
    # 2/3e    2/3i    4e      4i      5e      5i      6e      6i
    [0.1009, 0.1689, 0.0437, 0.0818, 0.0323, 0.0000, 0.0076, 0.0000],  # 2/3e
    [0.1346, 0.1371, 0.0316, 0.0515, 0.0755, 0.0000, 0.0042, 0.0000],  # 2/3i
    [0.0077, 0.0059, 0.0497, 0.1350, 0.0067, 0.0003, 0.0453, 0.0000],  # 4e
    [0.0691, 0.0029, 0.0794, 0.1597, 0.0033, 0.0000, 0.1057, 0.0000],  # 4i
    [0.1004, 0.0622, 0.0505, 0.0057, 0.0831, 0.3726, 0.0204, 0.0000],  # 5e
    [0.0548, 0.0269, 0.0257, 0.0022, 0.0600, 0.3158, 0.0086, 0.0000],  # 5i
    [0.0156, 0.0066, 0.0211, 0.0166, 0.0572, 0.0197, 0.0396, 0.2252],  # 6e
    [0.0364, 0.0010, 0.0034, 0.0005, 0.0277, 0.0080, 0.0658, 0.1443]]  # 6i

# In-degrees for external inputs
K_ext = {
    'L23': {'E': 1600, 'I': 1500},
    'L4': {'E': 2100, 'I': 1900},
    'L5': {'E': 2000, 'I': 1900},
    'L6': {'E': 2900, 'I': 2100}
}

# =========================================================
# Start of simulation itself
sim.setup(timestep=0.1, min_delay=0.1, max_delay=14.4)

sim.set_number_of_neurons_per_core('IF_curr_exp', 80)
sim.set_number_of_neurons_per_core('SpikeSourcePoisson', 80)

# create network
script_rng = NumpyRNG(seed=seed, parallel_safe=True)

# Compute DC input before scaling
DC_amp = {'L23': {'E': 0., 'I': 0.},
          'L4': {'E': 0., 'I': 0.},
          'L5': {'E': 0., 'I': 0.},
          'L6': {'E': 0., 'I': 0.}}
if input_type == 'DC':
    for target_layer in layers:
        DC_amp[target_layer] = {}
        for target_pop in pops:
            DC_amp[target_layer][target_pop] = (
                bg_rate * K_ext[target_layer][target_pop] * w_mean *
                neuron_params['tau_syn_E'] / 1000.)

n = network.Network(sim)
n.setup(sim)

# simulate
sim.run(1000.0)

for layer in layers:
    for pop in pops:
        filename = (
            'results/spikes_' + layer + pop + '.dat')
        n.pops[layer][pop].printSpikes(filename)

plotting.plot_raster_bars(
    raster_t_min, raster_t_max, n_rec, frac_to_plot,
    'results/')

sim.end()
