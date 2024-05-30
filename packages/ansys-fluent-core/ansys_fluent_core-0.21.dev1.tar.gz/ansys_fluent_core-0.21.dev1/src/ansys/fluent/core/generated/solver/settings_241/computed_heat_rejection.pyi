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

from .heat_exchanger import heat_exchanger as heat_exchanger_cls
from .fluid_zone import fluid_zone as fluid_zone_cls
from .boundary_zone_1 import boundary_zone as boundary_zone_cls
from .report_type import report_type as report_type_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_file import append_file as append_file_cls

class computed_heat_rejection(Command):
    fluent_name = ...
    argument_names = ...
    heat_exchanger: heat_exchanger_cls = ...
    fluid_zone: fluid_zone_cls = ...
    boundary_zone: boundary_zone_cls = ...
    report_type: report_type_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_file: append_file_cls = ...
