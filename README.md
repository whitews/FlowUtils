# FlowUtils

[![PyPI license](https://img.shields.io/pypi/l/flowutils.svg?colorB=dodgerblue)](https://pypi.python.org/pypi/flowutils/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/flowutils.svg)](https://pypi.python.org/pypi/flowutils/)
[![PyPI version](https://img.shields.io/pypi/v/flowutils.svg?colorB=blue)](https://pypi.python.org/pypi/flowutils/)
[![DOI](https://zenodo.org/badge/15146734.svg)](https://zenodo.org/badge/latestdoi/15146734)

[![Build & test (master)](https://github.com/whitews/FlowUtils/actions/workflows/tests_master.yml/badge.svg)](https://github.com/whitews/FlowUtils/actions/workflows/tests_master.yml)
[![Build & test (develop)](https://github.com/whitews/FlowUtils/actions/workflows/tests_develop.yml/badge.svg)](https://github.com/whitews/FlowUtils/actions/workflows/tests_develop.yml)
[![Coverage](https://codecov.io/gh/whitews/FlowUtils/branch/master/graph/badge.svg)](https://codecov.io/gh/whitews/flowutils)
[![Documentation Status](https://readthedocs.org/projects/flowutils/badge/?version=latest)](https://flowutils.readthedocs.io/en/latest/?badge=latest)

FlowUtils is a Python package containing utility functions related
to flow cytometry analysis, primarily focused on compensation,
transformation, and gating tasks commonly used within the flow community.

FlowUtils is part of a suite of Python libraries for analyzing flow 
cytometry data.  It was developed as an extension to the light-weight 
[FlowIO library](https://github.com/whitews/FlowIO). FlowIO reads and 
writes Flow Cytometry Standard (FCS) files, and has minimal dependencies. 
For higher level interaction with flow cytometry data, including GatingML 
& FlowJo 10 support, see the related 
[FlowKit project](https://github.com/whitews/FlowKit).

## Installation

FlowUtils uses C extensions for significant performance improvements.
For the most common platforms and Python versions, pre-built binaries
are available in PyPI (and installable via pip). If a pre-built binary
of FlowUtils is not available for your environment, then the C
extensions must be compiled using the source package.

### From PyPI

```
pip install flowutils
```

### From GitHub source code

```
git clone https://github.com/whitews/flowutils
cd flowutils
pip install .
```

## Documentation

[API Documentation is available here.](https://flowutils.readthedocs.io/en/latest/?badge=latest)
