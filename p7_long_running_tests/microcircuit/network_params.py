###################################################
###     	Network parameters		###
###################################################

from sim_params import *

params_dict = {
  'nest':
  {
    # Whether to make random numbers independent of the number of processes
    'parallel_safe': True,
    # Fraction of neurons to simulate
    'N_scaling': 1.,
    # Scaling factor for in-degrees. Upon downscaling, synaptic weights are
    # taken proportional to 1/sqrt(in-degree) and external drive is adjusted
    # to preserve mean and variances of activity in the diffusion approximation.
    # In-degrees and weights of both intrinsic and extrinsic inputs are adjusted.
    # This scaling was not part of the original study, but this option is included
    # here to enable simulations on small systems that give results similar to
    # full-scale simulations.
    'K_scaling': 1.,
    # Neuron model. Possible values: 'IF_curr_exp', 'IF_cond_exp'
    'neuron_model': 'IF_curr_exp',
    # V_model = v_offset + v_scaling*V_PyNN to ensure that conductances and membrane
    # time constants can be found that approximate the original dynamics given
    # e_rev_E = 0, e_rev_I = -100
    'v_offset': 0.,
    'v_scaling': 1.,
    # Connection routine
    # 'fixed_total_number' reproduces the connectivity from Potjans & Diesmann (2014),
    # establishing a fixed number of synapses between each pair of populations.
    # This function is available for the NEST and SpiNNaker back-ends.
    # 'without_multapses' approximates 'fixed_total_number' using single connections
    # with heterogeneous weights. Warning: at least with PyNN 0.7.5 and NEST
    # revision 10711, this function only works correctly on a single process, not in
    # parallel.
    # 'from_list' reads in the connections from file
    'conn_routine': 'fixed_total_number',
    # Whether to save connections to file. See README.txt for known issues with using
    # save_connections in parallel simulations.
    'save_connections': False,
    # Initialization of membrane potentials
    # 'from_list' uses a set of initial neuron voltages read from a file,
    # 'random' uses randomized voltages
    'voltage_input_type': 'random',
    # mean, sd of multiplicative Gaussian noise on weights to mimic neuromorphic hardware
    # (only implemented for conn_type without_multapses)
    # Use [] for no noise and [1., 0.25] to emulate the HMF.
    'w_noise': [],
    # Delay distribution. Possible values: 'normal' and 'uniform'.
    # The original model has normally distributed delays.
    # 'uniform' more closely approximates the distribution on the ESS
    'delay_dist_type': 'normal',
    # Type of background input. Possible values: 'poisson' and 'DC'
    # If 'DC' is chosen, a constant external current is provided, equal to the mean
    # current due to the Poisson input used in the default version of the model.
    'input_type': 'poisson',
    # Whether to draw Poisson input to each neuron from a pool of generators.
    # Can be used to approximate ESS settings, where this feature is needed for
    # limiting input bandwidth.
    'pool_poisson': False,
    # total size of pool of Poisson generators if pool_poisson is True
    'n_poisson_generators': 1000,
    # Whether to record from a fixed fraction of neurons in each population.
    # If False, a fixed number of neurons is recorded.
    'record_fraction': True,
    # Number of neurons from which to record spikes when record_fraction = False
    'n_record': 100,
    # Fraction of neurons from which to record spikes when record_fraction = True
    'frac_record_spikes': 1.,
    # Whether to record membrane potentials
    'record_v': False,
    # Fixed number of neurons from which to record membrane potentials when
    # record_v=True and record_fraction = False
    'n_record_v': 20,
    # Fraction of neurons from which to record membrane potentials when
    # record_v=True and record_fraction = True
    'frac_record_v': 0.1,
    # Whether to record correlations
    'record_corr': False,
    # random number generator seeds for V and connectivity.
    # When parallel_safe is True, only the first is used.
    # When parallel_safe is False, the first num_processes are used.
    'seeds': [2563297, 6231788, 1628140,  740208, 3671632, 5555862, \
              1039783, 7160620, 5939123, 8076622, 5775935, 3416980, \
              1397311, 6307045, 3906414, 7882158, 3264339, 5562636, \
              9329605, 3594087, 2056808, 1101821, 1215034, 3475196],
    # random number generator seed for NEST Poisson generators
    'master_seed': 124678
  },

  'spiNNaker':
  {
    # Whether to make random numbers independent of the number of processes
    'parallel_safe': True,
    # Fraction of neurons to simulate
    'N_scaling': 1.0,
    # Scaling factor for in-degrees. Upon downscaling, synaptic weights are
    # taken proportional to 1/sqrt(in-degree) and external drive is adjusted
    # to preserve mean and variances of activity in the diffusion approximation.
    # In-degrees and weights of both intrinsic and extrinsic inputs are adjusted.
    # This scaling was not part of the original study, but this option is included
    # here to enable simulations on small systems that give results similar to
    # full-scale simulations.
    'K_scaling': 1.0,
    # Neuron model. Possible values: 'IF_curr_exp', 'IF_cond_exp'
    'neuron_model' : 'IF_curr_exp',
    # V_model = v_offset + v_scaling*V_PyNN to ensure that conductances and membrane
    # time constants can be found that approximate the original dynamics given
    # e_rev_E = 0, e_rev_I = -100
    'v_offset': 0.,
    'v_scaling': 1.,
    # Connection routine
    # 'fixed_total_number' reproduces the connectivity from Potjans & Diesmann (2014),
    # establishing a fixed number of synapses between each pair of populations.
    # This function is available for the NEST and SpiNNaker back-ends.
    # 'without_multapses' approximates 'fixed_total_number' using single connections
    # with heterogeneous weights
    # 'from_list' reads in the connections from file
    'conn_routine': 'fixed_total_number',
    # Whether to save connections to file
    'save_connections': False,
    # Initialization of membrane potentials
    # 'from_list' uses a set of initial neuron voltages read from a file,
    # 'random' uses randomized voltages
    'voltage_input_type': 'random',
    'input_dir': 'voltages_0.1_0.1_delays',
    # mean, sd of multiplicative Gaussian noise on weights to mimic neuromorphic hardware
    # (only implemented for conn_type without_multapses)
    # Use [] for no noise and [1., 0.25] to emulate the HMF.
    'w_noise': [],
    # Delay distribution. Possible values: 'normal' and 'uniform'.
    # The original model has normally distributed delays.
    # 'uniform' more closely approximates the distribution on the ESS
    'delay_dist_type': 'normal',
    # Type of background input. Possible values: 'poisson' or 'DC'
    # If 'DC' is chosen, a constant external current is provided, equal to the mean
    # current due to the Poisson input used in the default version of the model.
    'input_type': 'poisson',
    # Whether to draw Poisson input to each neuron from a pool of generators.
    # Can be used to approximate ESS settings, where this feature is needed for
    # limiting input bandwidth.
    'pool_poisson': False,
    # total size of pool of Poisson generators if pool_poisson is True
    'n_poisson_generators': 1000,
    # Whether to record from a fixed fraction of neurons in each population.
    # If False, a fixed number of neurons is recorded.
    'record_fraction': True,
    # Number of neurons from which to record spikes when record_fraction = False
    'n_record': 100,
    # Fraction of neurons from which to record spikes when record_fraction = True
    'frac_record_spikes': 1.,
    # Whether to record membrane potentials
    'record_v': False,
    # Fixed number of neurons from which to record membrane potentials when
    # record_v=True and record_fraction = False
    'n_record_v': 20,
    # Fraction of neurons from which to record membrane potentials when
    # record_v=True and record_fraction = True
    'frac_record_v': 1.0,
    # Whether to record correlations
    'record_corr': False,
    # random number generator seed for V and connectivity.
    'seeds': [2563297],
    # Whether to send output live
    'live_output': False,
  },

  'hardware.brainscales':
  {
    # Fraction of neurons to simulate
    'N_scaling': .1,
    # Scaling factor for in-degrees. Upon downscaling, synaptic weights are
    # taken proportional to 1/sqrt(in-degree) and external drive is adjusted
    # to preserve mean and variances of activity in the diffusion approximation.
    # In-degrees and weights of both intrinsic and extrinsic inputs are adjusted.
    # This scaling was not part of the original study, but this option is included
    # here to enable simulations on small systems that give results similar to
    # full-scale simulations.
    'K_scaling': .1,
    # Neuron model. Possible values: 'IF_curr_exp', 'IF_cond_exp'
    'neuron_model': 'IF_cond_exp',
    # Size of the hardware
    # 'small': 32 HICANNs 'medium' and 'medium2': 128 HICANNs
    # 'medium2' uses a more homogeneous mapping than 'medium'
    'hardware_size': 'small',
    # V_model = v_offset + v_scaling*V_PyNN to ensure that conductances and membrane
    # time constants can be found that approximate the original dynamics given
    # e_rev_E = 0, e_rev_I = -100
    'v_offset': 200.,
    'v_scaling': 6.,
    # Connection routine
    # 'without_multapses' approximates the original connection routine using
    # single connections
    # with heterogeneous weights
    # 'from_list' reads in the connections from file
    'conn_routine': 'without_multapses',
    # Whether to save connections to file
    'save_connections': False,
    # Initialization of membrane potentials
    # 'from_list' uses a set of initial neuron voltages read from a file,
    # 'random' uses randomized voltages
    'voltage_input_type': 'random',
    # Expected fraction of internal synapses that cannot be mapped.
    # Used for adjusting parameters
    'expected_internal_synapse_loss': 0.,
    # Expected fraction of external synapses that cannot be mapped.
    # Used for adjusting parameters
    'expected_external_synapse_loss': 0.,
    # Type of background input. Possible values: 'poisson' and 'DC'
    # If 'DC' is chosen, a constant external current is provided, equal to the mean
    # current due to the Poisson input used in the default version of the model.
    'input_type': 'poisson',
    # Whether to draw Poisson input to each neuron from a pool of generators.
    # Can be used to approximate ESS settings, where this feature is needed for
    # limiting input bandwidth.
    'pool_poisson': True,
    # total size of pool of Poisson generators if pool_poisson is True
    'n_poisson_generators': 1000,
    # Whether to record from a fixed fraction of neurons in each population.
    # If False, a fixed number of neurons is recorded.
    'record_fraction': True,
    # Number of neurons from which to record spikes when record_fraction = False
    'n_record': 1000,
    # Fraction of neurons from which to record spikes when record_fraction = True
    'frac_record_spikes': 1.,
    # Whether to record membrane potentials
    'record_v': True,
    # Fixed number of neurons from which to record membrane potentials when
    # record_v=True and record_fraction = False
    'n_record_v': 20,
    # Fraction of neurons from which to record membrane potentials when
    # record_v=True and record_fraction = True
    'frac_record_v': 0.02,
    # Whether to record correlations
    'record_corr': False,
    # random number generator seed for V and connectivity
    'seeds': [2563297]
    }
}

