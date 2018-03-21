from distutils.core import setup, Extension
from numpy import get_include

logicle_extension = Extension(
    'flowutils.logicle_c',
    sources=[
        'flowutils/logicle_c_ext/_logicle.c',
        'flowutils/logicle_c_ext/logicle.c'
    ],
    include_dirs=[get_include()]
)

setup(
    name='FlowUtils',
    version='0.5',
    packages=['flowutils'],
    package_data={'': []},
    description='Flow Cytometry Standard Utilities',
    ext_modules=[logicle_extension],
    requires=[
        'numpy (>=1.7)',
        'scipy (>=0.12)'
    ]
)
