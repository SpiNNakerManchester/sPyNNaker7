from network_params import *
import random
from scipy import stats
import os
import math
import pyNN
from pyNN.random import RandomDistribution
from sim_params import *
import numpy as np

def FixedTotalNumberConnect(sim, pop1, pop2, K, w_mean, w_sd, d_mean, d_sd):
    """Function connecting two populations with multapses and a fixed total number of synapses"""

    if not K:
        return

    source_neurons = list(pop1.all_cells)
    target_neurons = list(pop2.all_cells)
    n_syn = int(round(K*len(target_neurons)))
    # weights are multiplied by 1000 because NEST uses pA whereas PyNN uses nA
    # RandomPopulationConnectD is called on each process with the full sets of
    # source and target neurons, and internally only connects the target
    # neurons on the current process.

    wd_dict = {'weight_m': 1000. * w_mean,
               'weight_s': 1000. * w_sd,
               'delay_m': d_mean,
               'delay_s': d_sd}

    sim.nest.sli_push(source_neurons)
    sim.nest.sli_push(target_neurons)
    sim.nest.sli_push(n_syn)
    sim.nest.sli_push(wd_dict)
    sim.nest.sli_run("/static_synapse RandomPopulationConnectD")

    if save_connections:
        # - weights are in pA
        # - no header lines
        # - one file for each MPI process
        # - GIDs

        # get connections to target on this MPI process
        conn = sim.nest.GetConnections(source=source_neurons, target=target_neurons)
        conns = sim.nest.GetStatus(conn, ['source', 'target', 'weight', 'delay'])
        if not os.path.exists(system_params['conn_dir']):
            try:
                os.makedirs(system_params['conn_dir'])
            except OSError, e:
                if e.errno != 17:
                    raise
                pass
        f = open(system_params['conn_dir'] +  '/' + pop1.label + "_" + \
                 pop2.label + '.conn' + str(sim.rank()), 'w')
        for c in conns:
            print >> f, str(c).replace('(','').replace(')','').replace(', ', '\t')
        f.close()



def FixedTotalNumberConnect2(sim, pop1, pop2, K, w_mean, w_sd, d_mean, d_sd, conn_type, rng):
    """SpiNNaker-specific function connecting two populations with multapses and a fixed total number of synapses"""

    if not K:
        return

    n_syn = int(round(K*len(pop2)))

    if delay_dist_type == 'normal':
        d_dist = RandomDistribution('normal', [d_mean, d_sd], rng=rng, \
                 boundaries=(simulator_params[simulator]['min_delay'], \
                 simulator_params[simulator]['max_delay']), constrain='redraw')
    elif delay_dist_type == 'uniform':
        d_dist = RandomDistribution('uniform', [d_mean - d_sd, d_mean + d_sd], rng=rng)

    if w_mean > 0:
        w_dist = RandomDistribution('normal', [w_mean, w_sd], rng=rng, \
                 boundaries=(0., np.inf), constrain='redraw')
    else:
        w_dist = RandomDistribution('normal', [w_mean, w_sd], rng=rng, \
                 boundaries=(-np.inf, 0.), constrain='redraw')

    connector = sim.MultapseConnector(num_synapses=n_syn, weights=w_dist, delays=d_dist)
    proj = sim.Projection(pop1, pop2, connector, target=conn_type, rng=rng)

    if save_connections:
        proj.saveConnections(system_params['conn_dir'] + '/' + pop1.label \
                             + "_" + pop2.label + '.conn', gather=True)


