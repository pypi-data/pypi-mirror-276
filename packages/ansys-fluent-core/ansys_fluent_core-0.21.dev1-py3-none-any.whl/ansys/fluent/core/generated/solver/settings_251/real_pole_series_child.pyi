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

from .pole import pole as pole_cls
from .amplitude import amplitude as amplitude_cls

class real_pole_series_child(Group):
    fluent_name = ...
    child_names = ...
    pole: pole_cls = ...
    amplitude: amplitude_cls = ...
