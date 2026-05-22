"""Test Suite Documentation for Vjer CI/CD Toolkit

This document describes the comprehensive unittest test suite for the Vjer CI/CD toolkit.

## Test Coverage

The test suite includes the following test modules:

### 1. test_config.py
Tests for configuration-related classes and functionality.

**Classes Tested:**
- `Environment`: Tests for environment variable access
- `ConfigSection`: Tests for configuration section management
- `ProjectConfig`: Tests for project configuration loading and access
- `ConfigurationError`: Tests for custom exception handling

**Key Test Cases:**
- Environment variable reading
- Configuration section initialization and updates
- Configuration expansion and default values
- Project configuration sections (project, test, build, deploy, release)
- Error handling for missing configuration files and invalid schemas

### 2. test_utils.py
Tests for utility classes and functions in the utils module.

**Classes Tested:**
- `GitClient`: Tests for Git client functionality
- Utility runner functions: `git`, `helm`, `apt`, `apt_install`, `pip_install`

**Key Test Cases:**
- Git client initialization with various parameters
- Environment variable resolution for Git references and branch names
- GitHub, GitLab, and generic Git CI environment support
- Context manager behavior for GitClient
- Utility runner function definitions

### 3. test_vjer_step.py
Tests for the VjerStep class with extensive mocking.

**Classes Tested:**
- `VjerStep`: Core step execution class with Docker support
- `VjerStepDocker`: Docker-related operations

**Key Test Cases:**
- VjerStep initialization
- Attribute access patterns (project vs step_info)
- Property access (helm_chart_root, pkg_name, helm_args, helm_repo)
- Docker initialization and image tagging
- Helm repository and args configuration
- Error handling for invalid attributes

### 4. test_tool_reporter.py
Tests for tool discovery and version reporting.

**Functions Tested:**
- `tool_reporter()`: Main reporting function
- `get_version()`: Version extraction for various tools
- `get_helm_info()`: Helm repository and plugin information

**Key Test Cases:**
- Tool version detection for Docker, Google Cloud SDK, and Helm
- Regex pattern matching for version strings
- Handling of missing tools (FileNotFoundError)
- Error handling for command failures
- Helm repository and plugin listing
- Raw output vs parsed output modes

### 5. test_vjer_module.py
Tests for Vjer module metadata and version information.

**Module Attributes Tested:**
- `__title__`: Module title
- `__version__`: Semantic version format
- `__author__`: Author information
- `__license__`: License type
- `__copyright__`: Copyright information
- `__build_name__` and `__build_date__`: Build metadata
- `__all__`: Exported symbols

**Key Test Cases:**
- Module metadata consistency
- Version format validation (semantic versioning)
- Version component parsing and ranges
- String attribute non-emptiness
- Module import functionality

### 6. test_test_module.py
Tests for the test action module (vjer.test).

**Classes Tested:**
- `TestStep`: Test execution step class

**Key Test Cases:**
- TestStep initialization
- Test results directory preparation
- Parent class method invocation
- Individual test runner methods (test_flake8, test_mypy, test_pylint)
- Helm chart testing
- Docker linting

### 7. test_integration.py
Integration and utility constant tests.

**Constants Tested:**
- `_CONFIG_SECTIONS`: Configuration sections definition
- `_PROJECT_DEFAULTS`: Default project configuration values
- `PROJECT_CFG_FILE`: Configuration file path
- `TOOL_REPORT`: Tool report path
- `DEFAULT_VERSION_FILES`: Version file patterns
- Exception hierarchy and error types

**Key Test Cases:**
- Configuration constant validation
- Default value correctness
- Exception class hierarchy
- List and dict attribute expansion in ConfigSection
- Environment variable handling

## Running the Tests

### Run All Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Run Specific Test Module
```bash
python -m unittest tests.test_config -v
python -m unittest tests.test_utils -v
python -m unittest tests.test_vjer_step -v
python -m unittest tests.test_tool_reporter -v
python -m unittest tests.test_vjer_module -v
python -m unittest tests.test_test_module -v
python -m unittest tests.test_integration -v
```

### Run Specific Test Class
```bash
python -m unittest tests.test_config.TestEnvironment -v
python -m unittest tests.test_config.TestConfigSection -v
python -m unittest tests.test_utils.TestGitClient -v
```

### Run Specific Test Method
```bash
python -m unittest tests.test_config.TestEnvironment.test_environment_getattr_existing_variable -v
```

### Using Vjer Test Command
The project's test command will run the test suite:
```bash
vjer test
```

### Run Tests with Coverage
```bash
pip install coverage
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report
coverage html
```

## Test Statistics

- **Total Test Modules**: 7
- **Approximate Total Test Cases**: 100+
- **Code Coverage**: Targets high coverage of public API and core functionality

## Mocking Strategy

The test suite uses extensive mocking to:
1. Isolate units under test
2. Avoid external dependencies (Git, Docker, Helm, etc.)
3. Test error conditions safely
4. Provide deterministic test execution

Key mocked components:
- `ProjectConfig`: Configuration file I/O
- `GitClient`: Git repository operations
- `docker.client`: Docker operations
- `sys.syscmd`: System commands
- `pathlib.Path`: File system operations

## Test Development Guidelines

### Adding New Tests
1. Create a new test class inheriting from `unittest.TestCase`
2. Use descriptive names: `test_<component>_<scenario>`
3. Use `setUp()` method for test fixture initialization
4. Mock external dependencies appropriately
5. Include both positive and negative test cases
6. Add docstrings to test methods

### Best Practices
1. One assertion per test method (or use `assert*` comprehensively)
2. Use `@patch` decorators for mocking external dependencies
3. Test both success and failure paths
4. Include edge cases and boundary conditions
5. Keep tests focused and independent
6. Use descriptive assertion messages

### Running Tests During Development
```bash
# Watch for changes and run tests automatically
pytest-watch tests/

# Run with verbose output
python -m unittest -v

# Run with debugging
python -m pdb -m unittest tests.test_config.TestEnvironment
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 5 seconds for most tests)
- No external dependencies required
- Proper error reporting
- Exit codes for CI integration

## Future Test Expansion

Potential areas for additional test coverage:
1. VjerAction and action lifecycle testing
2. Deploy and release module testing
3. Build module testing with various build systems
4. Version management and update testing
5. File operation and artifact management testing
6. Configuration file parsing with various schemas
7. Complex integration scenarios

## Contributing Tests

When contributing new tests:
1. Ensure tests pass locally before submission
2. Maintain > 80% code coverage
3. Add tests for bug fixes (regression tests)
4. Document complex test setups
5. Follow existing naming conventions
6. Update this documentation for new test modules
"""
