import spynnaker7.pyNN as p
import plot_utils

p.setup(0.1)
runtime = 1000
populations = []

num_pulses = 10
wavelength = 500 #ms
amplitude = 2

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [105, 106, 107 ,108, 109, 110, 111, 112]#, 110, 115, 120, 125, 1450]#, 485]
                                         }, label="src1")
pop_src2 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [105]#, 465, 470, 475, 480]# 750,755,760,765, 766, 767, 768]
                         }, label="src2")

cell_params = { # L_V_Py
                       'a': 0.111, 'c': -65.0, 'b': 0.2, 'd': 2.0, 'i_offset': 3.97,
        'u_init': -14.0, 'v_init': -70.0,

        'exc_a_tau':  0.5,  'exc_b_tau': 2.4, # Spike source
        'exc2_a_tau': 3.25, 'exc2_b_tau': 3.575,  # 5-HT2A
        'exc3_a_tau': 0.5, 'exc3_b_tau': 2.4, # AMPA
        'exc4_a_tau': 4, 'exc4_b_tau': 40, # NMDA

        'inh_a_tau':  1, 'inh_b_tau':  7, # Spike source
        'inh2_a_tau': 1, 'inh2_b_tau': 7, # Recurrent - pseudo GABA
        'inh3_a_tau': 210, 'inh3_b_tau': 231, # 5-HT1A
        'inh4_a_tau': 60, 'inh4_b_tau': 200 # GABA_B
}

pop_ex = p.Population(1, p.extra_models.IZK_curr_comb_exp_4E4I, cell_params,  label="test")
print pop_ex.get('i_offset')
# define projections
exc_proj0 = p.Projection(pop_src2, pop_ex,
        p.OneToOneConnector(weights=1, delays=100), target="inhibitory3")

# exc_proj1 = p.Projection(pop_src1, pop_ex,
#         p.OneToOneConnector(weights=200, delays=50), target="inhibitory4")

# # NMDA synapse
# exc_proj2 = p.Projection(pop_src2, pop_ex,
#         p.OneToOneConnector(weights=0.2, delays=1), target="excitatory4")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()

for i in range(num_pulses):
    p.run(wavelength/2)
    pop_ex.set('i_offset', pop_ex.get('i_offset') + amplitude)
    p.run(wavelength/2)
    pop_ex.set('i_offset', pop_ex.get('i_offset') - amplitude)



v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)

p.end()