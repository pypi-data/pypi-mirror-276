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

from .force_child import force_child


class lift(NamedObject[force_child], _CreatableNamedObjectMixin[force_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    child_object_type: force_child = force_child
    """
    child_object_type of lift.
    """
