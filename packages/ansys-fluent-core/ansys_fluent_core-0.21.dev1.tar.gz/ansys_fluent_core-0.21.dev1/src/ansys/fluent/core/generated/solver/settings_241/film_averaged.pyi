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

from .averaging_coefficient import averaging_coefficient as averaging_coefficient_cls
from .binary_diffusivity import binary_diffusivity as binary_diffusivity_cls

class film_averaged(Group):
    fluent_name = ...
    child_names = ...
    averaging_coefficient: averaging_coefficient_cls = ...
    binary_diffusivity: binary_diffusivity_cls = ...
