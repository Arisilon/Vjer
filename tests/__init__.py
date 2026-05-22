"""Test suite for the Vjer CI/CD toolkit."""

__all__ = ['test_config', 'test_utils', 'test_tool_reporter', 'test_vjer_module']

import sys
from pathlib import Path

# Ensure the local source tree takes precedence over any installed version
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Force reimport of vjer from the local source
if 'vjer' in sys.modules:
    # Remove all vjer submodules from the cache
    for mod_name in list(sys.modules):
        if mod_name == 'vjer' or mod_name.startswith('vjer.'):
            del sys.modules[mod_name]
