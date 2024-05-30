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

from .enable_roughness_correlation import enable_roughness_correlation as enable_roughness_correlation_cls
from .roughness_correlation_fcn import roughness_correlation_fcn as roughness_correlation_fcn_cls
from .geometric_roughness_ht_val import geometric_roughness_ht_val as geometric_roughness_ht_val_cls

class transition_sst_option(Group):
    fluent_name = ...
    child_names = ...
    enable_roughness_correlation: enable_roughness_correlation_cls = ...
    roughness_correlation_fcn: roughness_correlation_fcn_cls = ...
    geometric_roughness_ht_val: geometric_roughness_ht_val_cls = ...
