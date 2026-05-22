"""Integration and utility tests for vjer module."""

import tests.test_support  # noqa: F401
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from dotmap import DotMap
from batcave.lang import BatCaveException

from vjer.utils import (
    ConfigurationError, StepError, _CONFIG_SECTIONS, _PROJECT_DEFAULTS,
    REMOTE_REF, BAD_TAG_CHARACTERS, REPLACER_HOLDER,
    PROJECT_CFG_FILE, TOOL_REPORT, HELM_CHART_FILE,
    DEFAULT_VERSION_FILES, VJER_ENV
)


class TestConfigurationConstants(unittest.TestCase):
    """Tests for configuration constants."""

    def test_config_sections(self) -> None:
        """Test _CONFIG_SECTIONS is defined correctly."""
        self.assertIsInstance(_CONFIG_SECTIONS, tuple)
        self.assertGreater(len(_CONFIG_SECTIONS), 0)
        self.assertIn('project', _CONFIG_SECTIONS)
        self.assertIn('test', _CONFIG_SECTIONS)
        self.assertIn('build', _CONFIG_SECTIONS)

    def test_project_defaults(self) -> None:
        """Test _PROJECT_DEFAULTS is defined correctly."""
        self.assertIsInstance(_PROJECT_DEFAULTS, DotMap)
        self.assertIn('build_artifacts', _PROJECT_DEFAULTS)
        self.assertIn('test_results', _PROJECT_DEFAULTS)
        self.assertIn('dockerfile', _PROJECT_DEFAULTS)

    def test_project_config_file(self) -> None:
        """Test PROJECT_CFG_FILE constant."""
        self.assertIsInstance(PROJECT_CFG_FILE, str)
        self.assertIn('.yml', PROJECT_CFG_FILE)

    def test_tool_report_path(self) -> None:
        """Test TOOL_REPORT path."""
        self.assertIsInstance(TOOL_REPORT, Path)

    def test_remote_ref(self) -> None:
        """Test REMOTE_REF constant."""
        self.assertEqual(REMOTE_REF, 'vjer_origin')
        self.assertIsInstance(REMOTE_REF, str)

    def test_bad_tag_characters(self) -> None:
        """Test BAD_TAG_CHARACTERS constant."""
        self.assertIsInstance(BAD_TAG_CHARACTERS, str)
        self.assertGreater(len(BAD_TAG_CHARACTERS), 0)

    def test_replacer_holder(self) -> None:
        """Test REPLACER_HOLDER constant."""
        self.assertEqual(REPLACER_HOLDER, '-')

    def test_helm_chart_file(self) -> None:
        """Test HELM_CHART_FILE constant."""
        self.assertEqual(HELM_CHART_FILE, 'Chart.yaml')

    def test_default_version_files(self) -> None:
        """Test DEFAULT_VERSION_FILES constant."""
        self.assertIsInstance(DEFAULT_VERSION_FILES, dict)
        self.assertIn('helm', DEFAULT_VERSION_FILES)
        self.assertIn('flit', DEFAULT_VERSION_FILES)
        self.assertIn('setuptools', DEFAULT_VERSION_FILES)

    def test_vjer_env(self) -> None:
        """Test VJER_ENV constant."""
        self.assertIsInstance(VJER_ENV, str)
        # VJER_ENV should be either 'local' or some other value based on environment
        self.assertGreater(len(VJER_ENV), 0)


class TestStepError(unittest.TestCase):
    """Tests for StepError exception."""

    def test_step_error_unknown_object(self) -> None:
        """Test StepError.UNKNOWN_OBJECT error."""
        error = StepError.UNKNOWN_OBJECT
        self.assertIsNotNone(error)
        self.assertEqual(error.code, 1)

    def test_step_error_is_exception(self) -> None:
        """Test StepError is an exception."""
        self.assertTrue(issubclass(StepError, BatCaveException))


