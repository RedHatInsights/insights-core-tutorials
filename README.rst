=======================
Insights Core Tutorials
=======================

This repository provides tutorials and examples of how to build and test_secure_shell Insights Core Parsers
, Combiners and Rules.

Follow the tutorial links below to step through each section to go through the process of creating and running
each of the components represented in the "insights_examples" directory.

The process to create the files contained in the ``insights-core-tutorials/insights_examples`` directory are described
in detail in the tutorials:

  - `Insights Core Tutorials Read the Docs
    <http://insights-core-tutorials.readthedocs.io>`_


If you would like to just run pytest for the examples follow the ``Preparing Your Development Environment`` section of
``Insights Core Tutorials Read the Docs`` to create the environment and run the pytests.

The examples directory includes these files::

    insights_examples
    ├── combiners
    │   ├── hostname_uh.py
    │   └── __init__.py
    ├── __init__.py
    ├── parsers
    │   ├── __init__.py
    │   └── secure_shell.py
    ├── rules
    │   ├── bash_bug.py
    │   ├── __init__.py
    │   ├── is_fedora.py
    │   └── sshd_secure.py
    └── tests
        ├── combiners
        │   ├── __init__.py
        │   └── test_hostname_uh.py
        ├── __init__.py
        ├── integration.py
        ├── parsers
        │   ├── __init__.py
        │   └── test_secure_shell.py
        └── rules
            ├── __init__.py
            ├── test_bash_bug.py
            ├── test_is_fedora.py
            └── test_sshd_secure.py
