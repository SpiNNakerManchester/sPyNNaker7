import spynnaker7.pyNN as p
import plot_utils

p.setup(0.1)
runtime = 500
populations = []

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [5, 10, 15, 20, 25, 395]
                                         }, label="src1")
pop_src2 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [360, 365, 370, 375, 380]
                         }, label="src2")

# cell_params = {
#         'a': 0.01, 'c': -65.0, 'b': 0.2, 'd': 8.0, 'i_offset': 3.83,
#         'u_init': -14.0, 'v_init': -70.0}
cell_params = {
    'exc_a_tau': 1.235, 'exc_b_tau': 1.3585, # AMPA
        'exc2_a_tau': 18.5227, 'exc2_b_tau': 20.3750} # NMDA

pop_ex = p.Population(1, p.extra_models.IF_curr_comb_exp_3E3I, cell_params,  label="test")

# define projections
exc_proj0 = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=2, delays=1), target="excitatory")
# exc_proj1 = p.Projection(pop_src1, pop_ex,
#         p.OneToOneConnector(weights=2, delays=1), target="excitatory2")
exc_proj2 = p.Projection(pop_src2, pop_ex,
        p.OneToOneConnector(weights=1, delays=1), target="excitatory2")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()

p.run(runtime)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)

p.end()