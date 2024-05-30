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

from .option_1 import option as option_cls
from .material import material as material_cls
from .phase_material import phase_material as phase_material_cls
from .number_vol_spec import number_vol_spec as number_vol_spec_cls

class model(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    material: material_cls = ...
    phase_material: phase_material_cls = ...
    number_vol_spec: number_vol_spec_cls = ...
