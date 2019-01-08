from .. import is_fedora
from insights.specs import Specs
from insights.tests import InputData, archive_provider
from insights.core.plugins import make_response
# from insights.tests.integration import generate_tests, test_integration
# import pytest

FEDORA = "Fedora release 28 (Twenty Eight)"
RHEL = "Red Hat Enterprise Linux Server release 7.4 (Maipo)"


@archive_provider(is_fedora.report)
def integration_test():

    input_data = InputData("test_fedora")
    input_data.add(Specs.redhat_release, FEDORA)
    expected = make_response("IS_FEDORA", product="Fedora")

    yield input_data, expected

    input_data = InputData("test_rhel")
    input_data.add(Specs.redhat_release, RHEL)
    expected = make_response("IS_NOT_FEDORA", product="Red Hat Enterprise Linux Server")

    yield input_data, expected
