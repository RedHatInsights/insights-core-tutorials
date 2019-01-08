.. _tutorial-development-environment:

Preparing Your Development Environment
======================================

First you need to ensure you have the ``git`` and ``gcc`` tools available. 
On Red Hat Enterprise Linux you can do this with the command, as root: ``yum install git gcc``.

Now create your own fork of the insights-core project.  Do this by
going to the `insights-core-tutorials` Repository on GitHub and clicking on the
**Fork** button.

You will now have an *insights-core-tutorials* repository under your GitHub user that
you can use to checkout the code to your development environment.  To check
out the code go to the repository page for your fork and copy the link to
download the repo.

Once you have copied this link then go to a terminal in your working directory
and use the ``git`` command to clone the repository.  In this example the
working directory is ``/home/userone/github``::

    [userone@hostone ~]$ mkdir github
    [userone@hostone ~]$ cd github
    [userone@hostone work]$ git clone https://github.com/RedHatInsights/insights-core-tutorials.git
    Cloning into 'insights-core-tutorials'...
    remote: Counting objects: 21251, done.
    remote: Compressing objects: 100% (88/88), done.
    remote: Total 21251 (delta 68), reused 81 (delta 43), pack-reused 21118
    Receiving objects: 100% (21251/21251), 5.95 MiB | 2.44 MiB/s, done.
    Resolving deltas: 100% (15938/15938), done.

Next you need to follow the steps to create a virtual environment and set it up for development::

    [userone@hostone work]$ cd insights-core-tutorials
    [userone@hostone insights-core-tutorials]$ virtualenv -p python3.6 .
    Running virtualenv with interpreter /usr/bin/python3.6
    Using base prefix '/usr'
    New python executable in /home/userone/github/insights-core-tutorials/bin/python3.6
    Also creating executable in /home/userone/github/insights-core-tutorials/bin/python
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

Once these steps have been completed you will have a complete development
environment for parsers and combiners.  You can confirm that everything is setup
correctly by running the tests, ``pytest``.  This will test the components in the 
``insights_examples`` directory. 
Your results should look something like this::

   (env)[userone@hostone insights-core-tutorials]$ pytest
   ========================================================================================= test session starts ================================================================================================
   platform linux -- Python 3.6.6, pytest-3.0.6, py-1.7.0, pluggy-0.4.0
   rootdir: /home/lhuett/gitlab/insights-core-tutorials, inifile: setup.cfg
   plugins: cov-2.6.0
   collected 8 items 

   insights_examples/combiners/tests/test_hostname_uh.py .
   insights_examples/parsers/tests/test_secure_shell.py ...
   insights_examples/rules/tests/integration.py ...
   insights_examples/rules/tests/test_sshd_secure.py .

   ====================================================================================== 10 passed in 0.30 seconds ==============================================================================================

If during this step you see a test failure similar to the following make sure
you have ``unzip`` installed on your system::
    
    >           raise child_exception
    E           CalledProcessError: <CalledProcessError(0, ['unzip', '-q', '-d',
    '/tmp/tmplrXhIu', '/tmp/test.zip'], [Errno 2] No such file or directory)>

    /usr/lib64/python2.7/subprocess.py:1327: CalledProcessError

Next you will need to create ``mycomponents`` directory and directories to develop
each of the components (parsers, combiners and rules) in.

Here are the commands to complete the development environment for each component::

    (env)[userone@hostone ~]$ cd ~/github/insights-core-tutorials
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

    (env)[userone@hostone mycomponents]$ export PYTHONPATH=~/github/insights-core-tutorials/mycomponents:$PYTHONPATH

.. _set_cfg_for_mycomponents:
    
As you build your components and tests you will want to run the tests. If you would like to disable the running of 
the tests located in the insights_examples directory and only run the tests located in your newly created ``mycomponents`` 
directory, edit the setup.cfg in the ``insights-core-tutorials`` root directory as follows.

Replace ``insights_examples/*`` in the following line with ``mycomponents/*``::
   ``python_files = "insights_examples/*"``
It should look like this now::
   ``python_files = "mycomponents/*"``

Replace ``insights_examples`` in the following line with ``mycomponents``::
   ``testpaths = "insights_examples"``
It should look like this now::
   ``testpaths = "mycomponents"`` 


Your development environment is now ready to begin development and you may move
on to the next section.  If you had problems with any of these steps then
double check that you have completed all of the steps in order and if it still
doesn't work, open a `GitHub issue <https://github.com/RedHatInsights/insights-core/issues/new>`_.
