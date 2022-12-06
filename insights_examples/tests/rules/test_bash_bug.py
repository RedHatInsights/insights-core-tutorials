from insights.specs import Specs
from insights.tests import InputData, archive_provider
from insights.core.plugins import make_pass, make_fail
from insights_examples.rules import bash_bug

BUG_VERSION = "bash-4.4.14-1.any"
FIX_VERSION = "bash-4.4.18-1.any"
CURRENT_VERSION = "bash-4.4.23-1.fc28"

FOUND = "Bash bug found! Version: "
NOT_FOUND = "Bash bug not found: "

FEDORA = "Fedora release 28 (Twenty Eight)"
RHEL = "Red Hat Enterprise Linux Server release 7.4 (Maipo)"
TEST_HOSTNAME = "testhost.someplace.com"


@archive_provider(bash_bug.check_bash_bug)
def integration_test():

    input_data = InputData("no_bash_bug")
    input_data.add(Specs.installed_rpms, CURRENT_VERSION)
    expected = make_pass("BASH_BUG", bash=CURRENT_VERSION, found=NOT_FOUND)

    yield input_data, expected

    input_data = InputData("is_bash_bug")
    input_data.add(Specs.installed_rpms, BUG_VERSION)
    expected = make_fail("BASH_BUG", bash=BUG_VERSION, found=FOUND)

    yield input_data, expected
