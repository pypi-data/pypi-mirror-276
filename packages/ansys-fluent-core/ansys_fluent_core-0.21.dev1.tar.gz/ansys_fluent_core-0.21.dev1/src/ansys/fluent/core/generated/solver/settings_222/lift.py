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

from .lift_child import lift_child


class lift(NamedObject[lift_child], _CreatableNamedObjectMixin[lift_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    child_object_type: lift_child = lift_child
    """
    child_object_type of lift.
    """
