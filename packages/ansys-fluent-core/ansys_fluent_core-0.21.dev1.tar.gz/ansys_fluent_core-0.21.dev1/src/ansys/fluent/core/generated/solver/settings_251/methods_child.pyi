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

from .flow_solver import flow_solver as flow_solver_cls
from .adjoint_solver import adjoint_solver as adjoint_solver_cls
from .adjoint_activation import adjoint_activation as adjoint_activation_cls
from .adjoint_equations import adjoint_equations as adjoint_equations_cls

class methods_child(Group):
    fluent_name = ...
    child_names = ...
    flow_solver: flow_solver_cls = ...
    adjoint_solver: adjoint_solver_cls = ...
    adjoint_activation: adjoint_activation_cls = ...
    adjoint_equations: adjoint_equations_cls = ...
