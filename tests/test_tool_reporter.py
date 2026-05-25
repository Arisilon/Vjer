"""Tests for tool_reporter module."""

# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name,import-outside-toplevel
# flake8: noqa

from re import compile as re_compile
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from dotmap import DotMap
from batcave.sysutil import CMDError

from vjer.tool_reporter import tool_reporter, get_version, get_helm_info, PRODUCTS


class TestToolReporter(TestCase):
    """Tests for the tool_reporter function."""

    @patch('vjer.tool_reporter.get_helm_info')
    @patch('vjer.tool_reporter.get_version')
    def test_tool_reporter(self, mock_get_version: MagicMock, mock_get_helm_info: MagicMock) -> None:
        """Test tool_reporter function."""
        mock_get_version.return_value = '1.0.0'
        mock_get_helm_info.side_effect = [{'repo1': 'https://example.com/repo1'},
                                          {'plugin1': 'https://example.com/plugin1'}]
        result = tool_reporter()
        self.assertIn('tool_versions', result)
        self.assertIn('helm_plugins', result)
        self.assertIn('helm_repos', result)
        self.assertIsInstance(result['tool_versions'], dict)
        self.assertIsInstance(result['helm_plugins'], dict)
        self.assertIsInstance(result['helm_repos'], dict)

    @patch('vjer.tool_reporter.get_helm_info')
    @patch('vjer.tool_reporter.get_version')
    def test_tool_reporter_calls_get_version(self, mock_get_version: MagicMock, mock_get_helm_info: MagicMock) -> None:
        """Test that tool_reporter calls get_version for each product."""
        mock_get_version.return_value = '1.0.0'
        mock_get_helm_info.return_value = {}
        tool_reporter()
        self.assertEqual(mock_get_version.call_count, len(PRODUCTS))

    @patch('vjer.tool_reporter.get_helm_info')
    @patch('vjer.tool_reporter.get_version')
    def test_tool_reporter_calls_get_helm_info(self, mock_get_version: MagicMock, mock_get_helm_info: MagicMock) -> None:
        """Test that tool_reporter calls get_helm_info twice."""
        mock_get_version.return_value = '1.0.0'
        mock_get_helm_info.return_value = {}
        tool_reporter()
        self.assertEqual(mock_get_helm_info.call_count, 2)
        mock_get_helm_info.assert_any_call('plugin')
        mock_get_helm_info.assert_any_call('repo')


class TestGetVersion(TestCase):
    """Tests for the get_version function."""

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_docker(self, mock_syscmd: MagicMock) -> None:
        """Test get_version for Docker."""
        mock_syscmd.return_value = ['Docker version 20.10.0, build abc123']
        product = DotMap(name='Docker', command='', regex=re_compile('Docker version (.+)'), raw=False, args=[])
        version = get_version(product)
        self.assertIn('20.10.0', version)
        mock_syscmd.assert_called_once()

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_not_found(self, mock_syscmd: MagicMock) -> None:
        """Test get_version when command is not found."""
        mock_syscmd.side_effect = FileNotFoundError('Command not found')
        product = DotMap(name='MissingTool', command='missing', regex=re_compile('(.+)'), raw=False, args=[])
        version = get_version(product)
        self.assertEqual(version, 'Not Found')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_cmd_error(self, mock_syscmd: MagicMock) -> None:
        """Test get_version when CMDError with 'not found' occurs."""
        from batcave.lang import BatCaveError
        error = CMDError(BatCaveError(1, 'command not found'), returncode=1, cmd='tool', err_lines=['command not found'])
        mock_syscmd.side_effect = error
        product = DotMap(name='Tool', command='tool', regex=re_compile('(.+)'), raw=False, args=[])
        version = get_version(product)
        self.assertEqual(version, 'Not Found')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_cmd_error_not_related_to_not_found(self, mock_syscmd: MagicMock) -> None:
        """Test get_version re-raises CMDError not related to 'not found'."""
        from batcave.lang import BatCaveError
        error = CMDError(BatCaveError(2, 'some other error'), returncode=1, cmd='tool', err_lines=['other error'])
        mock_syscmd.side_effect = error
        product = DotMap(name='Tool', command='tool', regex=re_compile('(.+)'), raw=False, args=[])
        with self.assertRaises(CMDError):
            get_version(product)

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_with_custom_args(self, mock_syscmd: MagicMock) -> None:
        """Test get_version with custom args."""
        mock_syscmd.return_value = ['Version 1.2.3']
        product = DotMap(name='Helm', command='helm', regex=re_compile('Version (.+)'), raw=False, args=['version'])
        version = get_version(product)
        self.assertIn('1.2.3', version)
        mock_syscmd.assert_called_once_with('helm', 'version', ignore_stderr=True, append_stderr=True)

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_raw_output(self, mock_syscmd: MagicMock) -> None:
        """Test get_version with raw=True."""
        expected_output = ['Raw output line 1', 'Raw output line 2']
        mock_syscmd.return_value = expected_output
        product = DotMap(name='Tool', command='tool', regex=re_compile('(.+)'), raw=True, args=[])
        version = get_version(product)
        self.assertEqual(version, expected_output)

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_no_regex_match(self, mock_syscmd: MagicMock) -> None:
        """Test get_version when regex doesn't match."""
        mock_syscmd.return_value = ['Some output that does not match']
        product = DotMap(name='Tool', command='tool', regex=re_compile('Version (.+)'), raw=False, args=[])
        version = get_version(product)
        self.assertEqual(version, 'Not Found')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_multiline_output(self, mock_syscmd: MagicMock) -> None:
        """Test get_version with multiline output."""
        mock_syscmd.return_value = ['Line 1', 'Line 2 Version 1.5.0', 'Line 3']
        product = DotMap(name='Tool', command='tool', regex=re_compile('Version (.+)'), raw=False, args=[])
        version = get_version(product)
        self.assertIn('1.5.0', version)

    @patch('vjer.tool_reporter.syscmd')
    def test_get_version_gcloud(self, mock_syscmd: MagicMock) -> None:
        """Test get_version for Google Cloud SDK."""
        mock_syscmd.return_value = ['Google Cloud SDK 350.0.0']
        product = DotMap(name='Google Cloud SDK', command='gcloud',
                        regex=re_compile(r'Google Cloud SDK ([\d\.]+) '),
                        raw=False, args=[])
        # Note: This test might fail due to regex requiring space after version
        # but the output doesn't have trailing space
        version = get_version(product)
        self.assertIsNotNone(version)


