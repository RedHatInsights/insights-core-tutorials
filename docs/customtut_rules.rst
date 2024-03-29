.. _tutorial-custom-rule-development:

########################
Rule Using Custom Parser
########################


********
Overview
********

The purpose of a rule is to evaluate various facts and determine one or more
results about a system.  For our example rule we are interested in knowing
whether a system with ``sshd`` is configured according to the following
guidelines::

    # Password based logins are disabled - only public key based logins are allowed.
    AuthenticationMethods publickey

    # LogLevel VERBOSE logs user's key fingerprint on login. Needed to have
    # a clear audit track of which key was using to log in.
    LogLevel VERBOSE

    # Root login is not allowed for auditing reasons. This is because it's
    # difficult to track which process belongs to which root user:
    PermitRootLogin No

    # Use only protocol 2 which is the default.  1 should not be listed
    # Protocol 2

We also want to know what version of OpenSSH we are running if we find any problems.

You can find the complete implementation of the rule and test code in the
directory ``insights-core-tutorials/insights_examples/rules``.

The same development environment will be used that was setup at the beginning
of the tutorial using the :ref:`tutorial-development-environment` section.


************************
Secure Shell Server Rule
************************

Rule Code
=========

First we need to create a template rule file.  It is recommended that
you name the file based on the results it produces.  Since we are looking
at sshd security we will name the file ``mycomponents/rules/sshd_secure.py``.
Notice that the file is located in the ``rules`` subdirectory
of your project::

    (env)[userone@hostone mycomponents]$ touch rules/sshd_secure.py

Here's the basic contents of the rule file:

.. code-block:: python
   :linenos:

   from insights.core.plugins import make_fail, rule
   from mycomponents.parsers.secure_shell import SSHDConfig

   ERROR_KEY = "SSHD_SECURE"


   @rule(SSHDConfig)
   def report(sshd_config):
       """
       1. Evaluate config file facts
       2. Evaluate version facts
       """
       if results_found:
           return make_fail(ERROR_KEY, results=the_results)

First we import the insights-core methods ``make_fail()`` for creating
a response and ``rule()`` to decorate our rule method so that it
will be invoked by insights-core with the appropriate parser information.
Then we import the parsers that provide the facts we need.

.. code-block:: python
   :linenos:

   from insights.core.plugins import make_fail, rule
   from mycomponents.parsers.secure_shell import SSHDConfig

Next we define a unique error key string, ``ERROR_KEY`` that will be
collected by insights-core when our rule is executed, and provided in the results for
all rules.  This string must be unique among all of your rules, or
the last rule to execute will overwrite any results from other rules
with the same key.

.. code-block:: python
   :linenos:
   :lineno-start: 4

   ERROR_KEY = "SSHD_SECURE"

.. _rule-decorator:

The ``@rule()`` decorator is used to mark the rule method that will be
invoked by insights-core.  Arguments to ``@rule()`` consist of the parser
and combiner objects that are necessary for rule processing.  Each object
may be either *required*, *at least one* from a list, or *optional*.  All *required*
objects must be available or the rule will not be called.  One or more objects from
the *at least one* list must be available or the rule will not be called. Zero
or more objects can be available from the *optional* list.

In the ``rule`` decorator required
objects are listed first, next are the "at least one" as a ``list`` argument,
and finally the optional object as a ``list`` using the keyword ``optional``.
For example if the a rule has the following input requirements:

============  ===============================
Criteria      ``@rule`` Decorator Arguments
============  ===============================
Requires      ``SSHDConfig, InstalledRpms``
At Least One  ``[ChkConfig, UnitFiles]``
Optional      ``optional=[IPTables, IpAddr]``
============  ===============================

The decorator for the rule and the rule signature will look like this:

.. code-block:: python
 
    @rule(SSHDConfig, InstalledRpms, [ChkConfig, UnitFiles], optional=[IPTables, IpAddr])
    def report(sshd_config, installed_rpms, chk_config, unit_files, ip_tables, ip_addr):
        # sshd_config and installed_rpms will always be present
        # at least one of chk_config and unit_files will be present
        # ip_tables and ip_addr will be present if data is available
        # arguments will be None if data is not available

