FlowUtils API
===================================

FlowUtils includes 2 modules: :code:`compensate` and :code:`transforms`
containing functions for compensation and various transforms, respectively.

compensate Module
-----------------

The :code:`compensate` module includes functions for parsing the spillover
keyword value from the metadata within an FCS file, creating a compensation
from CSV or NumPy input types, and for applying a compensation matrix to
FCS event data (as a NumPy array).

.. toctree::
   :maxdepth: 2

   compensate functions <compensate>

transforms Module
-----------------

The :code:`transforms` module includes functions for applying various
transformations (and their inverse) to FCS event data that are commonly used within the
flow cytometry community. These include:

- Logarithmic
- Inverse hyperbolic sine (asinh)
- Logicle
- Hyperlog

.. toctree::
   :maxdepth: 2

   transforms functions <transforms>
