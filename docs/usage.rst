Usage Guide
===========

Vjer is a command line tool for automating CI/CD tasks.

Getting started
---------------

Install Vjer into a Python environment before using it:

.. code-block:: console

   pip install vjer

Activate your virtual environment before running Vjer:

.. code-block:: console

   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate     # Windows

Run Vjer from the project root:

.. code-block:: console

   vjer <action>

You may also run Vjer directly from source:

.. code-block:: console

   python -m vjer <action>

Supported actions
-----------------

- `test`
- `build`
- `deploy`
- `rollback`
- `pre_release`
- `release`
- `freeze`

The `pre_release` action uses the `release` section and is intended for staging,
pre-release tagging, and pre-release artifact preparation. The `release` action
uses the same `release` configuration for final publish behavior.

The `freeze` action does not use `vjer.yml`. It generates a frozen requirements
file from `requirements.txt`.

Configuration
-------------

Vjer expects a YAML configuration file named `vjer.yml` by default. Use `VJER_CFG`
to point to a different file.

Example:

.. code-block:: console

   export VJER_CFG=custom-vjer.yml
   vjer build

Common configuration sections are described in :doc:`configuration`.

Environment variables
---------------------

Vjer honors a small set of environment variables that affect startup and action
behavior.

- `VJER_CFG`
- `VJER_ENV`
- `VIRTUAL_ENV`
- `VJER_PKG_INSTALLS`
- `VJER_PIP_INSTALLS`
- `VJER_PIP_INSTALL_FILE`
- `VJER_PYPROJECT_BUILD`
- `VJER_DOCKER_PUSH`
- `VJER_BUILD_NUM`

For CI git integration, Vjer also reads standard provider variables such as
`CI_COMMIT_REF_NAME`, `CI_COMMIT_BRANCH`, `CI_REMOTE_REF`, `CI_REPOSITORY_URL`,
`GITHUB_REF`, `GITHUB_REPOSITORY`, and `GITHUB_SERVER_URL`.

Next steps
----------

- :doc:`cli_reference`
- :doc:`actions`
- :doc:`configuration`
