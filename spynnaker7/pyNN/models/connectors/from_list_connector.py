from spynnaker.pyNN.models.neural_projections.connectors \
    import FromListConnector as CommonFromListConnector
from spynnaker.pyNN.exceptions import InvalidParameterType
import numpy
import logging

logger = logging.getLogger(__name__)


class FromListConnector(CommonFromListConnector):
    """ Make connections according to a list.

    :param: conn_list:\
        a list of tuples, one tuple for each connection. Each\
        tuple should contain::

            (pre_idx, post_idx, weight, delay)

        where pre_idx is the index (i.e. order in the Population,\
        not the ID) of the presynaptic neuron, and post_idx is\
        the index of the postsynaptic neuron.
    """

    def __init__(self, conn_list, safe=True, verbose=False):
        """
        Creates a new FromListConnector.
        """
        # pylint: disable=len-as-condition
        # Disabled the warning because we might have a numpy array
        if conn_list is None or len(conn_list) == 0:
            raise InvalidParameterType(
                "The connection list for the FromListConnector must contain"
                " at least a list of tuples, each of which should contain:"
                " (pre_idx, post_idx, weight, delay)")

        conns, weights, delays, self._extra_conn_data = self._split_conn_list(
            conn_list, ['pre', 'post', 'weight', 'delay'])

        super(FromListConnector, self).__init__(conns, safe, verbose)
        self.set_weights_and_delays(weights, delays)

    @staticmethod
    def _split_conn_list(conn_list, column_names):
        """ Separate the connection list into the blocks needed.
        :param conn_list: the original connection list
        :param column_names: the column names if exist
        :return: source dest list, weights list, delays list, extra list
        """

        # weights and delay index
        weight_index = None
        delay_index = None

        # conn lists
        weights = None
        delays = None

        # locate weights and delay index in the listings
        if "weight" in column_names:
            weight_index = column_names.index("weight")
        if "delay" in column_names:
            delay_index = column_names.index("delay")
        element_index = list(range(2, len(column_names)))

        # figure out where other stuff is
        conn_list = numpy.array(conn_list)
        source_destination_conn_list = conn_list[:, [0, 1]]

        if weight_index is not None:
            element_index.remove(weight_index)
            weights = conn_list[:, weight_index]
        if delay_index is not None:
            element_index.remove(delay_index)
            delays = conn_list[:, delay_index]

        # build other data element conn list (with source and destination)
        other_conn_list = None
        other_element_column_names = list()
        for element in element_index:
            other_element_column_names.append(column_names[element])
        if element_index:
            other_conn_list = conn_list[:, element_index]
            other_conn_list.dtype.names = other_element_column_names

        # hand over split data
        return source_destination_conn_list, weights, delays, other_conn_list
