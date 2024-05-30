consoil
==========

|PyPI| |Documentation Status| |PyPI - License|

A Python package to calculate consolidation of sediment particles in soil suspensions. The code is being developed by `Ismail Myouri` 
for the MUDNET group at Delft Technical University and DELTARES, The Netherlands. 
The **consoil** package can be used under the conditions of the GPLv3 license.

Features
--------

* Basic classes for sedimentation.


Installation
------------

To use the package `consoil`, install it in a Python environment:

.. code-block:: console

    (env) pip install consoil

or

.. code-block:: console

    (env) conda install consoil

This should
automatically install the dependency packages ``matplotlib`` , ``scipy``
and ``pandas``, if they haven't been installed already. If you are
installing by hand, ensure that these packages are installed as well.

Example use
-----------

.. code:: python

   import numpy as np

   from consoil.constants import *
   from consoil import *

   import matplotlib
   import matplotlib.pyplot as plt
   from pathlib import Path

   matplotlib.use("Qt5Agg")
   DATADIR = Path(__file__).parent


consoil pages
----------------

-  `PyPi <https://pypi.org/project/consoil/>`__: consoil Python package
-  `BitBucket <https://bitbucket.org/deltares/consoil/>`__: consoil source code
-  `ReadTheDocs <https://consoil.readthedocs.io/>`__: consoil documentation

Author and license
------------------

-  Author: Ismail Myouri
-  Contact: i.myouri@tudelft.nl
-  License: `GPLv3 <https://www.gnu.org/licenses/gpl.html>`__

References
----------

-  ...

.. |PyPi| image:: https://img.shields.io/pypi/v/consoil
   :alt: PyPI

.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/consoil
   :alt: PyPI - Downloads

.. |PyPi Status| image:: https://img.shields.io/pypi/status/consoil
   :alt: PyPI - Status

.. |Documentation Status| image:: https://readthedocs.org/projects/dielectric/badge/?version=latest
   :target: https://edumud.readthedocs.io/en/latest/?badge=latest

.. |PyPI - License| image:: https://img.shields.io/pypi/l/consoil
   :alt: PyPI - License