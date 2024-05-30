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

from .max_iterations_1 import max_iterations as max_iterations_cls
from .constraint_relaxation import constraint_relaxation as constraint_relaxation_cls
from .preconditioning import preconditioning as preconditioning_cls

class prescribed_motions(Group):
    fluent_name = ...
    child_names = ...
    max_iterations: max_iterations_cls = ...
    constraint_relaxation: constraint_relaxation_cls = ...
    preconditioning: preconditioning_cls = ...
