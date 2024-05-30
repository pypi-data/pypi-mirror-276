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

from .echem_rate import echem_rate as echem_rate_cls
from .relative_permeability import relative_permeability as relative_permeability_cls

class customization(Group):
    fluent_name = ...
    child_names = ...
    echem_rate: echem_rate_cls = ...
    relative_permeability: relative_permeability_cls = ...