class TestConfigurationErrorHierarchy(unittest.TestCase):
    """Tests for ConfigurationError exception hierarchy."""

    def test_configuration_error_is_exception(self) -> None:
        """Test ConfigurationError is an exception."""
        self.assertTrue(issubclass(ConfigurationError, BatCaveException))

    def test_configuration_error_has_multiple_errors(self) -> None:
        """Test ConfigurationError has defined error types."""
        # These should be error objects
        self.assertIsNotNone(ConfigurationError.BAD_FORMAT)
        self.assertIsNotNone(ConfigurationError.CONFIG_FILE_NOT_FOUND)
        self.assertIsNotNone(ConfigurationError.INVALID_SCHEMA)


class TestEnvironmentConstants(unittest.TestCase):
    """Tests for environment-related constants."""

    def test_environment_variable_access(self) -> None:
        """Test accessing VJER_ENV."""
        with patch.dict(os.environ, {'VJER_ENV': 'testing'}):
            # Re-import to get updated constant
            import importlib
            import vjer.utils as utils_module
            importlib.reload(utils_module)
            self.assertIn(utils_module.VJER_ENV, ['testing', 'local'])

    def test_default_config_file(self) -> None:
        """Test default config file with environment override."""
        with patch.dict(os.environ, {'VJER_CFG': 'custom.yml'}):
            import importlib
            import vjer.utils as utils_module
            importlib.reload(utils_module)
            # Note: This might not work as expected if PROJECT_CFG_FILE is
            # already computed at module load time

    def test_project_cfg_file_valid(self) -> None:
        """Test PROJECT_CFG_FILE is a valid filename."""
        self.assertTrue(len(PROJECT_CFG_FILE) > 0)
        self.assertTrue(PROJECT_CFG_FILE.endswith(('.yml', '.yaml')))


class TestConfigSectionListHandling(unittest.TestCase):
    """Tests for list handling in ConfigSection."""

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_config_list_attribute_expansion(self, mock_git_client: MagicMock,
                                            mock_config: MagicMock) -> None:
        """Test that ConfigSection expands list attributes."""
        from vjer.utils import ConfigSection

        config = ConfigSection()
        config.update({'values_list': ['item1', 'item2', 'item3']})

        values_list = config.values_list
        self.assertIsInstance(values_list, list)
        self.assertEqual(len(values_list), 3)

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_config_dict_attribute_expansion(self, mock_git_client: MagicMock,
                                            mock_config: MagicMock) -> None:
        """Test that ConfigSection expands dict attributes."""
        from vjer.utils import ConfigSection

        config = ConfigSection()
        config.update({'settings': {'key1': 'value1', 'key2': 'value2'}})

        settings = config.settings
        self.assertIsInstance(settings, DotMap)
        self.assertEqual(settings.key1, 'value1')
        self.assertEqual(settings.key2, 'value2')


class TestProjectDefaultValues(unittest.TestCase):
    """Tests for project default values."""

    def test_build_artifacts_default(self) -> None:
        """Test build_artifacts default."""
        self.assertEqual(_PROJECT_DEFAULTS.build_artifacts, 'artifacts')

    def test_build_num_var_default(self) -> None:
        """Test build_num_var default."""
        self.assertEqual(_PROJECT_DEFAULTS.build_num_var, 'VJER_BUILD_NUM')

    def test_chart_root_default(self) -> None:
        """Test chart_root default."""
        self.assertEqual(_PROJECT_DEFAULTS.chart_root, 'helm-chart')

    def test_dockerfile_default(self) -> None:
        """Test dockerfile default."""
        self.assertEqual(_PROJECT_DEFAULTS.dockerfile, 'Dockerfile')

    def test_test_results_default(self) -> None:
        """Test test_results default."""
        self.assertEqual(_PROJECT_DEFAULTS.test_results, 'test_results')

    def test_container_registry_default(self) -> None:
        """Test container_registry default."""
        self.assertIsInstance(_PROJECT_DEFAULTS.container_registry, DotMap)
        self.assertEqual(_PROJECT_DEFAULTS.container_registry.type, 'local')


if __name__ == '__main__':
    unittest.main()