Currently our rule requires one parser ``SSHDConfig``.  We will add a
requirement to obtain facts about installed RPMs in the final code.

.. code-block:: python
   :linenos:
   :lineno-start: 7

   @rule(SSHDConfig)

The name of our rule method is ``report``, but the name may be any valid
method name.
The purpose of the method is to evaluate the parser facts stored
in the parser object ``sshd_config``.  If any results
are found in the evaluation then a response is created with the
``ERROR_KEY`` and any data that you want to be associated with
the results are included in the response.
This data can be viewed in the results made available to a customer
in the Red Hat Insights web interface.
You may use zero or more named arguments to
provide the data to ``make_fail``.  You should use meaningful
argument names as it helps in understanding of the results.

.. code-block:: python
   :linenos:
   :lineno-start: 8

   def report(sshd_config):
       """
       1. Evaluate config file facts
       2. Evaluate version facts
       """
       if results_found:
           return make_fail(ERROR_KEY, results=the_results)

In order to perform the evaluation we need the facts for ``sshd_config``
and for the OpenSSH version.  The ``SSHDConfig`` parser we developed
will provide
the facts for ``sshd_config`` and we can use another parser,
``InstalledRpms`` to help us determine facts about installed software.

Here is our updated rule with check for the configuration options and
the software version:

.. code-block:: python
   :linenos:

   from insights.core.plugins import make_fail, rule
   from mycomponents.parsers.secure_shell import SSHDConfig
   from insights.parsers.installed_rpms import InstalledRpms

   ERROR_KEY = "SSHD_SECURE"


   @rule(InstalledRpms, SSHDConfig)
   def report(installed_rpms, sshd_config):
       errors = {}

       auth_method = sshd_config.last('AuthenticationMethods')
       if auth_method:
           if auth_method.lower() != 'publickey':
               errors['AuthenticationMethods'] = auth_method
       else:
           errors['AuthenticationMethods'] = 'default'

       log_level = sshd_config.last('LogLevel')
       if log_level:
           if log_level.lower() != 'verbose':
               errors['LogLevel'] = log_level
       else:
           errors['LogLevel'] = 'default'

       permit_root = sshd_config.last('PermitRootLogin')
       if permit_root:
           if permit_root.lower() != 'no':
               errors['PermitRootLogin'] = permit_root
       else:
           errors['PermitRootLogin'] = 'default'

       # Default Protocol is 2
       protocol = sshd_config.last('Protocol')
       if protocol:
           if protocol.lower() != '2':
               errors['Protocol'] = protocol

       if errors:
           openssh_version = installed_rpms.get_max('openssh')
           return make_fail(ERROR_KEY, errors=errors, openssh=openssh_version.package)

This rules code implements the checking of the four configuration values
``AuthenticationMethods``, ``LogLevel``, ``PermitRootLogin``, and ``Protocol``,
and returns any errors found using ``make_fail`` in the return. Also,
if errors are found, the ``InstalledRpms`` parser facts are queried to determine
the version of `OpenSSH` installed and that value is also returned.  If
no values are found then an implicit ``None`` is returned.

Now that we have the logic to check all of the rule conditions it is possible
to refactor the rule to make the condition checks more obvious.  This is sometimes
helpful in testing your rule as will be discussed below.  Here is the refactored
rule:

.. code-block:: python
   :linenos:

   from insights.core.plugins import make_fail, rule
   from insights.parsers.secure_shell import SSHDConfig
   from insights.parsers.installed_rpms import InstalledRpms

   ERROR_KEY = "SSHD_SECURE"


   def check_auth_method(sshd_config, errors):
       auth_method = sshd_config.last('AuthenticationMethods')
       if auth_method:
           if auth_method.lower() != 'publickey':
               errors['AuthenticationMethods'] = auth_method
       else:
           errors['AuthenticationMethods'] = 'default'
       return errors


   def check_log_level(sshd_config, errors):
       log_level = sshd_config.last('LogLevel')
       if log_level:
           if log_level.lower() != 'verbose':
               errors['LogLevel'] = log_level
       else:
           errors['LogLevel'] = 'default'
       return errors


   def check_permit_root(sshd_config, errors):
       permit_root = sshd_config.last('PermitRootLogin')
       if permit_root:
           if permit_root.lower() != 'no':
               errors['PermitRootLogin'] = permit_root
       else:
           errors['PermitRootLogin'] = 'default'
       return errors


   def check_protocol(sshd_config, errors):
       # Default Protocol is 2 if not specified
       protocol = sshd_config.last('Protocol')
       if protocol:
           if protocol.lower() != '2':
               errors['Protocol'] = protocol
       return errors


   @rule(InstalledRpms, SSHDConfig)
   def report(installed_rpms, sshd_config):
       errors = {}
       errors = check_auth_method(sshd_config, errors)
       errors = check_log_level(sshd_config, errors)
       errors = check_permit_root(sshd_config, errors)
       errors = check_protocol(sshd_config, errors)

       if errors:
           openssh_version = installed_rpms.get_max('openssh')
           return make_fail(ERROR_KEY, errors=errors, openssh=openssh_version.package)

