from insights.core.spec_factory import simple_file
from . import Specs
import os


class DefaultSpecs(Specs):
    """
    This class defines how data is accessed from a host.
    Add specs here to collect data directly from a host when
    insights-core is executed.
    """
    conf_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'parsers/sshd_config')

    sshd_config = simple_file(conf_file)
