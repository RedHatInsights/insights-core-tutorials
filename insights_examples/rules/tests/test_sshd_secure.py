from insights_examples.rules import sshd_secure
from insights.tests import InputData, archive_provider
from insights.core.plugins import make_fail
from insights.specs import Specs

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
    to the rule.  So this is essentially and end-to-end
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
