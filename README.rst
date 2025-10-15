We are no longer actively maintaining this repository. All active work by the Allen Institute for Cell Science is located under the `AllenCell <https://github.com/AllenCell>`__ organization.

================
brightfield2fish
================


.. image:: https://travis-ci.com/AllenCellModeling/brightfield2fish.svg?branch=master
        :target: https://travis-ci.com/AllenCellModeling/brightfield2fish

.. image:: https://readthedocs.org/projects/brightfield2fish/badge/?version=latest
        :target: https://brightfield2fish.readthedocs.io/en/latest/?badge=latest
      
.. image:: https://codecov.io/gh/AllenCellModeling/brightfield2fish/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/AllenCellModeling/brightfield2fish


Translate brightfield images to and from FISH assay


* Free software: Allen Institute Software License

* Documentation: https://brightfield2fish.readthedocs.io.


Installation
------------

::

    $ conda create --name brightfield2fish python=3.7
    $ conda activate brightfield2fish
    $ cd brightfield2fish/
    $ pip install -e .[test]
    $ pip install -e .[dev]
    $ pre-commit install

