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

from .optimizer_type import optimizer_type as optimizer_type_cls
from .objectives_3 import objectives as objectives_cls
from .optimizer_settings import optimizer_settings as optimizer_settings_cls
from .turbulence_model_design_tool import turbulence_model_design_tool as turbulence_model_design_tool_cls
from .mesh_quality import mesh_quality as mesh_quality_cls
from .calculation_activities_1 import calculation_activities as calculation_activities_cls
from .initialize_4 import initialize as initialize_cls
from .reset_3 import reset as reset_cls
from .optimize import optimize as optimize_cls
from .summarize import summarize as summarize_cls
from .default_9 import default as default_cls

class optimizer(Group):
    fluent_name = ...
    child_names = ...
    optimizer_type: optimizer_type_cls = ...
    objectives: objectives_cls = ...
    optimizer_settings: optimizer_settings_cls = ...
    turbulence_model_design_tool: turbulence_model_design_tool_cls = ...
    mesh_quality: mesh_quality_cls = ...
    calculation_activities: calculation_activities_cls = ...
    command_names = ...

    def initialize(self, turbulence_design_variables: bool):
        """
        Initialize gradient-based optimizer.
        
        Parameters
        ----------
            turbulence_design_variables : bool
                Initialize the turbulence design variables in the design region?.
        
        """

    def reset(self, ):
        """
        Reset gradient-based optimizer.
        """

    def optimize(self, current_warnings: List[str], disable_settings_validation: bool):
        """
        Disable warnings detecting possibly wrong settings before running the optimizer.
        
        Parameters
        ----------
            current_warnings : typing.List[str]
                Warnings based on current settings.
            disable_settings_validation : bool
                Ignore warnings and proceed with optimization.
        
        """

    def summarize(self, ):
        """
        Summarize results from gradient-based optimizer.
        """

    def default(self, ):
        """
        Summarize results from gradient-based optimizer.
        """

