"""
Setup script for the FlowUtils package
"""
from setuptools import setup, Extension, dist

# NumPy is needed to build
# This retrieves a version at build time compatible with run time version
dist.Distribution().fetch_build_eggs(['numpy>=1.19'])

# override inspection for import not at top of file
# this has to be imported here, after fetching the NumPy egg
import numpy as np  # noqa: E402

with open("README.md", "r") as fh:
    long_description = fh.read()

logicle_extension = Extension(
    'flowutils.logicle_c',
    sources=[
        'flowutils/logicle_c_ext/_logicle.c',
        'flowutils/logicle_c_ext/logicle.c'
    ],
    include_dirs=[np.get_include(), 'flowutils/logicle_c_ext'],
    extra_compile_args=['-std=c99']
)

gating_extension = Extension(
    'flowutils.gating_c',
    sources=[
        'flowutils/gating_c_ext/_gate_helpers.c',
        'flowutils/gating_c_ext/gate_helpers.c'
    ],
    include_dirs=[np.get_include(), 'flowutils/gating_c_ext'],
    extra_compile_args=['-std=c99']
)

setup(
    name='FlowUtils',
    version='1.0.0b0',
    packages=['flowutils'],
    package_data={'': []},
    description='Flow Cytometry Standard Utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Scott White',
    author_email='whitews@gmail.com',
    license='BSD',
    url="https://github.com/whitews/flowutils",
    ext_modules=[logicle_extension, gating_extension],
    install_requires=['numpy>=1.19'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7'
    ]
)
