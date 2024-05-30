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

from .under_relaxation_factor_1 import under_relaxation_factor as under_relaxation_factor_cls
from .explicit_relaxation_factor import explicit_relaxation_factor as explicit_relaxation_factor_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    under_relaxation_factor: under_relaxation_factor_cls = ...
    explicit_relaxation_factor: explicit_relaxation_factor_cls = ...
