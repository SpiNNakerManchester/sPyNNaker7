import spynnaker7.pyNN as p


def test_direct_matrix():
    p.setup(timestep=1)
    pop_1 = p.Population(5, p.IF_curr_exp, {}, label="pop_1")
    input_pop = p.Population(
        5, p.SpikeSourceArray, {'spike_times': [0]}, label="input_pop")
    input_proj = p.Projection(
        input_pop, pop_1, p.OneToOneConnector(weights=5.0, delays=1),
        target="excitatory")
    input_proj_2 = p.Projection(
        input_pop, pop_1, p.AllToAllConnector(weights=4.0, delays=1))

    p.run(0)
    weights = input_proj.getWeights(format='list', gather=True)
    weights_2 = input_proj_2.getWeights(format='array', gather=True)
    p.end()

    # Check the one-to-one connection has 5 entries, each of which is 5
    assert len(weights) == 5
    assert all([weight == 5.0 for weight in weights])

    # Check the all-to-all connection matrix is 5x5, each value of which is 4
    assert len(weights) == 5
    assert all(len(weight_row) == 5 for weight_row in weights_2)
    assert all(
        [weight == 4.0 for weight_row in weights_2 for weight in weight_row])

    return weights, weights_2


if __name__ == "__main__":
    weights, weights_2 = test_direct_matrix()
    print weights
    print weights_2
