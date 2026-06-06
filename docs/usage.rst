Usage Guide
===========

Vjer is a command-line tool installed as the `vjer` entry point.

Getting started
---------------

Install Vjer into a Python environment before building the docs locally:

.. code-block:: console

   python -m pip install -U .
   python -m pip install -r docs/requirements.txt

Once installed, run Vjer from your virtual environment:

.. code-block:: console

   vjer test

Basic usage
-----------

The Vjer entry point is designed for action-driven automation:

- `vjer test`
- `vjer build`
- `vjer deploy`
- `vjer rollback`
- `vjer pre_release`
- `vjer release`
- `vjer freeze`

Learn more:

- :doc:`cli_reference`
- :doc:`actions`
- :doc:`configuration`
