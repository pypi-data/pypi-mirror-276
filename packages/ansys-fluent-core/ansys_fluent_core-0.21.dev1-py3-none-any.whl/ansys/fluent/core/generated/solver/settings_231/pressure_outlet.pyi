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

from .pressure_outlet_child import pressure_outlet_child


class pressure_outlet(NamedObject[pressure_outlet_child], _NonCreatableNamedObjectMixin[pressure_outlet_child]):
    fluent_name = ...
    child_object_type = ...
