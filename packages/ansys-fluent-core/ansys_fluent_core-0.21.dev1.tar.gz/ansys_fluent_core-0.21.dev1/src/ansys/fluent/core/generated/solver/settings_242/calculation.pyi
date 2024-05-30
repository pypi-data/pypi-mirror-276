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

from .iteration_count import iteration_count as iteration_count_cls
from .initialize_stabilization import initialize_stabilization as initialize_stabilization_cls
from .calculation_activities import calculation_activities as calculation_activities_cls
from .initialize_2 import initialize as initialize_cls
from .calculate_1 import calculate as calculate_cls

class calculation(Group):
    fluent_name = ...
    child_names = ...
    iteration_count: iteration_count_cls = ...
    initialize_stabilization: initialize_stabilization_cls = ...
    calculation_activities: calculation_activities_cls = ...
    command_names = ...

    def initialize(self, ):
        """
        Initialize adjoint solution and stabilization scheme.
        """

    def calculate(self, ):
        """
        Start evaluating the adjoint solution.
        """

