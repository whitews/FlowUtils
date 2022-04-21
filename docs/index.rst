.. FlowUtils documentation master file, created by
   sphinx-quickstart on Fri Oct 16.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FlowUtils Documentation
=======================

.. image:: https://img.shields.io/pypi/v/flowutils.svg?colorB=dodgerblue
    :target: https://pypi.org/project/flowutils/

.. image:: https://img.shields.io/pypi/l/flowutils.svg?colorB=green
    :target: https://pypi.python.org/pypi/flowutils/

.. image:: https://img.shields.io/pypi/pyversions/flowutils.svg
    :target: https://pypi.org/project/flowutils/

FlowUtils is a Python package containing various utility functions related
to flow cytometry analysis, primarily focused on compensation,
transformation, and gating tasks commonly used within the flow community.

FlowUtils is part of a suite of Python libraries for analyzing flow
cytometry data.  It was developed as an extension to the light-weight
[FlowIO library](https://github.com/whitews/FlowIO). FlowIO reads and
writes Flow Cytometry Standard (FCS) files, and has zero dependencies.
For higher level interaction with flow cytometry data, including
GatingML & FlowJo 10 support, see the related
[FlowKit project](https://github.com/whitews/FlowKit).

Installation
------------

**Note: FlowUtils uses C extensions for significant performance
improvements. For the most common platforms and Python versions, pre-built
binaries are available in PyPI (and installable via pip).**

**If a pre-built binary of FlowUtils is not available for your environment,
then the C extensions must be compiled using the source package. NumPy >=1.19
must be installed prior to compiling FlowUtils. If compiling using `gcc`, version 5 or later is required.**

From PyPI
.........

FlowUtils is available via the `pip` command. However, NumPy must be installed prior in order to
compile the C extensions.

.. code-block:: python

    pip install flowutils

From GitHub source code
.......................

.. code-block:: python

   pip install numpy>=1.19
   git clone https://github.com/whitews/flowutils
   cd flowutils
   python setup.py install

----

API
---

* :ref:`genindex`

.. toctree::
   :maxdepth: 3

   api
