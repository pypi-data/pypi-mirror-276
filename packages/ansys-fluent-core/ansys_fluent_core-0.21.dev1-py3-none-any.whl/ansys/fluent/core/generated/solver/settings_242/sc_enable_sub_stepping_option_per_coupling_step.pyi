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

from .enable_sub_stepping import enable_sub_stepping as enable_sub_stepping_cls
from .num_sub_stepping_coupling_itr import num_sub_stepping_coupling_itr as num_sub_stepping_coupling_itr_cls

class sc_enable_sub_stepping_option_per_coupling_step(Command):
    fluent_name = ...
    argument_names = ...
    enable_sub_stepping: enable_sub_stepping_cls = ...
    num_sub_stepping_coupling_itr: num_sub_stepping_coupling_itr_cls = ...
