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

from .formulation_1 import formulation as formulation_cls
from .relaxation_method import relaxation_method as relaxation_method_cls
from .convergence_acceleration_for_stretched_meshes import convergence_acceleration_for_stretched_meshes as convergence_acceleration_for_stretched_meshes_cls
from .relaxation_bounds import relaxation_bounds as relaxation_bounds_cls

class pseudo_time_method(Group):
    fluent_name = ...
    child_names = ...
    formulation: formulation_cls = ...
    relaxation_method: relaxation_method_cls = ...
    convergence_acceleration_for_stretched_meshes: convergence_acceleration_for_stretched_meshes_cls = ...
    command_names = ...

    def relaxation_bounds(self, relaxation_bounding_method: str, default_min_max_relaxation_limits: bool, minimum_allowed_effctive_relaxation: Union[float, str], maximum_allowed_effctive_relaxation: Union[float, str]):
        """
        Select relaxation bounding scheme for pseudo time method.
        
        Parameters
        ----------
            relaxation_bounding_method : str
                'relaxation_bounding_method' child.
            default_min_max_relaxation_limits : bool
                'default_min_max_relaxation_limits' child.
            minimum_allowed_effctive_relaxation : real
                'minimum_allowed_effctive_relaxation' child.
            maximum_allowed_effctive_relaxation : real
                'maximum_allowed_effctive_relaxation' child.
        
        """

