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
to flow cytometry analysis, primarily focused on compensation and
transformation tasks commonly used within the flow community. The FlowUtils
package is part of a suite of Python libraries for analyzing flow
cytometry data, and was developed as an extension to the light-weight
[FlowIO library](https://github.com/whitews/FlowIO). FlowIO reads and
writes Flow Cytometry Standard (FCS) files, and has zero dependencies.
For higher level interaction with flow cytometry data, including
GatingML & FlowJo 10 support, see the related
[FlowKit project](https://github.com/whitews/FlowKit).

Installation
------------

FlowUtils implements several transformation functions as C extensions
for increased performance on large arrays of FCS event data. **NumPy is
required to compile these C extensions prior to installing FlowUtils.**

From PyPI
.........

FlowUtils is available via the `pip` command. However, NumPy must be installed prior in order to
compile the C extensions.

.. code-block:: python

    pip install numpy
    pip install flowutils

From GitHub source code
.......................

.. code-block:: python

   pip install numpy
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
