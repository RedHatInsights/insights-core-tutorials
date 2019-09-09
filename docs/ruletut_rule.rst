.. _tutorial-custom_rule-development:

#######################################
Rule Using Existing Parser and Combiner
#######################################


Determine rule logic
====================

The most effective way to get started in developing a rule is first to identify the
problem you want to address.

For the purposes of this tutorial we'll look at a very simple scenario. Sometimes when
researching an issue we might need to know which Red Hat OS the host is running. For
simplicity's sake, in this example we will concentrate only on determining if the Red
Hat release is ``Fedora``.

For this case there is only one thing we need to check:

1. Is the Red Hat release ``Fedora``?


Identify Parsers
================

- We can check Red Hat release using the ``RedhatRelease`` parser.

Develop Plugin
==============

Now that we have identified the required parsers, let's get started on
developing our plugin.

Create a file called ``is_fedora.py`` in the ``mycomponents/rules`` directory.

.. code-block:: shell

    (env)[userone@hostone ~]$ cd ~/work/insights-core-tutorials/mycomponents/rules
    (env)[userone@hostone rules]$ touch is_fedora.py

Open ``is_fedora.py`` in your text editor of choice and start by stubbing out
the rule function and imports.

.. code-block:: python
    :linenos:

    from insights.parsers.redhat_release import RedhatRelease
    from insights import rule, make_fail, make_pass

    @rule(RedhatRelease)
    def report(rhrel):
        pass

Let's go over each line and describe the details:

.. code-block:: python
    :lineno-start: 1

    from insights.parsers.redhat_release import RedhatRelease

Parsers you want to use must be imported.  You must pass the parser class
objects directly to the ``@rule`` decorator to declare them as dependencies for
your rule.

.. code-block:: python
    :lineno-start: 2

    from insights import rule, make_fail, make_pass

``rule`` is a function decorator used to specify your main plugin function.
Combiners have a set of optional dependencies that are specified via the
``requires`` kwarg.

``make_fail, make_pass`` are formatting functions used to format
the `return value of a rule`_ function.

.. code-block:: python
    :lineno-start: 6

    ERROR_KEY_IS_FEDORA = "IS_FEDORA"

    CONTENT = {
        ERROR_KEY_IS_FEDORA: "This machine ({{hostname}}) runs {{product}}.",
    }

Here we defined the ``Jinja`` template for the message to be displayed for the
response tag for either pass or fail.


.. code-block:: python
    :lineno-start: 12

    @rule(RedhatRelease)

Here we are specifying that this rule requires the output of the
:py:class:`insights.parsers.redhat_release.RedhatRelease`,

Now let's add the rule logic

.. code-block:: python
    :lineno-start: 12

    @rule(RedhatRelease, content=CONTENT)
    def report(rhrel):
        """Fires if the machine is running Fedora."""

        if "Fedora" in rhrel.product:
            return make_pass(ERROR_KEY_IS_FEDORA, hostname=hostname.hostname, product=rhrel.product)
        else:
            return make_fail(ERROR_KEY_IS_FEDORA, hostname=hostname.hostname, product=rhrel.product)

Now let's look at what the rule is doing.

The ``RedhatRelease`` parser parses content from the ``/etc/redhat-release`` file on the
host it is running on and returns an object containing the Red Hat OS information for the
host.

.. code-block:: python
   :lineno-start: 16

        if "Fedora" in rhrel.product:
            return make_pass(ERROR_KEY_IS_FEDORA, hostname=hostname.hostname, product=rhrel.product)
        else:
            return make_fail(ERROR_KEY_IS_FEDORA, hostname=hostname.hostname, product=rhrel.product)

Here we check to see if the value ``Fedora`` is in the ``product`` property of the
``rhrel`` object. If true then the rule returns a response telling us that the host
is indeed running ``Fedora``, along with the product information returned by the
parser. If false then the rule returns a response telling us that the host is
not running ``Fedora``, along with the product information returned by the parser.


Develop Tests
=============

Start out by creating a ``test_is_fedora.py`` module in a ``tests`` package.

.. code-block:: shell

    (env)[userone@hostone ~]$ cd ~/work/insights-core-tutorials/rules/tests
    (env)[userone@hostone tests]$ touch __init__.py
    (env)[userone@hostone tests]$ touch test_is_fedora.py

Open ``test_is_fedora.py`` in your text editor of choice and start by stubbing
out a test and the required imports.

.. code-block:: python
    :linenos:

    from .. import is_fedora
    from insights.specs import Specs
    from insights.tests import InputData, archive_provider
    from insights.core.plugins import make_fail, make_pass


    @archive_provider(is_fedora.report)
    def integration_test():
        pass

The framework provides an integration test framework that allows you to define
an ``InputData`` object filled with raw examples of files required by your rule
and an expected response.  The object is evaluated by the pipeline as it would
be in a production context, after which the response is compared to your
expected output.

The ``@archive_provider`` decorator registers your test function with the
framework.  This function must be a generator that yields ``InputData`` and an
expected response in a two tuple.  The ``@archive_provider`` decorator takes
one parameter, the rule function to test.

The bulk of the work in building a test for a rule is in defining the
``InputData`` object.  If you remember our rule we accept ``RedhatRelease``.
We will define a data snippet for each test.

.. code-block:: python

    FEDORA = "Fedora release 28 (Twenty Eight)".strip()
    RHEL = "Red Hat Enterprise Linux Server release 7.4 (Maipo)".strip()
    TEST_HOSTNAME = "testhost.someplace.com"

Next for each test we need to build ``InputData`` objects and populate it with the content
and build the expected return. Then finally we need to yield the pair.

.. code-block:: python
    :lineno-start: 16

    input_data = InputData("test_fedora")
    input_data.add(Specs.redhat_release, FEDORA)
    input_data.add(Specs.hostname, TEST_HOSTNAME)
    expected = make_pass("IS_FEDORA", hostname=TEST_HOSTNAME, product="Fedora")

    yield input_data, expected

    input_data = InputData("test_rhel")
    input_data.add(Specs.redhat_release, RHEL)
    input_data.add(Specs.hostname, TEST_HOSTNAME)
    expected = make_fail("IS_FEDORA", hostname=TEST_HOSTNAME, product="Red Hat Enterprise Linux Server")

    yield input_data, expected


Now for the entire test:

.. code-block:: python
    :linenos:

    from .. import is_fedora
    from insights.specs import Specs
    from insights.tests import InputData, archive_provider
    from insights.core.plugins import make_fail, make_pass

    FEDORA = "Fedora release 28 (Twenty Eight)"
    RHEL = "Red Hat Enterprise Linux Server release 7.4 (Maipo)"
    TEST_HOSTNAME = "testhost.someplace.com"


    @archive_provider(is_fedora.report)
    def integration_test():

        input_data = InputData("test_fedora")
        input_data.add(Specs.redhat_release, FEDORA)
        input_data.add(Specs.hostname, TEST_HOSTNAME)
        expected = make_pass("IS_FEDORA", hostname=TEST_HOSTNAME, product="Fedora")


        yield input_data, expected

        input_data = InputData("test_rhel")
        input_data.add(Specs.redhat_release, RHEL)
        input_data.add(Specs.hostname, TEST_HOSTNAME)
        expected = make_fail("IS_FEDORA", hostname=TEST_HOSTNAME, product="Red Hat Enterprise Linux Server")

        yield input_data, expected

.. _return value of a rule:  https://insights-core.readthedocs.io/en/latest/api.html#rule-output