# Simulator back-end. Choose from 'nest', 'spiNNaker', 'hardware.brainscales'
simulator = 'spiNNaker'

# Load params from params_dict into global namespace
globals().update(params_dict[simulator])

# Relative inhibitory synaptic weight
g = -4.

if neuron_model == 'IF_curr_exp':
    neuron_params = {'cm'        : 0.25,              # nF
                     'i_offset'  : 0.0 / time_scaling,  # nA
                     'tau_m'     : 10.0 * time_scaling, # ms
                     'tau_refrac': 2.0 * time_scaling,  # ms
                     'tau_syn_E' : 0.5 * time_scaling,  # ms
                     'tau_syn_I' : 0.5 * time_scaling,  # ms
                     'v_reset'   : (-65.0-v_offset) / v_scaling, # mV
                     'v_rest'    : (-65.0-v_offset) / v_scaling, # mV
                     'v_thresh'  : (-50.0-v_offset) / v_scaling # mV
                     }

if neuron_model == 'IF_cond_exp':
    neuron_params = {'cm'         : 0.2,
                     'e_rev_E'    : 0.0,
                     'e_rev_I'    : -100.0,
                     'i_offset'   : 0.0 / time_scaling,
                     'tau_refrac' : 2.0 * time_scaling,
                     'tau_syn_E'  : 0.5 * time_scaling,
                     'tau_syn_I'  : 0.5 * time_scaling,
                     'v_reset'    : -50.0,
                     'v_rest'     : -50.0
                     }

