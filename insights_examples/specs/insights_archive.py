from functools import partial
from insights.core.context import HostArchiveContext
from insights.core.spec_factory import simple_file
from . import Specs
import os

simple_file = partial(simple_file, context=HostArchiveContext)


class InsightsArchiveSpecs(Specs):
    """
    This class defines how data is accessed from an insights archive.
    Add specs here if you want to process and insights archive.
    """

    conf_file = os.path.join(os.path.dirname(__file__), 'sshd_config')

    sshd_config = simple_file(conf_file)

    # chronyc_tracking = simple_file("insights_commands/chronyc_tracking")
    # ntpq_peers = simple_file("insights_commands/ntpq_-c_peers")
