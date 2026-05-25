"""Tests for vjer module metadata and version."""

# pylint: disable=missing-class-docstring,missing-function-docstring,invalid-name
# flake8: noqa

from unittest import TestCase, main

import vjer
from vjer import (__title__, __summary__, __uri__,
                  __version__, __build_name__, __build_date__,
                  __author__, __email__,
                  __license__, __copyright__, __all__)


class TestVjerModule(TestCase):
    """Tests for vjer module metadata."""

    def test_module_title(self) -> None:
        """Test module title."""
        self.assertEqual(__title__, 'Vjer')
        self.assertIsInstance(__title__, str)

    def test_module_summary(self) -> None:
        """Test module summary."""
        self.assertEqual(__summary__, 'CI/CD Toolkit')
        self.assertIsInstance(__summary__, str)

    def test_module_uri(self) -> None:
        """Test module URI."""
        self.assertIn('github.com', __uri__)
        self.assertIn('vjer', __uri__)
        self.assertIsInstance(__uri__, str)

    def test_module_version(self) -> None:
        """Test module version format."""
        # Version should follow semantic versioning pattern
        self.assertRegex(__version__, r'^\d+\.\d+\.\d+')
        self.assertIsInstance(__version__, str)

    def test_module_build_name(self) -> None:
        """Test module build name."""
        self.assertIsInstance(__build_name__, str)

    def test_module_build_date(self) -> None:
        """Test module build date."""
        self.assertIsInstance(__build_date__, str)

    def test_module_author(self) -> None:
        """Test module author."""
        self.assertEqual(__author__, 'Jeffery G. Smith')
        self.assertIsInstance(__author__, str)

    def test_module_email(self) -> None:
        """Test module email."""
        self.assertEqual(__email__, 'web@pobox.com')
        self.assertIsInstance(__email__, str)

    def test_module_license(self) -> None:
        """Test module license."""
        self.assertEqual(__license__, 'MIT')
        self.assertIsInstance(__license__, str)

    def test_module_copyright(self) -> None:
        """Test module copyright."""
        self.assertIn('Copyright', __copyright__)
        self.assertIn('Jeffery G. Smith', __copyright__)
        self.assertIsInstance(__copyright__, str)

    def test_module_all_exports(self) -> None:
        """Test __all__ contains expected exports."""
        expected_exports = {'__title__', '__summary__', '__uri__',
                            '__version__', '__build_name__', '__build_date__',
                            '__author__', '__email__',
                            '__license__', '__copyright__'}
        self.assertEqual(set(__all__), expected_exports)

    def test_module_can_be_imported(self) -> None:
        """Test that vjer module can be imported."""
        self.assertIsNotNone(vjer)

    def test_module_attributes_are_strings(self) -> None:
        """Test that all module attributes are strings."""
        attributes = [__title__, __summary__, __uri__,
                      __version__, __build_name__, __build_date__,
                      __author__, __email__,
                      __license__, __copyright__]
        for attr in attributes:
            self.assertIsInstance(attr, str,f'Expected string, got {type(attr).__name__}')

    def test_module_non_empty_strings(self) -> None:
        """Test that all module attributes are non-empty strings."""
        attributes = {'__title__': __title__,
                      '__summary__': __summary__,
                      '__uri__': __uri__,
                      '__version__': __version__,
                      '__author__': __author__,
                      '__email__': __email__,
                      '__license__': __license__,
                      '__copyright__': __copyright__}
        for attr_name, attr_value in attributes.items():
            self.assertTrue(len(attr_value) > 0, f'{attr_name} should not be empty')


class TestVjerModuleVersion(TestCase):
    """Tests for vjer module version format."""

    def test_version_major_component(self) -> None:
        """Test version has major component."""
        major = __version__.split('.', maxsplit=1)[0]
        self.assertTrue(major.isdigit())

    def test_version_minor_component(self) -> None:
        """Test version has minor component."""
        minor = __version__.split('.')[1]
        self.assertTrue(minor.isdigit())

    def test_version_patch_component(self) -> None:
        """Test version has patch component."""
        patch = __version__.split('.')[2]
        # Patch can be numeric or contain pre-release identifiers
        self.assertTrue(len(patch) > 0)

    def test_version_reasonable_range(self) -> None:
        """Test version components are in reasonable ranges."""
        parts = __version__.split('.')
        self.assertGreaterEqual(int(parts[0]), 0)
        self.assertGreaterEqual(int(parts[1]), 0)


if __name__ == '__main__':
    main()
