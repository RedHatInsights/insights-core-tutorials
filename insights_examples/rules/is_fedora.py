from insights.parsers.redhat_release import RedhatRelease
from insights.core.plugins import make_fail, make_pass, rule
from insights_examples.combiners.hostname_uh import HostnameUH

from insights import run

ERROR_KEY_IS_FEDORA = "IS_FEDORA"

# Jinga template for message to be displayed for either
# response tag
CONTENT = {
    ERROR_KEY_IS_FEDORA: "This machine ({{hostname}}) runs {{product}}.",
}


@rule(RedhatRelease, HostnameUH, content=CONTENT)
def report(rel, hostname):
    """Fires if the machine is running Fedora."""

    if "Fedora" in rel.product:
        return make_pass(ERROR_KEY_IS_FEDORA, hostname=hostname.hostname, product=rel.product)
    else:
        return make_fail(ERROR_KEY_IS_FEDORA, hostname=hostname.hostname, product=rel.product)


if __name__ == "__main__":
    run(report, print_summary=True)
