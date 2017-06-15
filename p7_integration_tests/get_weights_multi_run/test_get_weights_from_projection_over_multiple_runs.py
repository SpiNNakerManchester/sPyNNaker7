
class Test(object):

    def test(self):
        import spynnaker7.pyNN as p
        p.setup()
        p1 = p.Population(1, p.IF_curr_exp, {})
        p2 = p.Population(1, p.IF_curr_exp, {})

        proj = p.Projection(p1, p2, p.AllToAllConnector())

        p.run(500)

        x = proj.getWeights()

        p.run(500)

        y = proj.getWeights()

        p.end()



if __name__ == '__main__':
    x = Test()
    x.test()
