MSMetaEnhancer package
======================

The Application class serves as a top-level interface to use the tool.

The main method is (asynchronous) `annotate_spectra`, which runs the annotation
process using given conversions. It is possible to specify particular conversion jobs,
which will be executed in respecting the given order. If no jobs are given, all
jobs supported by given services are used.

Additionally, it allows to load and save spectra files in supported formats, and curate given spectra.

.. automodule:: MSMetaEnhancer.app
   :members:
   :undoc-members:
   :show-inheritance:

Converters
----------

.. toctree::

   MSMetaEnhancer.libs.webConverters
   MSMetaEnhancer.libs.computeConverters

Data representation
-------------------

.. toctree::

   MSMetaEnhancer.libs.data

Utils
-----

.. toctree::

    MSMetaEnhancer.libs.utils

Libs
----

.. toctree::

    MSMetaEnhancer.libs