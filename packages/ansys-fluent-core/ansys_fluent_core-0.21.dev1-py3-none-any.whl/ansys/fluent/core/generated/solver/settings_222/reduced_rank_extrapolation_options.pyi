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

from .subspace_size import subspace_size as subspace_size_cls
from .skip_itr import skip_itr as skip_itr_cls

class reduced_rank_extrapolation_options(Group):
    fluent_name = ...
    child_names = ...
    subspace_size: subspace_size_cls = ...
    skip_itr: skip_itr_cls = ...
