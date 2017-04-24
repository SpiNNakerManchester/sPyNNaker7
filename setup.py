import os
from setuptools import setup
from collections import defaultdict

exec(open("spynnaker7/pyNN/_version.py").read())

if os.environ.get('READTHEDOCS', None) == 'True':
    # scipy must be added in config.py as a mock
    install_requires = ['sPyNNaker >= 3.0.0, < 4.0.0',
                        'pyNN >= 0.7, < 0.8',
                        'numpy', 'lxml', 'six', 'bitarray']
else:
    install_requires = ['sPyNNaker >= 3.0.0, < 4.0.0',
                        'pyNN >= 0.7, < 0.8',
                        'numpy', 'scipy', 'lxml', 'six', 'bitarray']

# Build a list of all project modules, as well as supplementary files
main_package = "spynnaker7"
data_extensions = {".aplx", ".xml", ".json", ".xsd"}
config_extensions = {".cfg", ".template"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in data_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append("*{}".format(ext))
            break
        if ext in config_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append(filename)

setup(
    name="sPyNNaker7",
    version=__version__,
    description="Extensions of Spinnaker implementation specific for PyNN7",
    url="https://github.com/SpiNNakerManchester/SpyNNaker7",
    packages=packages,
    package_data=package_data,
    install_requires=install_requires
)