To increase the readability of the rule output and possibly make the transition to insights content
format smoother, add Jinja2 formatting to the sshd_secure rule. Here is the refactored
code with the additional Jinja2 formatting:

.. code-block:: python
   :linenos:

   from insights.core.plugins import make_fail, rule
   from insights.parsers.secure_shell import SSHDConfig
   from insights.parsers.installed_rpms import InstalledRpms

   ERROR_KEY = "SSHD_SECURE"

   # Jinja2 template displayed for make_response results
   CONTENT =  ERROR_KEY + """
   :{
                    {% for key, value in errors.items() -%}
                        {{key}}: {{value}}
                    {% endfor -%} }
   OPEN_SSH_PACKAGE: {{openssh}}""".strip()


   def check_auth_method(sshd_config, errors):
       auth_method = sshd_config.last('AuthenticationMethods')
       if auth_method:
           if auth_method.lower() != 'publickey':
               errors['AuthenticationMethods'] = auth_method
       else:
           errors['AuthenticationMethods'] = 'default'
       return errors


   def check_log_level(sshd_config, errors):
       log_level = sshd_config.last('LogLevel')
       if log_level:
           if log_level.lower() != 'verbose':
               errors['LogLevel'] = log_level
       else:
           errors['LogLevel'] = 'default'
       return errors


   def check_permit_root(sshd_config, errors):
       permit_root = sshd_config.last('PermitRootLogin')
       if permit_root:
           if permit_root.lower() != 'no':
               errors['PermitRootLogin'] = permit_root
       else:
           errors['PermitRootLogin'] = 'default'
       return errors


   def check_protocol(sshd_config, errors):
       # Default Protocol is 2 if not specified
       protocol = sshd_config.last('Protocol')
       if protocol:
           if protocol.lower() != '2':
               errors['Protocol'] = protocol
       return errors


   @rule(InstalledRpms, SSHDConfig)
   def report(installed_rpms, sshd_config):
       errors = {}
       errors = check_auth_method(sshd_config, errors)
       errors = check_log_level(sshd_config, errors)
       errors = check_permit_root(sshd_config, errors)
       errors = check_protocol(sshd_config, errors)

       if errors:
           openssh_version = installed_rpms.get_max('openssh')
           return make_fail(ERROR_KEY, errors=errors, openssh=openssh_version.package)

Rule Testing
============

Testing is an important aspect of rule development and it helps ensure
accurate rule logic.  There are generally two types of testing to be
performed on rules, unit and integration testing.  If rule logic is
divided among multiple methods then unit tests should be written to
test the methods.  If there is only one method then unit tests may
not be necessary.  Integration tests are necessary to test the rule
in a simulated insights-core environment.  This will be easier to understand
by viewing the test code:

