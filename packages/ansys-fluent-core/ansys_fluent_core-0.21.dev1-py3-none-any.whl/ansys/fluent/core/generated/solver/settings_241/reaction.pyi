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

from .react import react as react_cls
from .reaction_mechs_1 import reaction_mechs as reaction_mechs_cls
from .surface_volume_ratio import surface_volume_ratio as surface_volume_ratio_cls
from .electrolyte_1 import electrolyte as electrolyte_cls

class reaction(Group):
    fluent_name = ...
    child_names = ...
    react: react_cls = ...
    reaction_mechs: reaction_mechs_cls = ...
    surface_volume_ratio: surface_volume_ratio_cls = ...
    electrolyte: electrolyte_cls = ...
