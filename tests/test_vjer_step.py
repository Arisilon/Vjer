"""Tests for VjerStep class."""

# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name,protected-access,arguments-differ
# flake8: noqa

from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from dotmap import DotMap

from vjer.utils import VjerStep


class TestVjerStep(TestCase):
    """Tests for the VjerStep class."""

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def setUp(self, mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Set up test fixtures."""
        self.mock_config = mock_config
        self.mock_git_client = mock_git_client

        # Configure mock config
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        # Configure mock git client
        mock_git_instance = MagicMock()
        mock_git_instance.ci_remote_ref = 'https://github.com/test/repo.git'
        mock_git_instance.ci_commit_ref_name = 'main'
        mock_git_client.return_value = mock_git_instance

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_init(self, mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test VjerStep initialization."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        mock_git_instance = MagicMock()
        mock_git_client.return_value = mock_git_instance

        step = VjerStep()

        self.assertIsNotNone(step.config)
        self.assertIsNotNone(step.project)
        self.assertIsNotNone(step.build)
        self.assertIsNotNone(step.release)
        self.assertIsNotNone(step.git_client)
        self.assertEqual(step.pre_release_num, '0')
        self.assertIsNone(step.registry_client)
        self.assertIsNone(step.docker_client)

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_getattr_from_project(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test __getattr__ retrieves attributes from project."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()

        # Should get from project if not in step_info
        self.assertEqual(step.version, '1.0.0')
        self.assertEqual(step.name, 'test-project')

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_getattr_from_step_info(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test __getattr__ prefers step_info over project."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()
        step.step_info = DotMap(version='2.0.0')

        # Should prefer step_info value
        self.assertEqual(step.version, '2.0.0')

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_getattr_invalid_attribute(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test __getattr__ raises for invalid attributes."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()
        step.project = type('ProjectObj', (), {
            'project_root': Path('/test/project'),
            'name': 'test-project',
            'version': '1.0.0',
            'test_results': 'test_results',
            'artifacts': 'artifacts',
            'container_registry': DotMap(type='local', auth=tuple(), name=''),
            'version_service': DotMap(type='vjer')})()

        with self.assertRaises(AttributeError):
            _ = step.nonexistent_attribute

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_helm_chart_root_property(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test helm_chart_root property."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'),
            chart_root='helm-chart')
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()
        step.step_info = DotMap()

        helm_root = step.helm_chart_root
        self.assertIsInstance(helm_root, Path)

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_pkg_name_property(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test pkg_name property."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()
        step.step_info = DotMap(pkg_name='')

        pkg_name = step.pkg_name
        self.assertIn('test-project', pkg_name)
        self.assertIn('1.0.0', pkg_name)

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_helm_args_property_empty(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test helm_args property when no values."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()
        step.step_info = DotMap(helm_args='', values_files='', helm_variables='')

        helm_args = step.helm_args
        self.assertIsInstance(helm_args, dict)

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_vjer_step_helm_repo_property(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test helm_repo property."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'),
            helm_repository=DotMap(type='oci', url='', name=''))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        step = VjerStep()
        step.step_info = DotMap()

        helm_repo = step.helm_repo
        self.assertIsNotNone(helm_repo)


class TestVjerStepDocker(TestCase):
    """Tests for VjerStep Docker-related methods."""

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    @patch('vjer.utils.Cloud')
    def test_docker_init(self, mock_cloud: MagicMock, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test _docker_init method."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = DotMap(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            artifacts='artifacts',
            container_registry=DotMap(type='local', auth=tuple(), name=''),
            version_service=DotMap(type='vjer'))
        mock_config_instance.build = DotMap(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = DotMap()
        mock_config.return_value = mock_config_instance

        mock_registry = MagicMock()
        mock_docker = MagicMock()
        mock_cloud.side_effect = [mock_registry, mock_docker]

        step = VjerStep()
        step.step_info = DotMap(image='')

        step._docker_init(login=False)

        self.assertIsNotNone(step.registry_client)
        self.assertIsNotNone(step.docker_client)
        self.assertIsNotNone(step.image_name)
        self.assertIsNotNone(step.version_tag)
        self.assertIsNotNone(step.image_tag)


if __name__ == '__main__':
    main()
