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

from .surface_names_1 import surface_names as surface_names_cls
from .color_1 import color as color_cls
from .material import material as material_cls

class surfaces(Command):
    fluent_name = ...
    argument_names = ...
    surface_names: surface_names_cls = ...
    color: color_cls = ...
    material: material_cls = ...
