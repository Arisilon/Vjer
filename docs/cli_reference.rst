CLI Reference
=============

Vjer is a CLI-first tool. The following help output is generated from the installed application so docs stay in sync with the code.

Top-level command
-----------------

.. programoutput:: python -m vjer --help
   :caption: Vjer top-level help
   :force:

Action reference
----------------

This project takes a single action argument with the supported actions listed below:

- `test`
- `build`
- `deploy`
- `rollback`
- `pre_release`
- `release`
- `freeze`

Because the CLI uses a positional action name rather than separate argparse subcommands, the top-level help is the primary generated usage output.
