###################################################
###     	Simulation parameters		###
###################################################

# scaling factor for temporal parameters
# to avoid synchrony due to large delays in the ESS/HMF.
# time_scaling 2.5 maps [1.2, 4.4] to [0.48, 1.76] with mean 1.12, like the
# mean 1.125 ms of the excitatory and inhibitory delays in the original network
time_scaling = 1.

simulator_params = {
    'nest':
    {
      'timestep'        : 0.1 * time_scaling,
      'threads'         : 1,
      'sim_duration'    : 1000. * time_scaling,
      'min_delay'       : 0.1 * time_scaling,
      'max_delay'       : 100 * time_scaling
      # When max_delay is not set, FixedTotalNumberConnect sometimes
      # produces an error as requested delays are larger than the default 10 ms
      # Setting max_delay to np.inf is not good either: the simulation
      # fails as buffers are probably too large
    },
    'spiNNaker':
    {
      'timestep'        : 0.1 * time_scaling,
      'min_delay'       : 0.1 * time_scaling,
      'max_delay'       : 14.4 * time_scaling,
      'sim_duration'    : 1000.0 * time_scaling
    },
    'hardware.brainscales':
    {
      'useSystemSim'    : True, # to use the ESS
      'hardwareNeuronSize': 2, # use 8 for medium2 hardware setup
                               # and 2 for small hardware setup
      'ess_params'      : {'perfectSynapseTrafo': True,
                           'pulseStatisticsFile' : 'pulsestats.txt',
                           'weightDistortion': 0.25},
      'logfile'         : 'logfile.txt',
      'loglevel'        : 3,
      'realizedConnectionMatrixFile' : 'realized_conns.txt',
      'lostConnectionMatrixFile' : 'lost_conns.txt',
      'speedupFactor'   : 10000,
      'sim_duration'    : 1000. * time_scaling,
      'maxNeuronLoss'   : 1.,
      'maxSynapseLoss'  : 1.,
      'mappingStrategy' : 'user',
      'algoinitFilename': 'algoinit_custom_small.pl', # use algoinit_custom.pl for medium2 hardware,
                                      # and algoinit_custom_small.pl for small hardware setup.
      'mappingStatisticsFile' : 'mapping_stats.txt',
      'ignoreDatabase'   : True, # required for ESS if there is a CalibrationDB running
      'rng_seeds'       : [124678], # for HW Poisson generators and Mapping
    }
}

# parameters for run_microcircuit.py (using a queue)
system_params = {
    # number of nodes
    'n_nodes'           : 1,
    # number of MPI processes per node
    'n_procs_per_node'  : 24,
    # walltime for simulation
    'walltime'          : '8:0:0',
    # total memory for simulation
    'memory'            : '4gb',
    # file name for standard output
    'outfile'           : 'output.txt',
    # file name for error output
    'errfile'           : 'errors.txt',
    # absolute path to which the output files should be written
    'output_path'       : 'results',
    # Directory for connectivity I/O
    'conn_dir'		: 'connectivity_0.1_0.1_delays',
    # path to the MPI shell script
    'mpi_path'          : '/usr/local/mpi/openmpi/1.4.3/gcc64/bin/mpivars_openmpi-1.4.3_gcc64.sh',
    # path to back-end
    'backend_path'      : '/path/to/backend',
    # path to pyNN installation
    'pyNN_path'         : '/path/to/pyNN',
    # command for submitting the job
    'submit_cmd'        : 'qsub'
}

