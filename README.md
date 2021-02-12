# FlowUtils

[![PyPI license](https://img.shields.io/pypi/l/flowutils.svg?colorB=dodgerblue)](https://pypi.python.org/pypi/flowutils/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/flowutils.svg)](https://pypi.python.org/pypi/flowutils/)
[![PyPI version](https://img.shields.io/pypi/v/flowutils.svg?colorB=blue)](https://pypi.python.org/pypi/flowutils/)

[![Build Status](https://travis-ci.com/whitews/FlowUtils.svg?branch=master)](https://travis-ci.com/whitews/FlowUtils)
[![Coverage](https://codecov.io/gh/whitews/FlowUtils/branch/master/graph/badge.svg)](https://codecov.io/gh/whitews/flowutils)
[![Documentation Status](https://readthedocs.org/projects/flowutils/badge/?version=latest)](https://flowutils.readthedocs.io/en/latest/?badge=latest)

FlowUtils is a Python package containing various utility functions related
to flow cytometry analysis, primarily focused on compensation and
transformation tasks commonly used within the flow community.

FlowUtils is part of a suite of Python libraries for analyzing flow 
cytometry data.  It was developed as an extension to the light-weight 
[FlowIO library](https://github.com/whitews/FlowIO). FlowIO reads and 
writes Flow Cytometry Standard (FCS) files, and has zero dependencies. 
For higher level interaction with flow cytometry data, including 
GatingML & FlowJo 10 support, see the related 
[FlowKit project](https://github.com/whitews/FlowKit).

## Installation

FlowUtils implements several transformation functions as C extensions
for increased performance on large arrays of FCS event data. **NumPy is
required to compile these C extensions prior to installing FlowUtils.**

### From PyPI

FlowUtils is available via the `pip` command. However, NumPy must be installed prior in order to
compile the C extensions.

```
pip install numpy
pip install flowutils
```

### From GitHub source code

```
pip install numpy

git clone https://github.com/whitews/flowutils
cd flowutils

python setup.py install
```
