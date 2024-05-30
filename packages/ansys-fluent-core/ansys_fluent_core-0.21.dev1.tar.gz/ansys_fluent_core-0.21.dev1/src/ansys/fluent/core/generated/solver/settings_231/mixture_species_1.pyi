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

from .droplet_particle_child import droplet_particle_child


class mixture_species(NamedObject[droplet_particle_child], _NonCreatableNamedObjectMixin[droplet_particle_child]):
    fluent_name = ...
    child_object_type = ...
