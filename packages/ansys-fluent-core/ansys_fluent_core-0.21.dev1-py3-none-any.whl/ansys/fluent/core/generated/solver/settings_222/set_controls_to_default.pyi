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

from .solution_controls import solution_controls as solution_controls_cls
from .amg_controls import amg_controls as amg_controls_cls
from .multi_stage_parameter import multi_stage_parameter as multi_stage_parameter_cls
from .limits_1 import limits as limits_cls
from .reset_pseudo_time_method_generic import reset_pseudo_time_method_generic as reset_pseudo_time_method_generic_cls
from .reset_pseudo_time_method_equations import reset_pseudo_time_method_equations as reset_pseudo_time_method_equations_cls
from .reset_pseudo_time_method_relaxations import reset_pseudo_time_method_relaxations as reset_pseudo_time_method_relaxations_cls
from .reset_pseudo_time_method_scale_factors import reset_pseudo_time_method_scale_factors as reset_pseudo_time_method_scale_factors_cls

class set_controls_to_default(Group):
    fluent_name = ...
    command_names = ...

    def solution_controls(self, ):
        """
        'solution_controls' command.
        """

    def amg_controls(self, ):
        """
        'amg_controls' command.
        """

    def multi_stage_parameter(self, ):
        """
        'multi_stage_parameter' command.
        """

    def limits(self, ):
        """
        'limits' command.
        """

    def reset_pseudo_time_method_generic(self, ):
        """
        'reset_pseudo_time_method_generic' command.
        """

    def reset_pseudo_time_method_equations(self, ):
        """
        'reset_pseudo_time_method_equations' command.
        """

    def reset_pseudo_time_method_relaxations(self, ):
        """
        'reset_pseudo_time_method_relaxations' command.
        """

    def reset_pseudo_time_method_scale_factors(self, ):
        """
        'reset_pseudo_time_method_scale_factors' command.
        """

