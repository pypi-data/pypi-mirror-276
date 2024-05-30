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

from .option_6 import option as option_cls
from .partitioning_method_for_dpm_domain import partitioning_method_for_dpm_domain as partitioning_method_for_dpm_domain_cls

class dpm_domain(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    partitioning_method_for_dpm_domain: partitioning_method_for_dpm_domain_cls = ...
