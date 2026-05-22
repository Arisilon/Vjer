"""Tests for configuration classes in vjer.utils."""

import tests.test_support  # noqa: F401
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from dotmap import DotMap

from vjer.utils import (ConfigSection, ConfigurationError, Environment,
                        ProjectConfig, _PROJECT_DEFAULTS, _CONFIG_SECTIONS)


class TestEnvironment(unittest.TestCase):
    """Tests for the Environment class."""

    def test_environment_getattr_existing_variable(self) -> None:
        """Test getting an existing environment variable."""
        with patch.dict(os.environ, {'TEST_VAR': 'test_value'}):
            env = Environment()
            self.assertEqual(env.TEST_VAR, 'test_value')

    def test_environment_getattr_missing_variable(self) -> None:
        """Test getting a non-existing environment variable raises AttributeError."""
        with patch.dict(os.environ, {}, clear=True):
            env = Environment()
            with self.assertRaises(AttributeError) as ctx:
                _ = env.NONEXISTENT_VAR
            self.assertIn('Environment variable not found', str(ctx.exception))

    def test_environment_multiple_variables(self) -> None:
        """Test accessing multiple environment variables."""
        with patch.dict(os.environ, {'VAR1': 'value1', 'VAR2': 'value2'}):
            env = Environment()
            self.assertEqual(env.VAR1, 'value1')
            self.assertEqual(env.VAR2, 'value2')


