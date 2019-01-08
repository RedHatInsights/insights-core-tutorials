from insights.parsers.redhat_release import RedhatRelease
from insights.core.plugins import make_response, rule

# Jinga template for message to be displayed for either
# response tag
CONTENT = {
    "IS_FEDORA": "This machine runs {{product}}.",
    "IS_NOT_FEDORA": "This machine runs {{product}}."
}


@rule(RedhatRelease, content=CONTENT)
def report(rel):
    """Fires if the machine is running Fedora."""

    if "Fedora" in rel.product:
        return make_response("IS_FEDORA", product=rel.product)
    else:
        return make_response("IS_NOT_FEDORA", product=rel.product)
