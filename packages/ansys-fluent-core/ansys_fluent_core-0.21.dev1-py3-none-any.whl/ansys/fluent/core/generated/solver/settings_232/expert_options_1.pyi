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

from .re_randomization_every_iteration_enabled import re_randomization_every_iteration_enabled as re_randomization_every_iteration_enabled_cls
from .re_randomization_every_timestep_enabled import re_randomization_every_timestep_enabled as re_randomization_every_timestep_enabled_cls
from .tracking_statistics_format import tracking_statistics_format as tracking_statistics_format_cls
from .verbosity_1 import verbosity as verbosity_cls

class expert_options(Group):
    fluent_name = ...
    child_names = ...
    re_randomization_every_iteration_enabled: re_randomization_every_iteration_enabled_cls = ...
    re_randomization_every_timestep_enabled: re_randomization_every_timestep_enabled_cls = ...
    tracking_statistics_format: tracking_statistics_format_cls = ...
    verbosity: verbosity_cls = ...
