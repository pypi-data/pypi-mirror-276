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

from .option_11 import option as option_cls
from .change_all_o2o_si_names import change_all_o2o_si_names as change_all_o2o_si_names_cls

class naming_option(Command):
    fluent_name = ...
    argument_names = ...
    option: option_cls = ...
    change_all_o2o_si_names: change_all_o2o_si_names_cls = ...
