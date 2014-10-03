from distutils.core import setup
from numpy import get_include
from Cython.Distutils import Extension
from Cython.Distutils import build_ext

logicle_extension = Extension(
    'flowutils._logicle',
    sources=['flowutils/logicle_ext/%s' % i for i in [
        'Logicle.cpp',
        'my_logicle.cpp',
        'my_logicle_wrapper.cpp']
    ],
    include_dirs=[get_include()]
)

setup(
    name='FlowUtils',
    version='0.2',
    packages=['flowutils'],
    package_data={'': []},
    description='Flow Cytometry Standard Utilities',
    cmdclass={'build_ext': build_ext},
    ext_modules=[logicle_extension],
    requires=[
        'numpy (==1.7.1)',
        'scipy (==0.12)',
        'Cython (==0.18)'],
)
