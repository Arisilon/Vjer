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
- `pre_release` — run release preparation steps using the `release` section.
- `release` — run release steps using the `release` section.
- `freeze` — create a frozen requirements file from the root `requirements.txt`.

Running actions
---------------

Use the `vjer` entry point followed by an action name:

.. code-block:: console

   vjer <action>

The `build` action creates artifacts and documentation according to the `build` section.
The `release` and `pre_release` actions both use the `release` section. `pre_release`
commonly prepares pre-release artifacts and version metadata, while `release` performs the
final publish and tag actions.

Freeze action
-------------

The `freeze` action is not driven by `vjer.yml`. It reads the root `requirements.txt`
file, builds a temporary virtual environment, installs the requirements, and writes a frozen
requirements file named `requirements-frozen.txt` or `requirements-frozen-<suffix>.txt`.

Action configuration
--------------------

Action behavior is driven by the matching section in `vjer.yml`.
For example, `vjer build` runs the steps defined under `build.steps`, and `vjer test`
runs the steps defined under `test.steps`.

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

   release:
     steps:
       - type: pypi
         test_pypi: true
         username: __token__
         password: "{var:PYPI_TOKEN}"
       - type: increment_release
