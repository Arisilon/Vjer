"""Test support helpers for unit tests."""

import sys
import types
from unittest.mock import MagicMock

# Stub components that are not available in all environments.
batcave_cms = types.SimpleNamespace(
    Client=MagicMock(return_value=MagicMock()),
    ClientType=MagicMock()
)
sys.modules['batcave.cms'] = batcave_cms

# Stub bumpver config to avoid import and runtime package dependency.
bumpver_module = types.ModuleType('bumpver')
bumpver_config_module = types.ModuleType('bumpver.config')
def bumpver_init():
    return (None, types.SimpleNamespace(current_version='1.0.0'))
bumpver_config_module.init = bumpver_init
sys.modules['bumpver'] = bumpver_module
sys.modules['bumpver.config'] = bumpver_config_module

# Stub flit builder to avoid runtime package dependency.
flit_module = types.ModuleType('flit')
flit_build_module = types.ModuleType('flit.build')
def flit_main(path):
    return None
flit_build_module.main = flit_main
sys.modules['flit'] = flit_module
sys.modules['flit.build'] = flit_build_module

# Stub junitparser and xmlrunner for tests that import vjer.test.
sys.modules['junitparser'] = types.SimpleNamespace(JUnitXml=MagicMock())
sys.modules['xmlrunner'] = types.SimpleNamespace(XMLTestRunner=MagicMock(return_value=MagicMock(run=MagicMock())))
