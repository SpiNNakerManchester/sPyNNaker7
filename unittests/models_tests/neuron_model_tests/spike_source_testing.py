import spynnaker7.pyNN as p
import random
import numpy as np


def distance(x0, x1, grid=np.asarray([16, 16]), type='euclidian'):
    x0 = np.asarray(x0)
    x1 = np.asarray(x1)
    delta = np.abs(x0 - x1)
    delta = np.where(delta > grid * .5, delta - grid, delta)

    if type == 'manhattan':
        return np.abs(delta).sum(axis=-1)
    return np.sqrt((delta ** 2).sum(axis=-1))

def generate_rates(s, grid, f_base=5, f_peak=152.8, sigma_stim=2):
    '''
    Function that generates an array the same shape as the input layer so that
    each cell has a value corresponding to the firing rate for the neuron
    at that position.
    '''
    _rates = np.zeros(grid)

    for x in range(grid[0]):
        for y in range(grid[1]):
            _d = distance(s, (x, y), grid)
            _rates[x, y] = f_base + f_peak * np.e ** (
                -_d / (2 * (sigma_stim ** 2)))
    return _rates


timestep = 1
interval = 20
total_runtime = 15000 * interval
number_of_rates = total_runtime/interval
num_sources = 256
p.setup(timestep)



grid = np.asarray((1,256))
rates = []
max_locs = []
for i in range(number_of_rates):
    x = np.random.randint(0,256)
    max_locs.append(x)
    rate = generate_rates([1,x], grid)
    rates.append(list(rate[0]))

# for i in max_locs:
#     print i

# rates = []
# for i in range(number_of_rates):
#     c =  num_sources * [1]
#     c[random.randint(0,255)] = 200
#     rates.append(c)


# rate = [100, 200, 300] # (Hz) frequency of the random stimulation
# rates = [[10, 10, 500], [500, 10, 10], [10, 500, 10]]#, [10, 20, 500],  [10, 500, 10]]  # (Hz) frequency of the random stimulation
# total_runtime: make sure this is set to the end time of the simulation
# (or further, otherwise sources will stop making spikes)

# stim_dur = total_runtime/len(rate)   # (ms) duration of random stimulation

ext_stim = p.Population(
            num_sources, p.SpikeSourcePoissonVariable,
            {'rate_interval_duration': interval, 'rate': rates},
            label="expoisson")

exc_pop = p.Population(num_sources, p.IF_curr_exp, {})

p.Projection(ext_stim, exc_pop, p.OneToOneConnector(weights=2, delays=timestep))

recording = True
if recording:
    ext_stim.record()

# exc_pop.record()
# exc_pop.record_v()
# exc_pop.record_gsyn()

p.run(total_runtime)

# new_rate =  []
# for i in range(number_of_rates):
#     c =  num_sources * [1]
#     c[random.randint(0,255)] = 400
#     new_rate.append(c)
#
#
# ext_stim.set('rate', new_rate)
# p.run(total_runtime)

# spikes = exc_pop.getSpikes()
# v = exc_pop.get_v()
if recording:
    source_spikes = ext_stim.getSpikes()

    import pylab as plt
    def plot_spikes(spikes, title):
        if spikes is not None and len(spikes) > 0:
            f, ax1 = plt.subplots(1, 1, figsize=(16, 8))
            ax1.set_xlim((0, total_runtime))
            ax1.scatter([i[1] for i in spikes], [i[0] for i in spikes], s=.2)
            ax1.set_xlabel('Time/ms')
            ax1.set_ylabel('spikes')
            ax1.set_title(title)
            plt.show()

        else:
            print "No spikes received"


    plot_spikes(source_spikes, "SPIIIIKES!")
# plot_utils.plotAll(v, spikes)
p.end()