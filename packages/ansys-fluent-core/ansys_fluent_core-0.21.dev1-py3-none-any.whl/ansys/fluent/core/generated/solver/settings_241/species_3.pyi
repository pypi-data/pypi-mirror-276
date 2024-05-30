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

from .volumetric_species import volumetric_species as volumetric_species_cls
from .last_species import last_species as last_species_cls

class species(Group):
    fluent_name = ...
    child_names = ...
    volumetric_species: volumetric_species_cls = ...
    last_species: last_species_cls = ...
