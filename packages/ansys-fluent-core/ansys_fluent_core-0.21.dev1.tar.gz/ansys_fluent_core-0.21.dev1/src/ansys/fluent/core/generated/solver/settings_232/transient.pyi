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

from .transient_parameters_specify import transient_parameters_specify as transient_parameters_specify_cls
from .transient_scheme import transient_scheme as transient_scheme_cls
from .time_scale_modification_method import time_scale_modification_method as time_scale_modification_method_cls
from .time_scale_modification_factor import time_scale_modification_factor as time_scale_modification_factor_cls

class transient(Group):
    fluent_name = ...
    child_names = ...
    transient_parameters_specify: transient_parameters_specify_cls = ...
    transient_scheme: transient_scheme_cls = ...
    time_scale_modification_method: time_scale_modification_method_cls = ...
    time_scale_modification_factor: time_scale_modification_factor_cls = ...
