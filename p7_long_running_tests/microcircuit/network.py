from network_params import *
from sim_params import *
from scaling import get_indegrees, adjust_w_and_ext_to_K
from connectivity import *
from get_conductances import *
from helper_functions import create_weight_matrix, get_init_voltages_from_file
import pyNN
from pyNN.random import NumpyRNG, RandomDistribution
import numpy as np
import sys

class Network:

    def __init__(self, sim):
        return None

    def setup(self,sim):

        if simulator == 'hardware.brainscales' or parallel_safe:
            script_rng = NumpyRNG(seed=seeds[0], parallel_safe=True)
        else:
            script_rng = NumpyRNG(seed=seeds[sim.rank()], parallel_safe=False)

        self.projections = {}
        self.weight_objs = {}
        self.delay_objs = {}

        # Compute DC input before scaling
        if input_type == 'DC':
            self.DC_amp = {}
            for target_layer in layers:
                self.DC_amp[target_layer] = {}
                for target_pop in pops:
                    self.DC_amp[target_layer][target_pop] = bg_rate * \
                    K_ext[target_layer][target_pop] * w_mean * neuron_params['tau_syn_E'] / 1000.
        else:
            self.DC_amp = {'L23': {'E':0., 'I':0.},
                           'L4' : {'E':0., 'I':0.},
                           'L5' : {'E':0., 'I':0.},
                           'L6' : {'E':0., 'I':0.}}

        # In-degrees of the full-scale and scaled models
        K_full = get_indegrees()
        self.K = K_scaling * K_full

        self.K_ext = {}
        for layer in layers:
            self.K_ext[layer] = {}
            for pop in pops:
                self.K_ext[layer][pop] = K_scaling * K_ext[layer][pop]

        if neuron_model == 'IF_curr_exp':
            self.w = create_weight_matrix('IF_curr_exp')
            # Network scaling
            if K_scaling != 1:
                self.w, self.w_ext, self.DC_amp = adjust_w_and_ext_to_K(K_full, K_scaling, self.w, self.DC_amp)
            else:
                self.w_ext = w_mean

        if neuron_model == 'IF_cond_exp' :
            # Determine synaptic conductances that closely approximate the current-based dynamics
            # taking any in-degree scaling into account
            g_e, g_i, self.g_ext, tau_m, v_rest_intended = get_cond(self.DC_amp)
            self.w = create_weight_matrix('IF_cond_exp', g_e=g_e, g_i=g_i)

            v_thresh = {}
            for layer in layers:
                v_thresh[layer] = {}
                for pop in pops:
                    v_thresh[layer][pop] = (-50. - v_rest_intended[layer][pop])/v_scaling - 50.

        if 'v_thresh' in neuron_params:
            Vthresh = {}
            for layer in layers:
                Vthresh[layer] = {}
                for pop in pops:
                    Vthresh[layer][pop] = neuron_params['v_thresh']
        else:
            Vthresh = v_thresh

        # Initial membrane potential distributions
        # The original study used V0_mean = -58 mV, V0_sd = 5 mV.
        # This is adjusted here to any changes in v_rest and scaling of V.

        V0_mean = {}
        V0_sd = {}
        for layer in layers:
            V0_mean[layer] = {}
            V0_sd[layer] = {}
            for pop in pops:
                V0_mean[layer][pop] = (neuron_params['v_rest'] + Vthresh[layer][pop]) / 2.
                V0_sd[layer][pop] = (Vthresh[layer][pop] - neuron_params['v_rest']) / 3.

        V_dist = {}
        for layer in layers:
            V_dist[layer] = {}
            for pop in pops:
                V_dist[layer][pop] = RandomDistribution( \
                    'normal', [V0_mean[layer][pop], V0_sd[layer][pop]], rng=script_rng)

        model = getattr(sim, neuron_model)

        if record_corr and simulator == 'nest':
            # Create correlation recording device
            sim.nest.SetDefaults('correlomatrix_detector', {'delta_tau': 0.5})
            self.corr_detector = sim.nest.Create('correlomatrix_detector')
            sim.nest.SetStatus(self.corr_detector, {'N_channels': n_layers*n_pops_per_layer, \
                                                    'tau_max': tau_max, 'Tstart': tau_max})


        if sim.rank() == 0:
            print 'neuron_params:', neuron_params
            print 'K: ', self.K
            print 'K_ext: ', self.K_ext
            print 'w: ', self.w
            if neuron_model == 'IF_curr_exp':
                print 'w_ext: ', self.w_ext
                print 'DC_amp: ', self.DC_amp
            if neuron_model == 'IF_cond_exp':
                print 'g_ext: ', self.g_ext
                print 'tau_m: ', tau_m
            print 'V0_mean: '
            for layer in layers:
                for pop in pops:
                    print layer, pop, V0_mean[layer][pop]
            print 'n_rec:'
            for layer in layers:
                for pop in pops:
                    print layer, pop, n_rec[layer][pop]
                    if not record_fraction and n_record > int((N_full[layer][pop] * N_scaling)):
                        print 'Note that requested number of neurons to record exceeds ', \
                               layer, pop, ' population size'


        # Create cortical populations
        self.pops = {}
        global_neuron_id = 1
        self.base_neuron_ids = {}
        for layer in layers:
            self.pops[layer] = {}
            for pop in pops:
                if neuron_model == 'IF_cond_exp':
                    neuron_params['tau_m'] = tau_m[layer][pop]
                    neuron_params['v_thresh'] = v_thresh[layer][pop]

                self.pops[layer][pop] = sim.Population( \
                    int((N_full[layer][pop] * N_scaling)), \
                    model, cellparams=neuron_params, label=layer+pop)
                this_pop = self.pops[layer][pop]

                # Provide DC input in the current-based case
                # DC input is assumed to be absent in the conductance-based case
                if neuron_model == 'IF_curr_exp':
                    this_pop.set('i_offset', self.DC_amp[layer][pop])

                self.base_neuron_ids[this_pop] = global_neuron_id
                global_neuron_id += len(this_pop) + 2

                if voltage_input_type == 'random':
                    this_pop.initialize('v', V_dist[layer][pop])
                elif voltage_input_type == 'from_list':
                    this_pop.initialize('v', get_init_voltages_from_file(this_pop))

                # Spike recording
                if simulator == 'spiNNaker':
                    this_pop.record()
                    if live_output:
                        from spynnaker_external_devices_plugin.pyNN \
                            import activate_live_output_for
                        activate_live_output_for(this_pop)
                else:
                    this_pop[0:n_rec[layer][pop]].record()

                # Membrane potential recording
                if record_v:
                    if simulator == 'spiNNaker':
                        this_pop.record_v()
                    else:
                        if record_fraction:
                            n_rec_v = round(this_pop.size * frac_record_v)
                        else :
                            n_rec_v = n_record_v
                    this_pop[0 : n_rec_v].record_v()

                # Correlation recording
                if record_corr and simulator == 'nest':
                    index = structure[layer][pop]
                    sim.nest.SetDefaults('static_synapse', {'receptor_type': index})
                    sim.nest.ConvergentConnect(list(this_pop.all_cells), self.corr_detector)


        if record_corr and simulator == 'nest':
            # reset receptor_type
            sim.nest.SetDefaults('static_synapse', {'receptor_type': 0})

        if thalamic_input:
        # Create thalamic population
            self.thalamic_population = sim.Population( \
                thal_params['n_thal'], sim.SpikeSourcePoisson, {'rate': thal_params['rate'], \
                'start': thal_params['start'], 'duration': thal_params['duration']}, \
                label='thalamic_population')
            self.base_neuron_ids[self.thalamic_population] = global_neuron_id
            global_neuron_id += len(self.thalamic_population) + 2

        if pool_poisson:
        # Create pool of Poisson sources
            poisson_pool = sim.Population(n_poisson_generators, sim.SpikeSourceArray, label='poisson_pool')
            sim_duration = simulator_params[simulator]['sim_duration']
            # distribution from which to draw total numbers of spikes for each generator
            poisson_dist = RandomDistribution('poisson', [poisson_rate * sim_duration / 1000.], rng=script_rng)
            # distribution from which to draw spike times
            uniform_dist = RandomDistribution('uniform', [0, sim_duration], rng=script_rng)
            for pois in poisson_pool:
                n_spikes = poisson_dist.next(mask_local=False)
                if n_spikes > 0:
                    if n_spikes == 1:
                        pois_params = {'spike_times': [np.sort(uniform_dist.next(mask_local=False))]}
                    else:
                        pois_params = {'spike_times': np.sort(uniform_dist.next(n_spikes, mask_local=False))}

                    pois.set_parameters(**pois_params)

        possible_targets_curr = ['inhibitory', 'excitatory']
        possible_targets_cond = {'E': 'excitatory', 'I': 'inhibitory'}

        # Connect

        for target_layer in layers:
            for target_pop in pops:
                target_index = structure[target_layer][target_pop]
                this_target_pop = self.pops[target_layer][target_pop]
                if neuron_model == 'IF_curr_exp':
                    w_ext = self.w_ext
                elif neuron_model == 'IF_cond_exp':
                    w_ext = self.g_ext[target_layer][target_pop]
                # External inputs
                if input_type == 'poisson':
                    rate = bg_rate * self.K_ext[target_layer][target_pop]

                    if pool_poisson:
                        if sim.rank() == 0:
                            print 'connecting Poisson pool to', target_layer, target_pop
                        poisson_generator = poisson_pool
                        n_poisson_per_neuron = int(rate / poisson_rate)
                        conn = sim.FixedNumberPreConnector(n_poisson_per_neuron, weights = w_ext)
                        sim.Projection(poisson_pool, this_target_pop, conn, target = 'excitatory')
                    else : # unpooled (independent) Poisson inputs
                        if simulator == 'nest':
                        # create only a single Poisson generator for each population,
                        # since the native NEST implementation sends independent spike trains to all targets
                            if sim.rank() == 0:
                                print 'connecting Poisson generator to', target_layer, target_pop, ' via SLI'
                            sim.nest.sli_run('/poisson_generator Create /poisson_generator_e Set poisson_generator_e << /rate ' \
                                + str(rate) + ' >> SetStatus')
                            sim.nest.sli_run("poisson_generator_e " + str(list(this_target_pop.all_cells)).replace(',', '') \
                                + " [" + str(1000 * w_ext) + "] [" + str(d_mean['E']) + "] DivergentConnect")
                        else : # simulators other than NEST
                            if sim.rank() == 0:
                                print 'connecting Poisson generators to', target_layer, target_pop
                            poisson_generator = sim.Population(this_target_pop.size, \
                                sim.SpikeSourcePoisson, {'rate': rate})
                            conn = sim.OneToOneConnector(weights = w_ext)
                            print "Poisson input rate {}, weight to {}{} = {}".format(rate, target_layer, target_pop, w_ext)
                            sim.Projection(poisson_generator, this_target_pop, conn, target = 'excitatory')

                if thalamic_input:
                    # Thalamic inputs
                    if sim.rank() == 0:
                        print 'creating thalamic connections to ' + target_layer + target_pop
                    C_thal = thal_params['C'][target_layer][target_pop]
                    n_target = N_full[target_layer][target_pop]
                    K_thal = round(np.log(1 - C_thal) / np.log((n_target * thal_params['n_thal'] - 1.)/ \
                             (n_target * thal_params['n_thal']))) / n_target * K_scaling
                    if conn_routine == 'fixed_total_number':
                        if simulator == 'spiNNaker':
                            FixedTotalNumberConnect2(sim, self.thalamic_population, \
                                this_target_pop, K_thal, w_ext, w_rel * w_ext, \
                                d_mean['E'], d_sd['E'], 'excitatory', script_rng)
                        else:
                            FixedTotalNumberConnect(sim, self.thalamic_population, \
                                this_target_pop, K_thal, w_ext, w_rel * w_ext, \
                                d_mean['E'], d_sd['E'])
                    elif conn_routine == 'without_multapses':
                        ConnectWithoutMultapses(sim, self.thalamic_population, this_target_pop, K_thal, w_ext, \
                                                w_rel * w_ext, d_mean['E'], d_sd['E'], \
                                                'excitatory', script_rng)
                    elif conn_routine == 'from_list':
                        FromListConnect(sim, self.thalamic_population, this_target_pop, 'excitatory', self.base_neuron_ids)

                # Recurrent inputs
                for source_layer in layers:
                    for source_pop in pops:
                        source_index = structure[source_layer][source_pop]
                        this_source_pop = self.pops[source_layer][source_pop]
                        weight = self.w[target_index][source_index]

                        if neuron_model == 'IF_curr_exp':
                            conn_type = possible_targets_curr[int((np.sign(weight)+1)/2)]
                        elif neuron_model == 'IF_cond_exp':
                            conn_type = possible_targets_cond[source_pop]

                        if sim.rank() == 0:
                            print 'creating connections from ' + source_layer + \
                            source_pop + ' to ' + target_layer + target_pop

                        if source_pop == 'E' and source_layer == 'L4' and target_layer == 'L23' and target_pop == 'E':
                            w_sd = weight * w_rel_234
                        else:
                            w_sd = abs(weight * w_rel)

                        print "{}{} to {}{}, weight={}, w_sd={}, delay={}, d_sd={}".format(source_layer, source_pop, target_layer, target_pop, weight, w_sd, d_mean[source_pop], d_sd[source_pop])

                        if conn_routine == 'fixed_total_number':
                            if simulator == 'spiNNaker':
                                FixedTotalNumberConnect2( \
                                    sim, this_source_pop, this_target_pop, \
                                    self.K[target_index][source_index], weight, w_sd, \
                                    d_mean[source_pop], d_sd[source_pop], conn_type, script_rng)
                            else :
                                FixedTotalNumberConnect( \
                                    sim, this_source_pop, this_target_pop, \
                                    self.K[target_index][source_index], weight, w_sd, \
                                    d_mean[source_pop], d_sd[source_pop])
                        elif conn_routine == 'without_multapses' :
                            ConnectWithoutMultapses( \
                                sim, this_source_pop, this_target_pop, \
                                self.K[target_index][source_index], weight, w_sd, \
                                d_mean[source_pop], d_sd[source_pop], conn_type, script_rng)
                        elif conn_routine == 'from_list' :
                            FromListConnect(sim, this_source_pop, this_target_pop, conn_type, self.base_neuron_ids)
