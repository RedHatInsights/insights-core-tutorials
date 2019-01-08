from functools import partial
from insights.core.context import SosArchiveContext
from insights.core.spec_factory import simple_file, glob_file
from . import Specs
import os

simple_file = partial(simple_file, context=SosArchiveContext)
glob_file = partial(glob_file, context=SosArchiveContext)


class SosSpecs(Specs):
    """
    This class defines how data is accessed from a sosreport.
    Add specs here if you want to process a sosreport.
    """

    conf_file = os.path.join(os.path.dirname(__file__), 'sshd_config')

    sshd_config = simple_file(conf_file)
