import spynnaker7.pyNN as sim
import numpy
import pylab


# -------------------------------------------------------------------
# This example uses the sPyNNaker implementation of the inhibitory
# Plasticity rule developed by Vogels, Sprekeler, Zenke et al (2011)
# To reproduce the experiment from their paper
# -------------------------------------------------------------------
# Population parameters
model = sim.IF_curr_exp
cell_params = {
    'cm': 0.2,         # nF
    'i_offset': 0.2,
    'tau_m': 20.0,
    'tau_refrac': 5.0,
    'tau_syn_E': 5.0,
    'tau_syn_I': 10.0,
    'v_reset': -60.0,
    'v_rest': -60.0,
    'v_thresh': -50.0}


# How large should the population of excitatory neurons be?
# (Number of inhibitory neurons is proportional to this)
NUM_EXCITATORY = 2000

# Reduce number of neurons to simulate on each core
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)


# Function to build the basic network - dynamics should be a PyNN synapse
# dynamics object
def build_network(dynamics):
    # SpiNNaker setup
    sim.setup(timestep=1.0, min_delay=1.0, max_delay=10.0)

    # Create excitatory and inhibitory populations of neurons
    ex_pop = sim.Population(NUM_EXCITATORY, model, cell_params)
    in_pop = sim.Population(NUM_EXCITATORY / 4, model, cell_params)

    # Record excitatory spikes
    ex_pop.record()

    # Make excitatory->inhibitory projections
    sim.Projection(ex_pop, in_pop,
                   sim.FixedProbabilityConnector(0.02, weights=0.03),
                   target='excitatory')
    sim.Projection(ex_pop, ex_pop,
                   sim.FixedProbabilityConnector(0.02, weights=0.03),
                   target='excitatory')

    # Make inhibitory->inhibitory projections
    sim.Projection(in_pop, in_pop,
                   sim.FixedProbabilityConnector(0.02, weights=-0.3),
                   target='inhibitory')

    # Make inhibitory->excitatory projections
    ie_projection = sim.Projection(
        in_pop, ex_pop, sim.FixedProbabilityConnector(0.02, weights=0),
        target='inhibitory', synapse_dynamics=dynamics)

    return ex_pop, ie_projection


# Build static network
static_ex_pop, _ = build_network(None)

# Run for 1s
sim.run(1000)

# Get static spikes and save to disk
static_spikes = static_ex_pop.getSpikes(compatible_output=True)

# Build inhibitory plasticity  model
stdp_model = sim.STDPMechanism(
    timing_dependence=sim.extra_models.Vogels2011Rule(alpha=0.12, tau=20.0),
    weight_dependence=sim.AdditiveWeightDependence(w_min=0.0, w_max=1.0,
                                                   A_plus=0.05),
    mad=True)

# Build plastic network
plastic_ex_pop, plastic_ie_projection = build_network(
    sim.SynapseDynamics(slow=stdp_model))

# Run simulation
sim.run(10000)

# Get plastic spikes and save to disk
plastic_spikes = plastic_ex_pop.getSpikes(compatible_output=True)
numpy.save("plastic_spikes.npy", plastic_spikes)

plastic_weights = plastic_ie_projection.getWeights(format="array")
mean_weight = numpy.average(plastic_weights)
print "Mean learnt ie weight:%f" % mean_weight

# Create plot
fig, axes = pylab.subplots(3)

# Plot last 200ms of static spikes (to match Brian script)
axes[0].set_title("Excitatory raster without inhibitory plasticity")
axes[0].scatter(static_spikes[:, 1], static_spikes[:, 0], s=2, color="blue")
axes[0].set_xlim(800, 1000)
axes[0].set_ylim(0, NUM_EXCITATORY)

# Plot last 200ms of plastic spikes (to match Brian script)
axes[1].set_title("Excitatory raster with inhibitory plasticity")
axes[1].scatter(plastic_spikes[:, 1], plastic_spikes[:, 0], s=2, color="blue")
axes[1].set_xlim(9800, 10000)
axes[1].set_ylim(0, NUM_EXCITATORY)

# Plot rates
binsize = 10
bins = numpy.arange(0, 10000 + 1, binsize)
plastic_hist, _ = numpy.histogram(plastic_spikes[:, 1], bins=bins)
plastic_rate = plastic_hist * (1000.0/binsize) * (1.0/NUM_EXCITATORY)
axes[2].set_title("Excitatory rates with inhibitory plasticity")
axes[2].plot(bins[0:-1], plastic_rate, color="red")
axes[2].set_xlim(9800, 10000)
axes[2].set_ylim(0, 20)

# Show figures
pylab.show()

# End simulation on SpiNNaker
sim.end()
