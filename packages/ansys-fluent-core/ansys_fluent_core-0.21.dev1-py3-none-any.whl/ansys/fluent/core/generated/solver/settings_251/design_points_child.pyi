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
from .input_parameters import input_parameters as input_parameters_cls
from .output_parameters import output_parameters as output_parameters_cls
from .write_data_2 import write_data as write_data_cls
from .capture_simulation_report_data_1 import capture_simulation_report_data as capture_simulation_report_data_cls

class design_points_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    input_parameters: input_parameters_cls = ...
    output_parameters: output_parameters_cls = ...
    write_data: write_data_cls = ...
    capture_simulation_report_data: capture_simulation_report_data_cls = ...
