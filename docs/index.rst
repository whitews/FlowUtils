.. FlowUtils documentation master file

FlowUtils Documentation
=======================

.. image:: https://img.shields.io/pypi/v/flowutils.svg?colorB=dodgerblue
    :target: https://pypi.org/project/flowutils/

.. image:: https://img.shields.io/pypi/l/flowutils.svg?colorB=green
    :target: https://pypi.python.org/pypi/flowutils/

.. image:: https://img.shields.io/pypi/pyversions/flowutils.svg
    :target: https://pypi.org/project/flowutils/

FlowUtils is a Python package containing utility functions related
to flow cytometry analysis. Primarily focused on the commonly used
tasks of compensation and transformation, FlowUtils aims to be a
stable and reliable source with minimal dependencies.

It is part of a suite of Python cytometry libraries, which also
include FlowIO and FlowKit. The
`FlowIO library <https://github.com/whitews/FlowIO>`_
reads and writes Flow Cytometry Standard (FCS) files, and has zero
dependencies. For higher level interaction with flow cytometry data,
including GatingML & FlowJo 10 support, see the related
`FlowKit project <https://github.com/whitews/FlowKit>`_.

Installation
------------

FlowUtils uses C extensions for significant performance improvements.
For the most common platforms and Python versions, pre-built binaries
are available in PyPI (and installable via pip). If a pre-built binary
of FlowUtils is not available for your environment, then the C
extensions must be compiled using the source package.

From PyPI
.........

.. code-block:: python

    pip install flowutils

From GitHub source code
.......................

.. code-block:: python

   git clone https://github.com/whitews/flowutils
   cd flowutils
   pip install .

----

API
---

* :ref:`genindex`

.. toctree::
   :maxdepth: 3

   api
