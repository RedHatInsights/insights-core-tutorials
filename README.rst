=======================
Insights Core Tutorials
=======================

This repository provides tutorialis and examples of how to build and test_secure_shell Insights Core Parsers
, Combiners and Rules.

Follow the tutorial links below to step through each dection to go through the process of creating and running
each of the components represented in the insights-examples directory.

The process to create the files contained in the ``insights-core-tutorials/insights_examples`` directory are described
in detail in the tutorials:

  - `Insights Core Tutorials Read the Docs
    <http://insights-core-tutorial.readthedocs.io>`_


If you would like to just run the examples follow the ``Preparing Your Development Environment`` to create the 
environment and run the pytest, this test runs the test for the components in the 
``insights-core-tutorials/insights-examples`` directory structure.

The examples directory includes these files::
    
    insights-examples
    ├── combiners
    │   ├── hostname_uh.py
    │   ├── __init__.py
    │   └── tests
    │       ├── __init__.py
    │       └── test_hostname_uh.py
    ├── parsers
    │   ├── __init__.py
    │   ├── secure_shell.py
    │   └── tests
    │       ├── __init__.py
    │       └── test_secure_shell.py
    ├── README.rst
    └── rules
        ├── __init__.py
        ├── sshd_secure.py
        ├── is_fedora.py
        └── tests
            ├── __init__.py
            ├── integration.py
            ├── test_sshd_secure.py
            └── test_is_fedora.py
            


