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

from .recirculation_outlet_child import recirculation_outlet_child


class recirculation_outlet(NamedObject[recirculation_outlet_child], _NonCreatableNamedObjectMixin[recirculation_outlet_child]):
    fluent_name = ...
    child_object_type = ...
