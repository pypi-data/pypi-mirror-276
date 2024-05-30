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

from .matrix_component import matrix_component as matrix_component_cls
from .diffusivity import diffusivity as diffusivity_cls

class anisotropic(Group):
    fluent_name = ...
    child_names = ...
    matrix_component: matrix_component_cls = ...
    diffusivity: diffusivity_cls = ...
