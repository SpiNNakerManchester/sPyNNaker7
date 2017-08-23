import spynnaker7.pyNN as p
import pylab


def test_izk_cond_exp_set():

    p.setup(1.0)

    pop = p.Population(1, p.extra_models.IZK_cond_exp, {"i_offset": 1.0})
    pop.record_v()

    p.run(100)

    pop.set("i_offset", 2.0)

    p.run(100)

    v = pop.get_v()

    p.end()

    return v


if __name__ == "__main__":
    v = test_izk_cond_exp_set()
    pylab.figure()
    pylab.plot([i[1] for i in v], [i[2] for i in v])
    pylab.ylabel('v/mV')
    pylab.xlabel('Time/ms')
    pylab.title('Membrane voltage')
    pylab.show()
