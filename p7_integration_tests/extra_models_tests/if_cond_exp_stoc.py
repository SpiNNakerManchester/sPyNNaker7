"""
A single IF neuron with exponential, current-based synapses, fed by two
spike sources.

Run as:

$ python IF_curr_exp.py <simulator>

where <simulator> is 'neuron', 'nest', etc

Andrew Davison, UNIC, CNRS
September 2006

$Id$
"""

import pylab
import spynnaker7.pyNN as sim

sim.setup(timestep=1.0, min_delay=1.0, max_delay=4.0)

stoc_cell = sim.Population(1, sim.extra_models.IF_cond_exp_stoc, {
    'i_offset': 0.1,
    'tau_refrac': 3.0,
    'v_thresh': -51.0,
    'v_reset': -70.0,
    'tau_syn_E': 5.0,
    'tau_syn_I': 5.0})

exp_cell = sim.Population(1, sim.IF_cond_exp, {
    'i_offset': 0.1,
    'tau_refrac': 3.0,
    'v_thresh': -51.0,
    'v_reset': -70.0,
    'tau_syn_E': 5.0,
    'tau_syn_I': 5.0})


spike_sourceE = sim.Population(1, sim.SpikeSourceArray, {
    'spike_times': [float(i) for i in range(5, 105, 10)]})
spike_sourceI = sim.Population(1, sim.SpikeSourceArray, {
    'spike_times': [float(i) for i in range(155, 255, 10)]})

sim.Projection(spike_sourceE, exp_cell,
               sim.OneToOneConnector(weights=0.15, delays=2.0),
               target='excitatory')
sim.Projection(spike_sourceI, exp_cell,
               sim.OneToOneConnector(weights=-0.15, delays=4.0),
               target='inhibitory')
sim.Projection(spike_sourceE, stoc_cell,
               sim.OneToOneConnector(weights=0.15, delays=2.0),
               target='excitatory')
sim.Projection(spike_sourceI, stoc_cell,
               sim.OneToOneConnector(weights=-0.15, delays=4.0),
               target='inhibitory')

stoc_cell.record_gsyn()
exp_cell.record_gsyn()
stoc_cell.record_v()
exp_cell.record_v()
stoc_cell.record()
exp_cell.record()

sim.run(200.0)

v_delta = stoc_cell.get_v()
i_delta = stoc_cell.get_gsyn()
v_exp = exp_cell.get_v()
i_exp = exp_cell.get_gsyn()

# Plot
fig, axis = pylab.subplots(2)

axis[0].plot(v_delta[:, 1], v_delta[:, 2], label="Stochastic")
axis[0].plot(v_exp[:, 1], v_exp[:, 2], label="Static")
axis[0].set_title("Voltage")
axis[0].legend()

axis[1].plot(i_delta[:, 1], i_delta[:, 2], label="Stochastic")
axis[1].plot(i_exp[:, 1], i_exp[:, 2], label="Static")
axis[1].set_title("Current")
axis[1].legend()

sim.end()
pylab.show()
