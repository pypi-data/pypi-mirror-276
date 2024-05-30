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

from .thin_film import thin_film as thin_film_cls
from .liquid_vof_factor import liquid_vof_factor as liquid_vof_factor_cls

class boiling_parameters(Group):
    fluent_name = ...
    child_names = ...
    thin_film: thin_film_cls = ...
    liquid_vof_factor: liquid_vof_factor_cls = ...
