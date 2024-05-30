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

from .species_diffusivity_child import species_diffusivity_child


class species_diffusivity(NamedObject[species_diffusivity_child], _NonCreatableNamedObjectMixin[species_diffusivity_child]):
    fluent_name = ...
    child_object_type = ...