.. code-block:: python
   :linenos:

   from mycomponents.rules import sshd_secure
   from insights.tests import InputData, archive_provider, context_wrap
   from insights.core.plugins import make_fail
   from insights.specs import Specs
   # The following imports are not necessary for integration tests
   from mycomponents.parsers.secure_shell import SSHDConfig

   OPENSSH_RPM = """
   openssh-6.6.1p1-31.el7.x86_64
   openssh-6.5.1p1-31.el7.x86_64
   """.strip()

   EXPECTED_OPENSSH = "openssh-6.6.1p1-31.el7"

   GOOD_CONFIG = """
   AuthenticationMethods publickey
   LogLevel VERBOSE
   PermitRootLogin No
   # Protocol 2
   """.strip()

   BAD_CONFIG = """
   AuthenticationMethods badkey
   LogLevel normal
   PermitRootLogin Yes
   Protocol 1
   """.strip()

   DEFAULT_CONFIG = """
   # All default config values
   """.strip()



   @archive_provider(sshd_secure.report)
   def integration_tests():
       """
       InputData acts as the data source for the parsers
       so that they may execute and then be used as input
       to the rule.  So this is essentially an end-to-end
       test of the component chain.
       """
       input_data = InputData("GOOD_CONFIG")
       input_data.add(Specs.sshd_config, GOOD_CONFIG)
       input_data.add(Specs.installed_rpms, OPENSSH_RPM)
       yield input_data, None

       input_data = InputData("BAD_CONFIG")
       input_data.add(Specs.sshd_config, BAD_CONFIG)
       input_data.add(Specs.installed_rpms, OPENSSH_RPM)
       errors = {
           'AuthenticationMethods': 'badkey',
           'LogLevel': 'normal',
           'PermitRootLogin': 'Yes',
           'Protocol': '1'
       }
       expected = make_fail(sshd_secure.ERROR_KEY,
                                errors=errors,
                                openssh=EXPECTED_OPENSSH)
       yield input_data, expected

       input_data = InputData("DEFAULT_CONFIG")
       input_data.add(Specs.sshd_config, DEFAULT_CONFIG)
       input_data.add(Specs.installed_rpms, OPENSSH_RPM)
       errors = {
           'AuthenticationMethods': 'default',
           'LogLevel': 'default',
           'PermitRootLogin': 'default'
       }
       expected = make_fail(sshd_secure.ERROR_KEY,
                                errors=errors,
                                openssh=EXPECTED_OPENSSH)
       yield input_data, expected

Test Data
---------

Data utilized for all tests is defined in the test module.  In this
case we will use an OpenSSH RPM version that is present in RHEL 7.2,
``OPENSSH_RPM`` and three configuration files for ``sshd_config``.
``GOOD_CONFIG`` has all of the values that we are looking for and
should not return any error results.  ``BAD_CONFIG`` has all bad
values so it should return all error results.  And ``DEFAULT_CONFIG``
has no values present so it should return errors for all values
except ``Protocol`` which defaults to the correct value.

.. code-block:: python
   :linenos:
   :lineno-start: 8

   OPENSSH_RPM = """
   openssh-6.6.1p1-31.el7.x86_64
   openssh-6.5.1p1-31.el7.x86_64
   """.strip()

   EXPECTED_OPENSSH = "openssh-6.6.1p1-31.el7"

   GOOD_CONFIG = """
   AuthenticationMethods publickey
   LogLevel VERBOSE
   PermitRootLogin No
   # Protocol 2
   """.strip()

   BAD_CONFIG = """
   AuthenticationMethods badkey
   LogLevel normal
   PermitRootLogin Yes
   Protocol 1
   """.strip()

   DEFAULT_CONFIG = """
   # All default config values
   """.strip()


Integration Tests
-----------------

Integration tests are performed within the insights-core framework.  The
``InputData`` class is used to define the raw data that we want to be
present, and the framework creates an archive file to be input to
the insights-core framework so that the parsers will be invoked, and then
the rules will be invoked.  You need to create ``InputData`` objects
with all information that is necessary for parsers required
by your rules.  If input data is not present then parsers will not be
executed, and if your rule requires a missing parser it will not be executed.

To create your integration tests you must first create a method that
does not begin with ``test_`` and decorate that method with
``@archive_provider(rule_name)`` having an argument that is your
rule function name.  Typically we name the method ``integration_tests``.

.. code-block:: python
   :linenos:
   :lineno-start: 57

   @archive_provider(sshd_secure.report)
   def integration_tests():

Next we create an ``InputData`` object and it is useful to provide
a name argument to the constructor.  When you execute
integration tests, that name will show up in the results and make it
easier to debug if you have any problems. Next you add your test
inputs to the ``InputData`` object that will be used to create the
test archive. You add the data with the ``add`` method and identify
the source of the data using the data source spec that is associated
with the parser such as ``Specs.sshd_config``.
Once all of the data has been added, a ``yield``
statement provides the input data and expected results to the
``archive_provider`` to run the test.  In this particular test
case we provided all *good* data so we did not expect any results
``None``.

