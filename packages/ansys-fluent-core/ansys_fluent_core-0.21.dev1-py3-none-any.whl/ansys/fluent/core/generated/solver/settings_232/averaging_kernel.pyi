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

from .kernel import kernel as kernel_cls
from .gaussian_factor import gaussian_factor as gaussian_factor_cls

class averaging_kernel(Group):
    fluent_name = ...
    child_names = ...
    kernel: kernel_cls = ...
    gaussian_factor: gaussian_factor_cls = ...