class TestConfigSection(unittest.TestCase):
    """Tests for the ConfigSection class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = ConfigSection(
            default_key='default_value',
            version='1.0.0',
            build_num='0'
        )

    def test_config_section_init(self) -> None:
        """Test ConfigSection initialization."""
        self.assertIsNotNone(self.config._defaults)
        self.assertIsNotNone(self.config._values)
        self.assertIsNotNone(self.config._expander)

    def test_config_section_get_default(self) -> None:
        """Test getting a default value."""
        self.assertEqual(self.config.default_key, 'default_value')

    def test_config_section_set_value(self) -> None:
        """Test setting a value."""
        self.config.custom_key = 'custom_value'
        self.assertEqual(self.config.custom_key, 'custom_value')

    def test_config_section_values_property(self) -> None:
        """Test the values property."""
        self.config.test_key = 'test_value'
        values = self.config.values
        self.assertIn('test_key', values)
        self.assertEqual(values['test_key'], 'test_value')

    def test_config_section_update(self) -> None:
        """Test updating configuration values."""
        self.config.update({'new_key': 'new_value', 'another_key': 'another_value'})
        self.assertEqual(self.config.new_key, 'new_value')
        self.assertEqual(self.config.another_key, 'another_value')

    def test_config_section_update_defaults(self) -> None:
        """Test updating default values."""
        self.config.update_defaults({'default_new': 'new_default'})
        self.assertEqual(self.config.default_new, 'new_default')

    def test_config_section_update_expander_with_dict(self) -> None:
        """Test updating expander with a property dictionary."""
        self.config.update_expander(property_dict={'VAR': 'expanded_value'})
        # The expander should now contain the variable
        self.assertIsNotNone(self.config._expander)

    def test_config_section_internal_attributes(self) -> None:
        """Test that internal attributes starting with _ are not added to values."""
        self.config._internal = 'should_not_appear_in_values'
        self.assertNotIn('_internal', self.config.values)

    def test_config_section_with_dotmap(self) -> None:
        """Test updating with DotMap."""
        dot_data = DotMap(key1='value1', key2='value2')
        self.config.update(dot_data)
        self.assertEqual(self.config.key1, 'value1')
        self.assertEqual(self.config.key2, 'value2')

    def test_config_section_list_expansion(self) -> None:
        """Test that list values are properly returned."""
        self.config.update({'list_key': ['item1', 'item2']})
        list_value = self.config.list_key
        self.assertIsInstance(list_value, list)
        self.assertEqual(len(list_value), 2)

    def test_config_section_attribute_error(self) -> None:
        """Test that accessing non-existent attribute raises AttributeError."""
        with self.assertRaises(AttributeError):
            _ = self.config.nonexistent_attribute


class TestConfigurationError(unittest.TestCase):
    """Tests for ConfigurationError class."""

    def test_bad_format_error(self) -> None:
        """Test BAD_FORMAT error."""
        error = ConfigurationError.BAD_FORMAT
        self.assertIsNotNone(error)

    def test_config_file_not_found_error(self) -> None:
        """Test CONFIG_FILE_NOT_FOUND error."""
        error = ConfigurationError.CONFIG_FILE_NOT_FOUND
        self.assertIsNotNone(error)

    def test_invalid_schema_error(self) -> None:
        """Test INVALID_SCHEMA error."""
        error = ConfigurationError.INVALID_SCHEMA
        self.assertIsNotNone(error)


class TestProjectConfig(unittest.TestCase):
    """Tests for the ProjectConfig class."""

    @patch('vjer.utils.Path.cwd')
    @patch('vjer.utils.ProjectConfig._load_config')
    @patch('vjer.utils.ProjectConfig._set_defaults')
    @patch('vjer.utils.ProjectConfig._set_version')
    def test_project_config_init(self, mock_set_version: MagicMock,
                                 mock_set_defaults: MagicMock,
                                 mock_load_config: MagicMock,
                                 mock_cwd: MagicMock) -> None:
        """Test ProjectConfig initialization."""
        mock_cwd.return_value = Path('/test/project')

        config = ProjectConfig()

        self.assertIsNotNone(config._sections)
        self.assertEqual(len(config._sections), len(_CONFIG_SECTIONS))
        self.assertIsNotNone(config.project)

    @patch('vjer.utils.Path.cwd')
    @patch('vjer.utils.ProjectConfig._load_config')
    @patch('vjer.utils.ProjectConfig._set_defaults')
    @patch('vjer.utils.ProjectConfig._set_version')
    def test_project_config_section_access(self, mock_set_version: MagicMock,
                                          mock_set_defaults: MagicMock,
                                          mock_load_config: MagicMock,
                                          mock_cwd: MagicMock) -> None:
        """Test accessing configuration sections."""
        mock_cwd.return_value = Path('/test/project')

        config = ProjectConfig()

        # Test accessing valid sections
        self.assertIsNotNone(config.project)
        self.assertIsNotNone(config.test)
        self.assertIsNotNone(config.build)
        self.assertIsNotNone(config.deploy)
        self.assertIsNotNone(config.release)

    @patch('vjer.utils.Path.cwd')
    @patch('vjer.utils.ProjectConfig._load_config')
    @patch('vjer.utils.ProjectConfig._set_defaults')
    @patch('vjer.utils.ProjectConfig._set_version')
    def test_project_config_invalid_section(self, mock_set_version: MagicMock,
                                           mock_set_defaults: MagicMock,
                                           mock_load_config: MagicMock,
                                           mock_cwd: MagicMock) -> None:
        """Test accessing an invalid configuration section."""
        mock_cwd.return_value = Path('/test/project')

        config = ProjectConfig()

        with self.assertRaises(AttributeError):
            _ = config.invalid_section

    @patch('vjer.utils.Path.cwd')
    @patch('vjer.utils.ProjectConfig._load_config')
    @patch('vjer.utils.ProjectConfig._set_defaults')
    @patch('vjer.utils.ProjectConfig._set_version')
    def test_project_config_load_config_file_not_found(self, mock_set_version: MagicMock,
                                                       mock_set_defaults: MagicMock,
                                                       mock_load_config: MagicMock,
                                                       mock_cwd: MagicMock) -> None:
        """Test _load_config when config file doesn't exist."""
        mock_cwd.return_value = Path('/nonexistent/project')

        def raise_config_error(*args: tuple, **kwargs: dict) -> None:
            raise ConfigurationError(ConfigurationError.CONFIG_FILE_NOT_FOUND,
                                   file=Path('/nonexistent/project/vjer.yml'))

        mock_load_config.side_effect = raise_config_error
        with self.assertRaises(ConfigurationError):
            ProjectConfig()

    @patch('vjer.utils.Path.cwd')
    @patch('vjer.utils.ProjectConfig._load_config')
    @patch('vjer.utils.ProjectConfig._set_defaults')
    @patch('vjer.utils.ProjectConfig._set_version')
    def test_project_config_schema_attribute(self, mock_set_version: MagicMock,
                                            mock_set_defaults: MagicMock,
                                            mock_load_config: MagicMock,
                                            mock_cwd: MagicMock) -> None:
        """Test schema attribute is accessible."""
        mock_cwd.return_value = Path('/test/project')

        config = ProjectConfig()
        config.schema = 3

        self.assertEqual(config.schema, 3)


if __name__ == '__main__':
    unittest.main()
