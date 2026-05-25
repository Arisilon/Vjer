"""Tests for vjer.test module."""

# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name
# flake8: noqa

from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch, PropertyMock

from vjer.test import TestStep


class TestTestStep(TestCase):
    """Tests for the TestStep class."""

    @patch('vjer.test.VjerAction')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_step_init(self, mock_git_client: MagicMock, mock_config: MagicMock,
                            _unused_mock_vjer_action: MagicMock) -> None:
        """Test TestStep initialization."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            version='1.0.0',
            test_results='test_results',
            test_results_dir=Path('/test/project/test_results'),
            artifacts='artifacts',
            container_registry=MagicMock(type='local', auth=tuple(), name=''),
            version_service=MagicMock(type='vjer'))
        mock_config_instance.build = MagicMock(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        mock_git_instance = MagicMock()
        mock_git_client.return_value = mock_git_instance

        step = TestStep()

        self.assertIsNotNone(step)
        self.assertIsNotNone(step.config)
        self.assertIsNotNone(step.project)


class TestTestStepPre(TestCase):
    """Tests for TestStep.pre method."""

    @patch('vjer.test.rmpath')
    @patch('vjer.test.Path')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_step_pre_removes_old_test_results(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock,
                                                    _unused_mock_path_class: MagicMock, _unused_mock_rmpath: MagicMock) -> None:
        """Test that pre() removes old test results directory."""
        mock_config_instance = MagicMock()
        test_results_path = Path('/test/project/test_results')
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            test_results_dir=test_results_path,
            test_results='test_results',
            artifacts='artifacts',
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(is_first_step=True)

        # Mock Path operations
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'mkdir'):
                with patch('vjer.test.VjerStep.pre'):
                    step.pre()

    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_step_pre_calls_parent_pre(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock) -> None:
        """Test that pre() calls parent class pre()."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            test_results_dir=Path('/test/project/test_results'),
            test_results='test_results',
            artifacts='artifacts',
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0', build_version='1.0.0-0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(is_first_step=False)

        with patch('vjer.test.VjerStep.pre') as mock_parent_pre:
            step.pre()
            mock_parent_pre.assert_called_once()


class TestTestStepTestMethods(TestCase):
    """Tests for TestStep test method runners."""

    @patch('vjer.test.SysCmdRunner')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_flake8(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock, _unused_mock_syscmd_runner: MagicMock) -> None:
        """Test test_flake8 method calls SysCmdRunner."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            test_results_dir=Path('/test/project/test_results'),
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(targets=[], options={})

        with patch.object(step, '_test_runner') as mock_test_runner:
            step.test_flake8()
            mock_test_runner.assert_called_once_with('flake8')

    @patch('vjer.test.SysCmdRunner')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_mypy(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock, _unused_mock_syscmd_runner: MagicMock) -> None:
        """Test test_mypy method calls SysCmdRunner."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            test_results_dir=Path('/test/project/test_results'),
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(targets=[], options={})

        with patch.object(step, '_test_runner') as mock_test_runner:
            step.test_mypy()
            mock_test_runner.assert_called_once_with('mypy')

    @patch('vjer.test.SysCmdRunner')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_pylint(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock, _unused_mock_syscmd_runner: MagicMock) -> None:
        """Test test_pylint method calls SysCmdRunner."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            test_results_dir=Path('/test/project/test_results'),
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(targets=[], options={})

        with patch.object(step, '_test_runner') as mock_test_runner:
            step.test_pylint()
            mock_test_runner.assert_called_once_with('pylint')


class TestTestStepHelm(TestCase):
    """Tests for TestStep helm test method."""

    @patch('vjer.test.helm')
    @patch('vjer.test.Path')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_helm(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock,
                       _unused_mock_path: MagicMock, _unused_mock_helm: MagicMock) -> None:
        """Test test_helm method."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            chart_root='helm-chart',
            test_results_dir=Path('/test/project/test_results'),
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(helm_args={}, build_test_stage='')

        with patch.object(step, 'dockerfile', Path('/test/Dockerfile')):
            with patch.object(type(step), 'helm_chart_root', new_callable=PropertyMock, return_value=Path('/test/helm-chart')):
                with patch('vjer.test.slurp', return_value=['FROM base']):
                    with patch('vjer.test.syscmd'):
                        with patch('vjer.test.open', create=True):
                            with patch('vjer.test.yaml_load', return_value={'type': 'library'}):
                                step.test_helm()


class TestTestStepDocker(TestCase):
    """Tests for TestStep docker test method."""

    @patch('vjer.test.Path')
    @patch('vjer.utils.ProjectConfig')
    @patch('vjer.utils.GitClient')
    def test_test_docker(self, _unused_mock_git_client: MagicMock, mock_config: MagicMock, _unused_mock_path: MagicMock) -> None:
        """Test test_docker method."""
        mock_config_instance = MagicMock()
        mock_config_instance.project = MagicMock(
            project_root=Path('/test/project'),
            name='test-project',
            test_results_dir=Path('/test/project/test_results'),
            version_service=MagicMock(type='vjer'),
            container_registry=MagicMock(type='local', auth=tuple(), name=''))
        mock_config_instance.build = MagicMock(build_num='0')
        mock_config_instance.release = MagicMock()
        mock_config.return_value = mock_config_instance

        step = TestStep()
        step.step_info = MagicMock(build_test_stage='')

        with patch.object(step, 'dockerfile', Path('/test/Dockerfile')):
            with patch('vjer.test.slurp', return_value=['FROM base']):
                with patch('vjer.test.syscmd'):
                    step.test_docker()


if __name__ == '__main__':
    main()

# cSpell:ignore syscmd
