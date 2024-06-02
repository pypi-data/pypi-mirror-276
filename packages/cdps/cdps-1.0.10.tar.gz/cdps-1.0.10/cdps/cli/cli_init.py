import os

from cdps.constants import core_constant
from cdps.cdps_server import CDPS


def initialize_environment(*, quiet: bool = False, focus: bool = False):
    CDPS(initialize_environment=True, focus=focus)
    if not quiet:
        print('Initialized environment for {} in {}'.format(
            core_constant.NAME, os.getcwd()))
