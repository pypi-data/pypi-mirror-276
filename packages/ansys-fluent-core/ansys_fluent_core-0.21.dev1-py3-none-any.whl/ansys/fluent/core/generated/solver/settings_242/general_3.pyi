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

from .material_4 import material as material_cls
from .participates_in_radiation import participates_in_radiation as participates_in_radiation_cls

class general(Group):
    fluent_name = ...
    child_names = ...
    material: material_cls = ...
    participates_in_radiation: participates_in_radiation_cls = ...