v_rest_base = neuron_params['v_rest']

layers = {'L23': 0, 'L4': 1, 'L5': 2, 'L6': 3}
n_layers = len(layers)
pops = {'E': 0, 'I': 1}
n_pops_per_layer = len(pops)
structure = {'L23': {'E':0, 'I':1},
             'L4' : {'E':2, 'I':3},
             'L5' : {'E':4, 'I':5},
             'L6' : {'E':6, 'I':7}}

# Numbers of neurons in full-scale model
N_full = {
  'L23': {'E': 20683, 'I': 5834},
  'L4' : {'E': 21915, 'I': 5479},
  'L5' : {'E': 4850,  'I': 1065},
  'L6' : {'E': 14395, 'I': 2948}
}

# Probabilities for >=1 connection between neurons in the given populations.
# The first index is for the target population; the second for the source population
#             2/3e      2/3i    4e      4i      5e      5i      6e      6i
conn_probs = [[0.1009,  0.1689, 0.0437, 0.0818, 0.0323, 0.,     0.0076, 0.    ],
             [0.1346,   0.1371, 0.0316, 0.0515, 0.0755, 0.,     0.0042, 0.    ],
             [0.0077,   0.0059, 0.0497, 0.135,  0.0067, 0.0003, 0.0453, 0.    ],
             [0.0691,   0.0029, 0.0794, 0.1597, 0.0033, 0.,     0.1057, 0.    ],
             [0.1004,   0.0622, 0.0505, 0.0057, 0.0831, 0.3726, 0.0204, 0.    ],
             [0.0548,   0.0269, 0.0257, 0.0022, 0.06,   0.3158, 0.0086, 0.    ],
             [0.0156,   0.0066, 0.0211, 0.0166, 0.0572, 0.0197, 0.0396, 0.2252],
             [0.0364,   0.001,  0.0034, 0.0005, 0.0277, 0.008,  0.0658, 0.1443]]

