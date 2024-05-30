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

from .intake_fan_child import intake_fan_child


class intake_fan(NamedObject[intake_fan_child], _NonCreatableNamedObjectMixin[intake_fan_child]):
    fluent_name = ...
    child_object_type = ...
