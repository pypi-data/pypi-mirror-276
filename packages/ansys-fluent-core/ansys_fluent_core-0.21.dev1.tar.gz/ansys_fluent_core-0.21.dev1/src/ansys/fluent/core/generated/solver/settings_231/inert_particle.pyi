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

from .inert_particle_child import inert_particle_child


class inert_particle(NamedObject[inert_particle_child], _CreatableNamedObjectMixin[inert_particle_child]):
    fluent_name = ...
    child_object_type = ...
