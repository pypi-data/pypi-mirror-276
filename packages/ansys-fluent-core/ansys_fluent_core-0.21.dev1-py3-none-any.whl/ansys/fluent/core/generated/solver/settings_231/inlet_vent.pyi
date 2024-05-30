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

from .inlet_vent_child import inlet_vent_child


class inlet_vent(NamedObject[inlet_vent_child], _NonCreatableNamedObjectMixin[inlet_vent_child]):
    fluent_name = ...
    child_object_type = ...
