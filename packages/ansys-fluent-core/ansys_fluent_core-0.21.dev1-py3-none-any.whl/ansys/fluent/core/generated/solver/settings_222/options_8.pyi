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

from .option import option as option_cls
from .constant_1 import constant as constant_cls
from .variable import variable as variable_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    constant: constant_cls = ...
    variable: variable_cls = ...
