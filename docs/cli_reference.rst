CLI Reference
=============

Top-level command
-----------------

.. programoutput:: python -m vjer --help
   :caption: Vjer top-level help
   :force:

Supported actions
-----------------

Vjer accepts a single action argument and runs the matching configured phase.

- `test`
- `build`
- `deploy`
- `rollback`
- `pre_release`
- `release`
- `freeze`

Usage
-----

Run a Vjer action from the project root:

.. code-block:: console

   vjer <action>

From source tree without an installed console script:

.. code-block:: console

   python -m vjer <action>

The `freeze` action accepts an optional suffix argument. For example:

.. code-block:: console

   vjer freeze
   vjer freeze ci

Environment variables
---------------------

Vjer supports a small set of runtime environment variables that modify CLI behavior and configuration loading.

- `VJER_CFG`
  - Override the configuration file name. Defaults to `vjer.yml` in the project root.
- `VJER_ENV`
  - Determines the runtime environment. Defaults to `local`.
  - When set to `local`, Vjer requires `VIRTUAL_ENV` to be active.
- `VIRTUAL_ENV`
  - Required when running locally in `VJER_ENV=local`.
- `VJER_PKG_INSTALLS`
  - Space-separated packages installed with `apt-get` before action execution on Linux.
- `VJER_PIP_INSTALLS`
  - Packages installed with pip before action execution.
- `VJER_PIP_INSTALL_FILE`
  - A requirements file to install with pip before action execution.
- `VJER_PYPROJECT_BUILD`
  - When set, Vjer installs the project from `pyproject.toml` using the configured build backend.
- `VJER_DOCKER_PUSH`
  - Controls whether Docker images built by Docker build steps are pushed.
  - Default: `true` in non-local environments and `false` in `VJER_ENV=local`.
- `VJER_BUILD_NUM`
  - Build number used to form build metadata and non-bumpver image tags.
  - Default: `0`.

CI environment variables used by Git operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vjer also reads standard CI variables when available to determine the current branch and repository remote:

- `CI_COMMIT_REF_NAME`
- `CI_COMMIT_BRANCH`
- `GITHUB_REF`
- `CI_REMOTE_REF`
- `CI_REPOSITORY_URL`
- `GITHUB_REPOSITORY`
- `GITHUB_SERVER_URL`
