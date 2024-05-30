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

from .enable_6 import enable as enable_cls
from .solution_method import solution_method as solution_method_cls

class do_energy_coupling(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    solution_method: solution_method_cls = ...
