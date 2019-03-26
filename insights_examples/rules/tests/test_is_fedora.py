from .. import is_fedora
from insights.specs import Specs
from insights.tests import InputData, archive_provider
from insights.core.plugins import make_pass, make_fail

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
    expected = make_fail("IS_NOT_FEDORA", hostname=TEST_HOSTNAME, product="Red Hat Enterprise Linux Server")

    yield input_data, expected
