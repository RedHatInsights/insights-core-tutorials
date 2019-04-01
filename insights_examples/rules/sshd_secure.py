from insights.core.plugins import make_fail, rule
from insights_examples.parsers.secure_shell import SSHDConfig
from insights.parsers.installed_rpms import InstalledRpms
from insights import add_filter
from insights.specs import Specs

from insights import run

ERROR_KEY = "SSHD_SECURE"

# Jinga template displayed for make_response results
CONTENT = ERROR_KEY + """
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


add_filter(Specs.sshd_config, ["AuthenticationMethods", "LogLevel", "PermitRootLogin", "Protocol"])


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


if __name__ == "__main__":
    run(report, print_summary=True)
