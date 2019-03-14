from insights import rule, make_pass, make_fail
from insights.parsers.installed_rpms import InstalledRpm, InstalledRpms

ERROR_KEY_BASH_BUG_PRESENT = "BASH_BUG_PRESENT"
ERROR_KEY_BASH_BUG_NOT_PRESENT = "BASH_BUG_NOT_PRESENT"

CONTENT = {
    ERROR_KEY_BASH_BUG_PRESENT: "Bash bug found! Version: {{bash}}",
    ERROR_KEY_BASH_BUG_NOT_PRESENT: "Bash bug not found: {{bash}}."
}


@rule(InstalledRpms)
def check_bash_bug(rpms):
    bug_version = InstalledRpm.from_package('bash-4.4.14-1.any')
    fix_version = InstalledRpm.from_package('bash-4.4.18-1.any')
    current_version = rpms.get_max('bash')
    if bug_version <= current_version < fix_version:
        return make_fail(ERROR_KEY_BASH_BUG_PRESENT, bash=current_version.nvr)
    else:
        return make_pass(ERROR_KEY_BASH_BUG_NOT_PRESENT, bash=current_version.nvr)
