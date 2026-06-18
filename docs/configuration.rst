Configuration Reference
=======================

Vjer project configuration is stored in a YAML file. By default this file is named
`vjer.yml` and is located in the project root. You can override the filename with
`VJER_CFG`.

Schema
------

The configuration file must include a top-level `schema` value.
The current supported schema is `3`.

The file is validated at startup. Vjer raises a `ConfigurationError` if the file is
missing, empty, malformed, or uses an unsupported schema.

Variable expansion
------------------

Vjer supports variable expansion in string values using BatCave's expander syntax.
For example, values can reference environment variables or other configuration
properties:

.. code-block:: yaml

   project:
     name: sample-app
     version: "{var:VJER_VERSION}"

The expander is applied to strings, lists, and dictionaries.

Configuration sections
----------------------

Vjer recognizes these sections:

- `project`
- `test`
- `build`
- `deploy`
- `rollback`
- `release`

Notes:

- `pre_release` uses the `release` section and is not a separate configuration section.
- `freeze` is a supported action but not driven by `vjer.yml`.

Example configuration
---------------------

.. code-block:: yaml

   schema: 3
   project:
     name: vjer
     version_service:
       type: bumpver
     container_registry:
       type: local
       auth: []
       name: ''
     helm_repository:
       type: oci
       url: 'https://example.com/helm'
       name: 'example'
     environment:
       PYPI_TOKEN: '{var:PYPI_TOKEN}'
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
         pre_release_only: true
       - type: increment_release

Project section
---------------

The `project` section defines common project settings and defaults.

Fields:

- `name`
  - The project name.
- `version`
  - The explicit project version used when `version_service.type` is `vjer`.
- `version_service`
  - Controls how the version is determined.
  - `type: bumpver` reads the current version from bumpver configuration.
  - `type: environment` reads the version from an environment variable specified by `variable`.
  - `type: vjer` uses Vjer's internal versioning behavior and will use `project.version` if set.
  - `variable` is used only when `type: environment`.
- `environment`
  - A mapping of environment variables to set before action execution.
- `artifacts_dir`
  - Path to the build artifacts directory. Default: `artifacts`.
- `documentation`
  - Documentation source directory. Default: `docs`.
- `test_results`
  - Test results directory. Default: `test_results`.
- `build_num_var`
  - Environment variable used to read the build number. Default: `VJER_BUILD_NUM`.
- `chart_root`
  - Helm chart root directory. Default: `helm-chart`.
- `dockerfile`
  - Dockerfile path. Default: `Dockerfile`.
- `container_registry`
  - Registry configuration used for Docker build and release steps.
  - `type` defaults to `local`.
  - `auth` is passed to the registry client.
  - `name` is the registry name or path prefix.
- `helm_repository`
  - Helm repository configuration used for Helm deploy and release steps.
  - Common fields include `type`, `url`, `name`, and `push_args`.

Build section
-------------

The `build` section configures build-time behavior and build steps.

Fields:

- `source_dir`
  - Root of the build source tree. Default: `src`.
- `version_files`
  - List of files to update with version values during build and reset after completion.
- `artifacts`
  - Arbitrary artifact metadata for custom build logic.
- `build_date`
  - Timestamp inserted into build metadata. Default: the current date/time.
- `platform`
  - Platform metadata used by the build environment.

Build step types
~~~~~~~~~~~~~~~~

Build steps are defined under `build.steps`. Supported types include:

- `docker`
  - Builds a Docker image.
  - Optional fields: `image`, `build_args`, `tags`, `version_files`, `dockerfile`, `set_app_version`, `module`.
  - `build_args` are merged with built-in values `VERSION` and `BUILD_VERSION`.
  - `VJER_DOCKER_PUSH` controls whether the image is pushed automatically.
- `flit`
  - Builds a Python package using flit.
  - Optional fields: `module`, `version_files`.
- `setuptools`
  - Builds a Python package using setuptools.
  - Optional fields: `module`, `version_files`.
- `helm`
  - Packages a Helm chart and optionally makes it available for deploy/release.
  - Optional fields: `values_files`, `helm_variables`, `version_files`.
- `sphinx`
  - Builds Sphinx documentation.
  - Optional field: `doc_type`.
  - If `doc_type: api`, Sphinx autogeneration runs before building documentation.

Test section
------------

The `test` section defines test steps. Each step uses `type` to select the test runner.

Common fields for test steps:

- `targets`
  - Arguments passed to the test command. Defaults to the project name or discovered tests.
- `options`
  - A mapping of options passed to the test command.
- `build_test_stage`
  - Used by Docker-based tests to select a Docker build stage.
- `dockerfile`
  - Path to the Dockerfile when running Docker-based tests.
- `helm_args`
  - Additional Helm command arguments.
- `values_files`
  - List of values files to pass to Helm commands.
- `helm_variables`
  - Helm variable overrides to pass as `--set` pairs.

Supported test step types:

- `docker`
- `flake8`
- `helm`
- `mypy`
- `pylint`
- `python_unittest`

Release section
---------------

The `release` section defines publication and versioning steps.
It is used by both `vjer release` and `vjer pre_release`.

Common release step fields:

- `release_only`
  - If true, the step runs only during `release` and not `pre_release`.
- `pre_release_only`
  - If true, the step runs only during `pre_release` and not `release`.

Release step types
~~~~~~~~~~~~~~~~~~

- `docker`
  - Tags and optionally pushes Docker images.
  - Optional fields: `image`, `tags`, `release_only`, `pre_release_only`.
- `flit_build`
  - Builds with flit and copies artifacts.
- `github`
  - Creates a GitHub release using the GitHub CLI.
- `helm`
  - Pushes a Helm chart to the configured Helm repository.
- `increment_release`
  - Bumps the version after release.
  - Uses `project.version_service.type` to select the increment behavior.
  - Optional: `increment_branch`, `args`.
- `pypi`
  - Uploads artifacts to PyPI via Twine.
  - Optional fields: `test_pypi`, `username`, `password`.
- `setuptools_build`
  - Builds a Python package with setuptools.
- `tag_source`
  - Tags the Git source repository.
  - Optional field: `release_tag`.

Deploy section
--------------

The `deploy` section defines deployment steps.

Deploy step fields are passed to Helm commands:

- `chart_name`
- `release_name`
- `remote`
- `helm_args`
- `values_files`
- `helm_variables`

Helm deployment behavior:

- If `remote` is not `false`, Vjer deploys from the configured Helm repository.
- If `remote` is `false`, Vjer deploys from a local Helm package file.

Rollback section
----------------

The `rollback` section defines rollback steps for release rollbacks.
It currently supports Helm rollback with the same fields as deploy:

- `chart_name`
- `release_name`
- `helm_args`
- `values_files`
- `helm_variables`

Freeze action
-------------

The `freeze` action is not configured through `vjer.yml`.
It creates a frozen requirements file from the root `requirements.txt`
file and writes output to `requirements-frozen.txt` or
`requirements-frozen-<suffix>.txt` when a suffix argument is provided.

Writing configuration
---------------------

Vjer can write the active project configuration using `ProjectConfig.write()`.
This preserves the `schema` field and writes only the active configuration values.
