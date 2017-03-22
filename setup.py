from setuptools import setup
from spynnaker7.pyNN._version import __version__

exec (open("spynnaker/pyNN/_version.py").read())

setup(
    name="sPyNNaker",
    version=__version__,
    description="Spinnaker implementation of PyNN 0.7",
    url="https://github.com/SpiNNakerManchester/SpyNNaker7",
    packages=['spynnaker7',
              'spynnaker7.pyNN',
              'spynnaker7.pyNN.models',
              'spynnaker7.pyNN.models.connectors',
              'spynnaker7.pyNN.utilities',
              'spynnaker7.pyNN.utilities.conf',
              'spynnaker7.pyNN.utilities.random_stats'],
    install_requires=[
        'SpiNNFrontEndCommon >= 3.0.0, < 4.0.0', 'sPyNNaker'
        'pyNN >= 0.7, < 0.8', 'numpy',
        'scipy', 'lxml', 'six', 'bitarray']
)