.. code-block:: python
   :linenos:
   :lineno-start: 59

       input_data = InputData("GOOD_CONFIG")
       input_data.add(Specs.sshd_config, GOOD_CONFIG)
       input_data.add(Specs.installed-rpms, OPENSSH_RPM)
       yield input_data, None

.. note:: If your input data has a path that is significant
    to the interpretation of the data, such as
    ``/etc/sysconfig/network-scripts/ifcfg-eth0`` where there may be
    multiple ``ifcfg`` scripts, you'll need to add the path as well.
    For example::

        input_data.add(Specs.ifcfg,
                       IFCFG_ETH0,
                       path="etc/sysconfig/network-scripts/ifcfg-eth0")
        input_data.add(Specs.ifcfg,
                       IFCFG_ETH1,
                       path="etc/sysconfig/network-scripts/ifcfg-eth1")

In the second test case we are using *bad* input data so we have to
also provide the errors that we expect our rule to return to the
framework.  The expected results are in the same format that we
create the return value in ``ssh_secure.report``.

.. code-block:: python
   :linenos:
   :lineno-start: 64

       input_data = InputData(name="BAD_CONFIG")
       input_data.add(Specs.sshd_config, BAD_CONFIG)
       input_data.add(Specs.installed-rpms, OPENSSH_RPM)
       errors = {
           'AuthenticationMethods': 'badkey',
           'LogLevel': 'normal',
           'PermitRootLogin': 'Yes',
           'Protocol': '1'
       }
       expected = make_fail(sshd_secure.ERROR_KEY,
                                errors=errors,
                                openssh=EXPECTED_OPENSSH)
       yield input_data, expected

Running the Tests
-----------------

We execute these tests by moving to the root directory of our rules
project, ensuring that our virtual environment is active, and running
``pytest``::

    (env)[userone@hostone mycomponents]$ pytest -k rules
    ====================== test session starts =============================================
    platform linux -- Python 3.6.6, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
    rootdir: /home/userone/work/insights-core-tutorials, inifile: setup.cfg
    plugins: cov-2.4.0
    collected 22 items / 8 deselected / 14 selected

    mycomponents/tests/integration.py .....                                                                                                                                                    [ 83%]
    =================== 14 passed, 8 deselected in 0.30 seconds ============================

You may also want to run the rule using ``insights-run``.
This will give you a better idea of what the output would be from the rule.
We execute this test by moving to the root directory (``insights-core-tutorials``),
ensuring that our virtual environment is active, and running
``insight-run -p rules/sshd_secure.py``::

    (insights-core)[userone@hostone mycomponents]$ insights-run -p rules/sshd_secure.py
    ---------
    Progress:
    ---------
    F

    --------------
    Rules Executed
    --------------
    [FAIL] rules.sshd_secure.report
    ------------------------
    SSHD_SECURE:
        errors : {'AuthenticationMethods': 'default',
                  'LogLevel': 'default',
                  'PermitRootLogin': 'default',
                  'Protocol': '1'}
        openssh: 'openssh-7.7p1-6.fc28'



    ----------------------
    Rule Execution Summary
    ----------------------
    Missing Deps: 0
    Passed      : 0
    Fingerprint : 0
    Failed      : 1
    Metadata    : 0
    Metadata Key: 0
    Exceptions  : 0



Note: If you have already built your parser in the ``mycomponents/parsers``
directory then you will see the following, otherwise you would only see
tests for rules...

If any tests fail you can use the following ``pytest`` ``-s -v --appdebug``
options to help get additional information.  If you want to limit which
test run you can also use the ``-k test_filter_string`` option.

.. --------------------------------------------------------------------
.. Put all of the references that are used throughout the document here
.. Links:

.. _Red Hat Customer Portal: https://access.redhat.com
.. _Red Hat Insights Portal: https://access.redhat.com/products/red-hat-insights.
.. _insights-core Repository: https://github.com/RedHatInsights/insights-core
.. _Mozilla OpenSSH Security Guidelines: https://wiki.mozilla.org/Security/Guidelines/OpenSSH
