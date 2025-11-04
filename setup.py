"""
Setup script for the FlowUtils package
"""
from setuptools import setup, Extension
import numpy as np  # NumPy is needed to build C extensions

# read in version string
VERSION_FILE = 'src/flowutils/_version.py'
__version__ = None  # to avoid inspection warning and check if __version__ was loaded
exec(open(VERSION_FILE).read())

if __version__ is None:
    raise RuntimeError("__version__ string not found in file %s" % VERSION_FILE)

with open("README.md", "r") as fh:
    long_description = fh.read()

# NOTE ON C EXTENSIONS
# On MacOS, clang 14 and later introduced changes to
# Fused Multiply-Add (FMA). Prior to version 14, clang
# was less likely to use FMA. clang 14 began using FMA by
# default, resulting in numerical differences in some
# expressions. Specifically, the is_left() function in
# gate_helpers.c was affected and resulted in failed tests.
# To enforce consistency across platforms the compile
# flag '-ffp-contract=off' was added to disable FMA.
# This fixed the discrepancies on Mac OS.
logicle_extension = Extension(
    'flowutils.logicle_c',
    sources=[
        'src/flowutils/logicle_c_ext/_logicle.c',
        'src/flowutils/logicle_c_ext/logicle.c'
    ],
    include_dirs=[np.get_include(), 'src/flowutils/logicle_c_ext'],
    extra_compile_args=['-std=c99', '-ffp-contract=off']
)

gating_extension = Extension(
    'flowutils.gating_c',
    sources=[
        'src/flowutils/gating_c_ext/_gate_helpers.c',
        'src/flowutils/gating_c_ext/gate_helpers.c'
    ],
    include_dirs=[np.get_include(), 'src/flowutils/gating_c_ext'],
    extra_compile_args=['-std=c99',  '-ffp-contract=off']
)

setup(
    name='FlowUtils',
    version=__version__,  # noqa PyTypeChecker
    packages=['flowutils'],
    package_dir={'': "src"},
    package_data={'': []},
    description='Flow Cytometry Standard Utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Scott White',
    author_email='whitews@gmail.com',
    license='BSD',
    url="https://github.com/whitews/flowutils",
    ext_modules=[logicle_extension, gating_extension],
    install_requires=['numpy>=2.0,<3.0'],
    classifiers=[
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9'
    ]
)
