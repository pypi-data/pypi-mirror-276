#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .re_randomize_every_iteration import re_randomize_every_iteration as re_randomize_every_iteration_cls
from .re_randomize_every_timestep import re_randomize_every_timestep as re_randomize_every_timestep_cls
from .tracking_statistics_format import tracking_statistics_format as tracking_statistics_format_cls
from .verbosity_1 import verbosity as verbosity_cls

class expert_options(Group):
    fluent_name = ...
    child_names = ...
    re_randomize_every_iteration: re_randomize_every_iteration_cls = ...
    re_randomize_every_timestep: re_randomize_every_timestep_cls = ...
    tracking_statistics_format: tracking_statistics_format_cls = ...
    verbosity: verbosity_cls = ...
