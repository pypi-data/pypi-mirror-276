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

from .check_convergence import check_convergence as check_convergence_cls
from .absolute_criteria import absolute_criteria as absolute_criteria_cls

class adjoint_equations_child(Group):
    fluent_name = ...
    child_names = ...
    check_convergence: check_convergence_cls = ...
    absolute_criteria: absolute_criteria_cls = ...
