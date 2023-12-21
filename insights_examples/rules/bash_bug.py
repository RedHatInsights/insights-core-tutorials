"""
Bash Bug
========

This is a simple rule example that simulates a bash bug based on version of the
the bash rpm installed. This example can be run against the local host
using the following command::

$ insights-run -p insights_examples.rules.bash_bug

or from the insights_examples/rules directory::

$ python bash_bug.py
"""
from insights import rule, make_pass, make_fail
from insights.parsers.installed_rpms import InstalledRpm, InstalledRpms

ERROR_KEY_BASH_BUG = "BASH_BUG"

CONTENT = {
    ERROR_KEY_BASH_BUG: "{{found}}{{bash}}"
}


@rule(InstalledRpms)
def check_bash_bug(rpms):
    bug_version = InstalledRpm.from_package('bash-4.4.14-1.any')
    fix_version = InstalledRpm.from_package('bash-4.4.18-1.any')
    current_version = rpms.get_max('bash')
    if bug_version <= current_version < fix_version:
        found = "Bash bug found! Version: "
        return make_fail(ERROR_KEY_BASH_BUG, bash=current_version.nvr, found=found)
    else:
        not_found = "Bash bug not found: "
        return make_pass(ERROR_KEY_BASH_BUG, bash=current_version.nvr, found=not_found)


if __name__ == "__main__":
    from insights import run
    run(check_bash_bug, print_summary=True)
