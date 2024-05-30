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

from .end_of_timestep import end_of_timestep as end_of_timestep_cls

class interrupt(Command):
    fluent_name = ...
    argument_names = ...
    end_of_timestep: end_of_timestep_cls = ...
