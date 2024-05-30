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

from .conjugate_heat_transfer import conjugate_heat_transfer as conjugate_heat_transfer_cls
from .solve import solve as solve_cls

class multidomain(Group):
    fluent_name = ...
    child_names = ...
    conjugate_heat_transfer: conjugate_heat_transfer_cls = ...
    solve: solve_cls = ...
