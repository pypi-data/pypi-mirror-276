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

from .option import option as option_cls
from .domain import domain as domain_cls
from .all_wall_zones import all_wall_zones as all_wall_zones_cls
from .wall_zones_1 import wall_zones as wall_zones_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .momentum_center import momentum_center as momentum_center_cls
from .momentum_axis import momentum_axis as momentum_axis_cls
from .pressure_coordinate import pressure_coordinate as pressure_coordinate_cls
from .coordinate_value import coordinate_value as coordinate_value_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class forces(Command):
    fluent_name = ...
    argument_names = ...
    option: option_cls = ...
    domain: domain_cls = ...
    all_wall_zones: all_wall_zones_cls = ...
    wall_zones: wall_zones_cls = ...
    direction_vector: direction_vector_cls = ...
    momentum_center: momentum_center_cls = ...
    momentum_axis: momentum_axis_cls = ...
    pressure_coordinate: pressure_coordinate_cls = ...
    coordinate_value: coordinate_value_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
