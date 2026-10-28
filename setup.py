"""
Setup script for the FlowUtils package
"""
from setuptools import setup, Extension
import sys
import numpy as np  # NumPy is needed to build C extensions

# read in version string
VERSION_FILE = 'src/flowutils/_version.py'
__version__ = None  # to avoid inspection warning and check if __version__ was loaded
exec(open(VERSION_FILE).read())

if __version__ is None:
    raise RuntimeError("__version__ string not found in file %s" % VERSION_FILE)

with open("README.md", "r") as fh:
    long_description = fh.read()

# NOTES ON C EXTENSIONS:
#
# On macOS, clang 14 and later introduced changes to
# Fused Multiply-Add (FMA). Prior to version 14, clang
# was less likely to use FMA. clang 14 began using FMA by
# default, resulting in numerical differences in some
# expressions. Specifically, the is_left() function in
# gate_helpers.c was affected and resulted in failed tests.
# To enforce consistency across platforms the compile
# flag '-ffp-contract=off' was added to disable FMA.
# This fixed the discrepancies on macOS.
#
# The exp10 extension was added to address 1-ULP inconsistencies
# in 10^x calculations needed for FCS pre-processing in FlowIO.

# Define cross-platform compiler architectures
if sys.platform == "win32":
    base_compile_args = ["-O2"]

    # NOTE: FlowUtils must use clang-cl to correctly compile the exp10 extension
    # /O2 optimizes speed safely
    # Use strict rounding
    core_math_compile_args = ["-O2", "-frounding-math"]
    libs = []
else:
    # GCC/Clang Flags: Disable FMA explicitly to handle the macOS Clang 14+ drift
    base_compile_args = ["-std=gnu99", "-ffp-contract=off"]
    # Add strict rounding tracking for CORE-MATH
    core_math_compile_args = ["-std=gnu99", "-O3", "-frounding-math"]
    libs = ["m"]  # Link math library on Unix/Linux/macOS

exp10_extension = Extension(
    "flowutils.exp10_c",
    sources=[
        "src/flowutils/core_math_ext/_exp10.c",     # Your C-API wrapper
        "src/flowutils/core_math_ext/exp10.c"       # The pristine CORE-MATH source file
    ],
    include_dirs=[np.get_include(), 'src/flowutils/core_math_ext'],
    extra_compile_args=core_math_compile_args,
    libraries=libs
)

logicle_extension = Extension(
    'flowutils.logicle_c',
    sources=[
        'src/flowutils/logicle_c_ext/_logicle.c',
        'src/flowutils/logicle_c_ext/logicle.c'
    ],
    include_dirs=[np.get_include(), 'src/flowutils/logicle_c_ext'],
    extra_compile_args=base_compile_args,
    libraries=libs
)

gating_extension = Extension(
    'flowutils.gating_c',
    sources=[
        'src/flowutils/gating_c_ext/_gate_helpers.c',
        'src/flowutils/gating_c_ext/gate_helpers.c'
    ],
    include_dirs=[np.get_include(), 'src/flowutils/gating_c_ext'],
    extra_compile_args=base_compile_args,
    libraries=libs
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
    ext_modules=[exp10_extension, logicle_extension, gating_extension],
    install_requires=['numpy>=2.0,<3.0'],
    classifiers=[
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10'
    ]
)
