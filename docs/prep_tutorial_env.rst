.. _tutorial-development-environment:

Preparing Your Development Environment
======================================

First you need to ensure you have the ``git`` and ``gcc`` tools available. 
On Red Hat Enterprise Linux you can do this with the command, as root: ``yum install git gcc``.

Now create your own fork of the insights-core-tutorials project. Do this by
going to the `insights-core-tutorials` Repository on GitHub and clicking on the
**Fork** button.

You will now have an *insights-core-tutorials* repository under your GitHub user that
you can use to checkout the code to your development environment.  To check
out the code go to the repository page for your fork and copy the link to
download the repo.

Once you have copied this link then go to a terminal in your working directory
and use the ``git`` command to clone the repository.  In this tutorial we will be using 
``work`` as the directory that will contain the ``isights-core-tutorials`` project.
If you choose to use a different root directory you will need to substitute ``work``
with your chosen root directory when referenced in the tutorial. So for the puposes of 
this document our working directory is ``/home/userone/work``::

    [userone@hostone ~]$ mkdir work
    [userone@hostone ~]$ cd work
    [userone@hostone work]$ git clone git@github.com:userone/insights-core-tutorials.git
    Cloning into 'insights-core-tutorials'...
    remote: Counting objects: 21251, done.
    remote: Compressing objects: 100% (88/88), done.
    remote: Total 21251 (delta 68), reused 81 (delta 43), pack-reused 21118
    Receiving objects: 100% (21251/21251), 5.95 MiB | 2.44 MiB/s, done.
    Resolving deltas: 100% (15938/15938), done.

Next you need to run the ``setup_env.sh`` script to set up your python environment.

If you have used the script to setup you environment you can skip the maual setup instructions 
and go straight to the .

Else, if you would rather create the python environment manaually you can follow these steps 
to create a virtual environment and set it up for development::

    [userone@hostone work]$ cd insights-core-tutorials
    [userone@hostone insights-core-tutorials]$ virtualenv -p python3.6 .
    Running virtualenv with interpreter /usr/bin/python3.6
    Using base prefix '/usr'
    New python executable in /home/userone/work/insights-core-tutorials/bin/python3.6
    Also creating executable in /home/userone/work/insights-core-tutorials/bin/python
    Installing setuptools, pip, wheel...done.

    New python executable in ./bin/python
    Installing Setuptools..................................................done.
    Installing Pip....................................................done.
    
Setup your environment to use the new virtualenv you just created, and upgrade
``pip`` to the latest version::
    
    [userone@hostone insights-core-tutorials]$ source ./bin/activate
    (env)[userone@hostone insights-core-tutorials]$ pip install --upgrade pip
    
Now install all of the required packages for ``insights-core-tutorials`` development::
    
    (env)[userone@hostone insights-core-tutorials]$ pip install -e .[develop]

Next you will need to create ``mycomponents`` directory and directories to develop
each of the components (parsers, combiners and rules) in.

.. _set_cfg_for_mycomponents:

The following are the commands to create the ``mycomponents`` development environment
for each component::

    (env)[userone@hostone ~]$ cd ~/work/insights-core-tutorials
    (env)[userone@hostone insights-core-tutorials]$ mkdir mycomponents
    (env)[userone@hostone insights-core-tutorials]$ cd mycomponents
    (env)[userone@hostone mycomponents]$ touch __init__.py
    (env)[userone@hostone mycomponents]$ mkdir parsers
    (env)[userone@hostone mycomponents]$ touch ./parsers/__init__.py
    (env)[userone@hostone mycomponents]$ mkdir ./parsers/tests
    (env)[userone@hostone mycomponents]$ touch ./parsers/tests/__init__.py
    (env)[userone@hostone mycomponents]$ mkdir combiners
    (env)[userone@hostone mycomponents]$ touch ./combiners/__init__.py
    (env)[userone@hostone mycomponents]$ mkdir ./combiners/tests
    (env)[userone@hostone mycomponents]$ touch ./combiners/tests/__init__.py
    (env)[userone@hostone mycomponents]$ mkdir rules
    (env)[userone@hostone mycomponents]$ touch ./rules/__init__.py
    (env)[userone@hostone mycomponents]$ mkdir ./rules/tests
    (env)[userone@hostone mycomponents]$ touch ./rules/tests/__init__.py

    (env)[userone@hostone mycomponents]$ export PYTHONPATH=~/work/insights-core-tutorials/mycomponents:$PYTHONPATH


Once you have completed the setup of the environment by either running the provided script
or running the preceeding setup steps manually, you will have a complete development
environment for rules, parsers, combiners and for your mycomonents development directory.

You can now confirm that everything is setup correctly so far by running the tests, ``pytest``.

This will test the components in the ``insights_examples`` directory.
Your results should look something like this::

   (env)[userone@hostone insights-core-tutorials]$ pytest
   ================================================================== test session starts ===================================================================
   platform linux -- Python 3.6.6, pytest-4.0.1, py-1.7.0, pluggy-0.8.0
   rootdir: /home/userone/work/insights-core-tutorials, inifile: setup.cfg
   plugins: cov-2.6.1
   collected 10 items

   insights_examples/combiners/tests/test_hostname_uh.py .
   insights_examples/parsers/tests/test_secure_shell.py ...
   insights_examples/rules/tests/integration.py ...
   insights_examples/rules/tests/test_sshd_secure.py .

   ============================================================== 10 passed in 0.30 seconds =================================================================

If during this step you see a test failure similar to the following make sure
you have ``unzip`` installed on your system::

    >           raise child_exception
    E           CalledProcessError: <CalledProcessError(0, ['unzip', '-q', '-d',
    '/tmp/tmplrXhIu', '/tmp/test.zip'], [Errno 2] No such file or directory)>

    /usr/lib64/python2.7/subprocess.py:1327: CalledProcessError

Your development environment is now ready to begin development and you may move
on to the next section.  If you had problems with any of these steps then
double check that you have completed all of the steps in order and if it still
doesn't work, open a `GitHub issue <https://github.com/RedHatInsights/insights-core/issues/new>`_.
