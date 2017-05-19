from distutils.core import setup
from numpy import get_include
from Cython.Distutils import Extension
from Cython.Distutils import build_ext

logicle_extension = Extension(
    'flowutils._logicle',
    sources=[
        'flowutils/logicle_ext/Logicle.cpp',
        'flowutils/logicle_ext/my_logicle.cpp',
        'flowutils/my_logicle_wrap.cxx'
    ],

    include_dirs=[get_include()]
)

setup(
    name='FlowUtils',
    version='0.4',
    packages=['flowutils'],
    package_data={'': []},
    description='Flow Cytometry Standard Utilities',
    cmdclass={'build_ext': build_ext},
    ext_modules=[logicle_extension],
    requires=[
        'numpy (>=1.7.1)',
        'scipy (>=0.12)',
        'Cython (>=0.18)'
    ]
)
