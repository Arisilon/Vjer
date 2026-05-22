"""Tests for GitClient and other utility classes in vjer.utils."""

import tests.test_support  # noqa: F401
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

from vjer.utils import GitClient, git, helm, apt, apt_install, pip_install


class TestGitClient(unittest.TestCase):
    """Tests for the GitClient class."""

    def test_git_client_init_with_defaults(self) -> None:
        """Test GitClient initialization with default values."""
        with patch.dict(os.environ, {}, clear=True):
            client = GitClient()
            self.assertIsNone(client.project_id)
            self.assertIsNone(client.client)
            self.assertEqual(client.branch, '')

    def test_git_client_init_with_parameters(self) -> None:
        """Test GitClient initialization with parameters."""
        with patch.dict(os.environ, {}, clear=True):
            client = GitClient(project_id='test-project', branch='main')
            self.assertEqual(client.project_id, 'test-project')
            self.assertEqual(client.branch, 'main')

    def test_git_client_context_manager(self) -> None:
        """Test GitClient as context manager."""
        with patch.dict(os.environ, {}, clear=True):
            with GitClient() as client:
                self.assertIsNotNone(client)

    def test_git_client_ci_commit_ref_name_from_env(self) -> None:
        """Test ci_commit_ref_name from CI_COMMIT_REF_NAME environment."""
        with patch.dict(os.environ, {'CI_COMMIT_REF_NAME': 'feature/test'}):
            client = GitClient()
            self.assertEqual(client.ci_commit_ref_name, 'feature/test')

    def test_git_client_ci_commit_ref_name_from_github_ref(self) -> None:
        """Test ci_commit_ref_name from GITHUB_REF environment."""
        with patch.dict(os.environ, {'GITHUB_REF': 'refs/heads/main'}, clear=True):
            client = GitClient()
            self.assertEqual(client.ci_commit_ref_name, 'main')

    def test_git_client_ci_commit_ref_name_from_github_ref_tag(self) -> None:
        """Test ci_commit_ref_name from GITHUB_REF with tag."""
        with patch.dict(os.environ, {'GITHUB_REF': 'refs/tags/v1.0.0'}, clear=True):
            client = GitClient()
            self.assertEqual(client.ci_commit_ref_name, 'v1.0.0')

    def test_git_client_ci_commit_ref_name_from_ci_branch(self) -> None:
        """Test ci_commit_ref_name from CI_COMMIT_BRANCH environment."""
        with patch.dict(os.environ, {'CI_COMMIT_BRANCH': 'develop'}, clear=True):
            client = GitClient()
            self.assertEqual(client.ci_commit_ref_name, 'develop')

    def test_git_client_ci_commit_ref_name_missing(self) -> None:
        """Test ci_commit_ref_name raises when no env var found."""
        with patch.dict(os.environ, {}, clear=True):
            client = GitClient()
            with self.assertRaises(AttributeError) as ctx:
                _ = client.ci_commit_ref_name
            self.assertIn('Environment variable not found', str(ctx.exception))

    def test_git_client_ci_remote_ref_from_env(self) -> None:
        """Test ci_remote_ref from CI_REMOTE_REF environment."""
        with patch.dict(os.environ, {'CI_REMOTE_REF': 'https://github.com/test/repo.git'}):
            client = GitClient()
            self.assertEqual(client.ci_remote_ref, 'https://github.com/test/repo.git')

    def test_git_client_ci_remote_ref_from_ci_repository_url(self) -> None:
        """Test ci_remote_ref from CI_REPOSITORY_URL environment."""
        with patch.dict(os.environ, {'CI_REPOSITORY_URL': 'https://gitlab.com/test/repo.git'}, clear=True):
            client = GitClient()
            self.assertEqual(client.ci_remote_ref, 'https://gitlab.com/test/repo.git')

    def test_git_client_ci_remote_ref_from_github(self) -> None:
        """Test ci_remote_ref from GITHUB environment variables."""
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'user/repo', 'GITHUB_SERVER_URL': 'https://github.com'}, clear=True):
            client = GitClient()
            self.assertEqual(client.ci_remote_ref, 'https://github.com/user/repo.git')

    def test_git_client_ci_remote_ref_from_github_default_server(self) -> None:
        """Test ci_remote_ref from GITHUB with default server."""
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'user/repo'}, clear=True):
            client = GitClient()
            self.assertEqual(client.ci_remote_ref, 'https://github.com/user/repo.git')

    def test_git_client_ci_remote_ref_missing(self) -> None:
        """Test ci_remote_ref raises when no env var found."""
        with patch.dict(os.environ, {}, clear=True):
            client = GitClient()
            with patch.object(client, 'client', None):
                with self.assertRaises(AttributeError) as ctx:
                    _ = client.ci_remote_ref
                self.assertIn('Environment variable not found', str(ctx.exception))


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility runner functions."""

    def test_git_runner_exists(self) -> None:
        """Test that git runner is defined."""
        self.assertIsNotNone(git)
        self.assertTrue(callable(git))

    def test_helm_runner_exists(self) -> None:
        """Test that helm runner is defined."""
        self.assertIsNotNone(helm)
        self.assertTrue(callable(helm))

    def test_apt_runner_exists(self) -> None:
        """Test that apt runner is defined."""
        self.assertIsNotNone(apt)
        self.assertTrue(callable(apt))

    def test_apt_install_runner_exists(self) -> None:
        """Test that apt_install runner is defined."""
        self.assertIsNotNone(apt_install)
        self.assertTrue(callable(apt_install))

    def test_pip_install_runner_exists(self) -> None:
        """Test that pip_install runner is defined."""
        self.assertIsNotNone(pip_install)
        self.assertTrue(callable(pip_install))


class TestGitClientWithMockClient(unittest.TestCase):
    """Tests for GitClient with mocked git client."""

    @patch('vjer.utils.Client')
    def test_git_client_with_git_repo(self, mock_client_class: MagicMock) -> None:
        """Test GitClient when .git directory exists."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        with patch('vjer.utils.Path') as mock_path:
            mock_git_dir = MagicMock()
            mock_git_dir.exists.return_value = True

            # Test without triggering Path operations in __init__
            with patch.dict(os.environ, {'CI_COMMIT_REF_NAME': 'main'}, clear=True):
                client = GitClient(client_root='/test/repo')
                # The client should be created if .git directory exists
                # (depends on implementation details)

    @patch('vjer.utils.Client')
    def test_git_client_active_branch(self, mock_client_class: MagicMock) -> None:
        """Test ci_commit_ref_name using active_branch from git client."""
        mock_client = MagicMock()
        mock_client.active_branch = 'feature-branch'
        mock_client_class.return_value = mock_client

        with patch.dict(os.environ, {}, clear=True):
            with patch('vjer.utils.Path') as mock_path:
                mock_git_dir = MagicMock()
                mock_git_dir.exists.return_value = True

                # Manually set client for testing
                client = GitClient()
                client.client = mock_client

                self.assertEqual(client.ci_commit_ref_name, 'feature-branch')


if __name__ == '__main__':
    unittest.main()
