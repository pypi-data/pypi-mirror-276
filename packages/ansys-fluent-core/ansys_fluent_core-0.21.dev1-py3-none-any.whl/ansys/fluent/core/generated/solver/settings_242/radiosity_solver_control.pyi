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

from .maximum_radiation_iterations import maximum_radiation_iterations as maximum_radiation_iterations_cls
from .residual_convergence_criteria import residual_convergence_criteria as residual_convergence_criteria_cls

class radiosity_solver_control(Group):
    fluent_name = ...
    child_names = ...
    maximum_radiation_iterations: maximum_radiation_iterations_cls = ...
    residual_convergence_criteria: residual_convergence_criteria_cls = ...
