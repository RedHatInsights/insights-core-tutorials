from insights import run
from insights.core.plugins import make_fail, make_pass, rule
from insights.parsers.redhat_release import RedhatRelease
from insights_examples.combiners.hostname_uh import HostnameUH

ERROR_KEY_IS_FEDORA = "IS_FEDORA"

# Jinja2 template for message to be displayed for either
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