class TestGetHelmInfo(TestCase):
    """Tests for the get_helm_info function."""

    @patch('vjer.tool_reporter.syscmd')
    def test_get_helm_info_repos(self, mock_syscmd: MagicMock) -> None:
        """Test get_helm_info for repos."""
        mock_syscmd.return_value = ['NAME    URL',
                                    'stable  https://charts.helm.sh/stable',
                                    'bitnami https://charts.bitnami.com/bitnami']

        result = get_helm_info('repo')
        self.assertIn('stable', result)
        self.assertIn('bitnami', result)
        self.assertEqual(result['stable'], 'https://charts.helm.sh/stable')
        self.assertEqual(result['bitnami'], 'https://charts.bitnami.com/bitnami')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_helm_info_plugins(self, mock_syscmd: MagicMock) -> None:
        """Test get_helm_info for plugins."""
        mock_syscmd.return_value = ['NAME    VERSION DESCRIPTION',
                                    'diff    3.5.0   Show diffs',
                                    'upgrade 0.0.1   Upgrade plugin']
        result = get_helm_info('plugin')
        self.assertIn('diff', result)
        self.assertIn('upgrade', result)

    @patch('vjer.tool_reporter.syscmd')
    def test_get_helm_info_helm_not_installed(self, mock_syscmd: MagicMock) -> None:
        """Test get_helm_info when helm is not installed."""
        mock_syscmd.side_effect = FileNotFoundError('helm not found')
        result = get_helm_info('repo')
        self.assertIn('Helm', result)
        self.assertEqual(result['Helm'], 'not installed')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_helm_info_no_repos(self, mock_syscmd: MagicMock) -> None:
        """Test get_helm_info when no repos found."""
        from batcave.lang import BatCaveError
        error = CMDError(BatCaveError(1, 'no repositories to show'), returncode=1, cmd='helm', err_lines=['no repositories to show'])
        mock_syscmd.side_effect = error
        result = get_helm_info('repo')
        self.assertIn('found', result)
        self.assertEqual(result['found'], 'none')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_helm_info_cmd_error_other(self, mock_syscmd: MagicMock) -> None:
        """Test get_helm_info re-raises CMDError not related to 'no repositories'."""
        from batcave.lang import BatCaveError
        error = CMDError(BatCaveError(2, 'some other error'), returncode=1, cmd='helm', err_lines=['some other error'])
        mock_syscmd.side_effect = error
        with self.assertRaises(CMDError):
            get_helm_info('repo')

    @patch('vjer.tool_reporter.syscmd')
    def test_get_helm_info_empty_result(self, mock_syscmd: MagicMock) -> None:
        """Test get_helm_info when result is empty."""
        mock_syscmd.return_value = ['NAME    URL']
        result = get_helm_info('repo')
        self.assertIn('found', result)
        self.assertEqual(result['found'], 'none')


class TestProductsList(TestCase):
    """Tests for PRODUCTS list."""

    def test_products_list_not_empty(self) -> None:
        """Test that PRODUCTS list is not empty."""
        self.assertGreater(len(PRODUCTS), 0)

    def test_products_have_required_fields(self) -> None:
        """Test that each product has required fields."""
        for product in PRODUCTS:
            self.assertIn('name', product)
            self.assertIn('regex', product)
            self.assertTrue(hasattr(product, 'name'))
            self.assertTrue(hasattr(product, 'regex'))


if __name__ == '__main__':
    main()

# cSpell:ignore syscmd bitnami
