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

from .combusting_particle_child import combusting_particle_child


class combusting_particle(NamedObject[combusting_particle_child], _CreatableNamedObjectMixin[combusting_particle_child]):
    fluent_name = ...
    child_object_type = ...
