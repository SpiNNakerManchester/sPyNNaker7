from p7_integration_tests.base_test_case import BaseTestCase
from testfixtures import LogCapture
import spynnaker7.pyNN as p


class TestGetWeightsAfterRuns(BaseTestCase):

    def test_run(self):
        with LogCapture() as l:
            p.setup()
            p1 = p.Population(1, p.IF_curr_exp, {})
            p2 = p.Population(1, p.IF_curr_exp, {})

            proj = p.Projection(p1, p2, p.AllToAllConnector())

            p.run(500)

            proj.getWeights()

            p.run(500)

            proj.getWeights()

            p.end()
            self.assert_logs_messages(
                l.records, "Getting weights", 'INFO', 2)


if __name__ == '__main__':
    x = TestGetWeightsAfterRuns()
    x.test_run()
