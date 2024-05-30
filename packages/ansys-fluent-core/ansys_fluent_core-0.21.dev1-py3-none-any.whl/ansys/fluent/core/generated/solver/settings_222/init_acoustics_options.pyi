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

from .set_ramping_length import set_ramping_length as set_ramping_length_cls
from .number_of_timesteps import number_of_timesteps as number_of_timesteps_cls

class init_acoustics_options(Command):
    fluent_name = ...
    argument_names = ...
    set_ramping_length: set_ramping_length_cls = ...
    number_of_timesteps: number_of_timesteps_cls = ...
