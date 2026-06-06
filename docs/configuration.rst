Configuration Reference
=======================

Vjer project configuration is stored in a YAML file named `vjer.yml` by default.
You can override the filename using the `VJER_CFG` environment variable.

Schema
------

The configuration file must include a `schema` value.
The current supported schema is `3`.

Sections
--------

The supported configuration sections are:

- `project`
- `test`
- `build`
- `deploy`
- `rollback`
- `release`

Example configuration
---------------------

.. code-block:: yaml

   schema: 3
   project:
     name: vjer
     version_service:
       type: bumpver
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

The `project` section defines general project settings and defaults.
Common fields include:

- `name` — the project name.
- `version_service` — controls how the release version is determined.
  - `type: bumpver` reads the version from bumpver configuration.
  - `type: environment` reads the version from an environment variable.
  - `type: vjer` uses Vjer's internal versioning behavior.
- `environment` — optional environment variables set before actions run.

Default project values include:

- `artifacts_dir` (default `artifacts`)
- `documentation` (default `docs`)
- `test_results` (default `test_results`)
- `build_num_var` (default `VJER_BUILD_NUM`)
- `chart_root` (default `helm-chart`)
- `dockerfile` (default `Dockerfile`)
- `version_service.type` (default `vjer`)

Build section
-------------

The `build` section defines build step configuration.
Common fields include:

- `source_dir` — the build source tree root.
- `version_files` — files used for version updates.
- `artifacts` — artifact publishing or packaging settings.
- `build_date` — a timestamp inserted into the build metadata.
- `platform` — platform information used by the build environment.

Test section
------------

The `test` section contains a `steps` list describing tests to run.
Each entry typically defines a `type` such as `flake8`, `pylint`, `mypy`, or `python_unittest`.

Release section
---------------

The `release` section contains a `steps` list describing publish and versioning actions.
Common release step types include `pypi`, `increment_release`, `setuptools_build`, and `github`.

Deploy / rollback
------------------

The `deploy` and `rollback` sections contain step lists for deploying and rolling back releases.
These sections are used by the matching `vjer deploy` and `vjer rollback` actions.

Writing configuration
---------------------

Vjer can write a configuration file from the active `ProjectConfig` object using `ProjectConfig.write()`.
This writes only values that are present in the active configuration and preserves the `schema` field.

Notes
-----

- If a configuration file is missing, Vjer raises a `ConfigurationError`.
- Invalid schema values are rejected.
- The project config defaults are applied automatically when Vjer loads the file.
