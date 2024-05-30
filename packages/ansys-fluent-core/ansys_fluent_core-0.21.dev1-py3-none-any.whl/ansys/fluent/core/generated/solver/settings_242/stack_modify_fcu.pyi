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

from .fcu_name import fcu_name as fcu_name_cls
from .cellzones_1 import cellzones as cellzones_cls

class stack_modify_fcu(Command):
    fluent_name = ...
    argument_names = ...
    fcu_name: fcu_name_cls = ...
    cellzones: cellzones_cls = ...
