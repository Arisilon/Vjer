Actions Reference
=================

Vjer uses a single action argument to drive the automation pipeline.
Each action corresponds to a section in the project configuration and executes the configured steps for that phase.

Supported actions
-----------------

- `test` — run test steps from the `test` section.
- `build` — run build steps from the `build` section.
- `deploy` — run deploy steps from the `deploy` section.
- `rollback` — run rollback steps from the `rollback` section.
- `pre_release` — run release preparation steps from the `release` section.
- `release` — run release steps from the `release` section.
- `freeze` — run project freeze or locking steps.

Running actions
---------------

Use the `vjer` entry point followed by an action name:

.. code-block:: console

   vjer <action>

The `build` action may create artifacts and documentation as defined in your project config.
The `release` and `pre_release` actions are typically configured for publishing and tagging workflows.

Action configuration
--------------------

Action behavior is driven by the matching section in `vjer.yml`.
For example, `vjer build` runs the steps defined under the `build` section, and `vjer test` runs the steps defined under the `test` section.

Example
-------

.. code-block:: yaml

   test:
     steps:
       - type: flake8
       - type: pylint
       - type: mypy
       - type: python_unittest

   build:
     steps:
       - type: sphinx
         doc_type: cli