# In-degrees for external inputs
K_ext = {
  'L23': {'E': 1600, 'I': 1500},
  'L4' : {'E': 2100, 'I': 1900},
  'L5' : {'E': 2000, 'I': 1900},
  'L6' : {'E': 2900, 'I': 2100}
}

# Mean rates in the full-scale model, necessary for scaling
# Precise values differ somewhat between network realizations
full_mean_rates = {
  'L23': {'E': 0.971 / time_scaling, 'I': 2.868 / time_scaling},
  'L4' : {'E': 4.746 / time_scaling, 'I': 5.396 / time_scaling},
  'L5' : {'E': 8.142 / time_scaling, 'I': 9.078 / time_scaling},
  'L6' : {'E': 0.991 / time_scaling, 'I': 7.523 / time_scaling}
}

if pool_poisson:
    # rate of each Poisson generator in spikes/s.
    # If chosen as 800*K_scaling/n, the input rates of the model with independent
    # Poisson generators can be precisely reproduced. A higher rate means that different
    # neurons receive input from fewer common sources, but larger overlap between their
    # spike trains in case of common sources.
    poisson_rate = 40. / time_scaling

# Mean and standard deviation of initial membrane potential distribution
V0_mean = -58. # mV
V0_sd = 5.     # mV

# Background rate per synapse
bg_rate = 8. / time_scaling # spikes/s

# Mean synaptic weight for all excitatory projections except L4e->L2/3e
w_mean = 87.8e-3 / time_scaling # nA
# Mean synaptic weight for L4e->L2/3e connections
# See p. 801 of the paper, second paragraph under 'Model Parameterization',
# and the caption to Supplementary Fig. 7
w_234 = 2 * w_mean # nA

# Standard deviation of weight distribution relative to mean for
# all projections except L4e->L2/3e
w_rel = 0.1
# Standard deviation of weight distribution relative to mean for L4e->L2/3e
# This value is not mentioned in the paper, but is chosen to match the
# original code by Tobias Potjans
w_rel_234 = 0.05

# Means and standard deviations of delays from given source populations (ms)
# When delay_dist_type is 'uniform', delays are drawn from [d_mean-d_sd, d_mean+d_sd].
# To approximate the ESS/HMF delays using NEST, use uniform delays with:
# d_mean = {'E': 2.8, 'I': 2.8}
# d_sd = {'E': 1.6, 'I': 1.6}
d_mean = {'E': 1.5 * time_scaling, 'I': 0.75 * time_scaling}
d_sd = {'E': 0.75 * time_scaling, 'I': 0.375 * time_scaling}

# Parameters for transient thalamic input
thalamic_input = False
thal_params = {
  # Number of neurons in thalamic population
  'n_thal'      : 902,
  # Connection probabilities
  'C'           : {'L23': {'E': 0, 'I': 0},
                   'L4' : {'E': 0.0983, 'I': 0.0619},
                   'L5' : {'E': 0, 'I': 0},
                   'L6' : {'E': 0.0512, 'I': 0.0196}},
  'rate'        : 120. / time_scaling, # spikes/s;
  # Note that the rate is erroneously given as 15 spikes/s in the paper.
  # The rate actually provided was 120 spikes/s.
  'start'       : 300. * time_scaling, # ms
  'duration'    : 10. * time_scaling  # ms;
}

# Maximum delay over which to determine covariances
tau_max = 100.*time_scaling

# Parameters for plots of spiking activity
plot_spiking_activity = True
# raster_t_min and raster_t_max include the time scaling factor
raster_t_min = 0 # ms
raster_t_max = simulator_params[simulator]['sim_duration'] # ms
# Fraction of recorded neurons to include in raster plot
frac_to_plot = 0.5

# Numbers of neurons from which to record spikes
n_rec = {}
for layer in layers:
    n_rec[layer] = {}
    for pop in pops:
        if record_fraction:
            n_rec[layer][pop] = min(int(round(N_full[layer][pop] * N_scaling * frac_record_spikes)), \
                                    int(round(N_full[layer][pop] * N_scaling)))
        else:
            n_rec[layer][pop] = min(n_record, int(round(N_full[layer][pop] * N_scaling)))

