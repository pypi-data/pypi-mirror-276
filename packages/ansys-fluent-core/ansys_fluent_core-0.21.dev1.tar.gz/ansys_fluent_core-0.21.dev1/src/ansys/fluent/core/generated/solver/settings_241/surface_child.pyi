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

from .name import name as name_cls
from .report_type import report_type as report_type_cls
from .field import field as field_cls
from .surface_names import surface_names as surface_names_cls
from .per_surface import per_surface as per_surface_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .custom_vector import custom_vector as custom_vector_cls
from .phase_27 import phase as phase_cls
from .physics_1 import physics as physics_cls
from .geometry_5 import geometry as geometry_cls
from .surfaces_4 import surfaces as surfaces_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    report_type: report_type_cls = ...
    field: field_cls = ...
    surface_names: surface_names_cls = ...
    per_surface: per_surface_cls = ...
    average_over: average_over_cls = ...
    retain_instantaneous_values: retain_instantaneous_values_cls = ...
    custom_vector: custom_vector_cls = ...
    phase: phase_cls = ...
    physics: physics_cls = ...
    geometry: geometry_cls = ...
    surfaces: surfaces_cls = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        'create_output_parameter' command.
        """

