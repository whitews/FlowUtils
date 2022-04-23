.. FlowUtils documentation master file

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
`FlowIO library <https://github.com/whitews/FlowIO>`_. FlowIO reads and
writes Flow Cytometry Standard (FCS) files, and has zero dependencies.
For higher level interaction with flow cytometry data, including
GatingML & FlowJo 10 support, see the related
`FlowKit project <https://github.com/whitews/FlowKit>`_.

Installation
------------

FlowUtils uses C extensions for significant performance
improvements. For the most common platforms and Python versions, pre-built
binaries are available in PyPI (and installable via pip).

If a pre-built binary of FlowUtils is not available for your environment,
then the C extensions must be compiled using the source package. NumPy
must be installed prior to compiling these extensions. If compiling using gcc,
version 5 or later is required.

Compiling FlowUtils from source can also result in NumPy C API incompatibilities. See the `NumPy docs <https://numpy.org/devdocs/user/depending_on_numpy.html>`_ for more information.

From PyPI
.........

.. code-block:: python

    pip install flowutils

From GitHub source code
.......................

.. code-block:: python

   pip install numpy>=1.20
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
