from pyNN.recording import files
from spynnaker.pyNN.models.neural_projections.connectors.from_file_connector \
    import FromFileConnector as CommonFromFileConnector


class FromFileConnector(CommonFromFileConnector):
    def __init__(
            self, file, distributed=False, safe=True, verbose=False):
        CommonFromFileConnector.__init__(
            self, file=None, distributed=distributed, safe=safe,
            verbose=verbose)

    def get_reader(self, file):
        """
        get a filereader object using the pynn methods

        :return: A pynn StandardTextFile or similar
        """
        return files.StandardTextFile(file, mode="r")
