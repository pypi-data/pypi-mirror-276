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

from .phase_child_1 import phase_child


class phase(NamedObject[phase_child], _CreatableNamedObjectMixin[phase_child]):
    """
    'phase' child.
    """

    fluent_name = "phase"

    child_object_type: phase_child = phase_child
    """
    child_object_type of phase.
    """