def ConnectWithoutMultapses(sim, pop1, pop2, K, w_mean, w_sd, d_mean, d_sd, conn_type, rng):
    """Connects two populations approximating multapses as single synapses with increased weights.
       Differs from actual multapses in that the delays of the different connections are equal."""

    if not K:
        return

    l1 = len(pop1)
    l2 = len(pop2)

    if simulator != 'hardware.brainscales':
        if delay_dist_type == 'normal':
            d_dist = RandomDistribution('normal', [d_mean, d_sd], rng=rng, \
                boundaries=(simulator_params[simulator]['min_delay'], \
                simulator_params[simulator]['max_delay']), constrain='redraw')
        elif delay_dist_type == 'uniform':
            d_dist = RandomDistribution('uniform', [d_mean - d_sd, d_mean + d_sd], rng=rng)

    if w_mean > 0:
        w_dist = RandomDistribution('normal', [w_mean, w_sd], rng=rng, \
             boundaries=(0., np.inf), constrain='redraw')
    else:
        w_dist = RandomDistribution('normal', [w_mean, w_sd], rng=rng, \
             boundaries=(-np.inf, 0.), constrain='redraw')

    # expected number of single synapses
    n_syn = K * l2
    # probability of at least one connection between a given neuron pair
    p = 1. - (1. - 1. / (l1 * l2))**n_syn
    # Determine the largest expected multapse degree
    q = 1 - 1. / (l1 * l2)
    rv = stats.binom(n_syn, 1. / (l1 * l2))
    max_multapse_degree = int(rv.ppf(q)) + 1

    # number of connections consisting of one or more synapses
    n_conn = int(round(p * l1 * l2))

    # array of synaptic weights
    # mask_local=False ensures that the total nr of weights is drawn on each process
    w_array = w_dist.next(n_conn, mask_local=False)

    j=0
    for i in xrange(2, max_multapse_degree):
        n_syn_this_degree = int(round(stats.binom.pmf( \
                                i, n_conn, 1. / (l1 * l2)) * n_conn))
        # for each multapse degree, draw an appropriate number of additional
        # weights and add them to the existing ones
        for k in xrange(i-1):
            w_array[j:j+n_syn_this_degree] += w_dist.next(n_syn_this_degree, \
                                                          mask_local=False)
        j += n_syn_this_degree

    # simulate multiplicative noise on the weights present in the neuromorphic hardware
    if simulator != 'hardware.brainscales':
        if w_noise:
            w_noise_dist = RandomDistribution( \
                           'normal', w_noise, rng=rng, \
                           boundaries=(0, np.inf), constrain='redraw')
            noise = w_noise_dist.next(n_conn, mask_local=False)
            w_array *= noise

    # shuffle weight array
    random.shuffle(w_array)

    # draw delays
    if simulator == 'hardware.brainscales':
        d_array = np.empty(n_conn)
    else:
        d_array = d_dist.next(n_conn, mask_local=False)

    # draw pre- and postsynaptic neurons, avoiding multapses
    a = np.arange(l1 * l2).reshape(l1, l2)
    grid = np.indices(a.shape)
    idx = zip( grid[0].ravel(), grid[1].ravel() )
    np.random.shuffle(idx)
    pairs = np.transpose(idx[0:n_conn])

    # establish connections
    conn_list = np.transpose(np.vstack((pairs, w_array, d_array)))
    connector = sim.FromListConnector(conn_list)
    proj = sim.Projection(pop1, pop2, connector, target=conn_type)

    if save_connections:
        proj.saveConnections(system_params['conn_dir'] + '/' + pop1.label + \
                             "_" + pop2.label + '.conn', gather=True)


def FromListConnect(sim, pop1, pop2, conn_type, base_neuron_ids):
    """Establish connections based on data read from file"""
    connections = list()
    for filename in os.listdir(system_params['conn_dir']):
        if filename.startswith(pop1.label + "_" + pop2.label):
            print "Reading {}".format(filename)
            f = open(os.path.join(system_params['conn_dir'], filename))
            in_comment_bracket = False
            for line in f:
                if line.startswith("#"):
                    if "[" in line:
                        in_comment_bracket = True
                if not line.startswith("#"):
                    if in_comment_bracket:
                        if "]" in line:
                            in_comment_bracket = False
                    else:
                        line = line.strip()
                        (source_id, target_id, weight, delay) = line.split()
                        source_id = int(math.floor(float(source_id))) - base_neuron_ids[pop1]
                        target_id = int(math.floor(float(target_id))) - base_neuron_ids[pop2]
                        if source_id < 0 or target_id < 0:
                            print line, base_neuron_ids[pop1], base_neuron_ids[pop2]
                        connections.append((source_id, target_id,
                                float(weight) / 1000.0, float(delay)))
            f.close()
    if len(connections) > 0:
        connector = sim.FromListConnector(conn_list=connections)
        sim.Projection(pop1, pop2, connector, target=conn_type)
