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

from .cell_zones_6 import cell_zones as cell_zones_cls
from .volumes_2 import volumes as volumes_cls
from .cell_function_2 import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .file_name_14 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class volume_average(Command):
    fluent_name = ...
    argument_names = ...
    cell_zones: cell_zones_cls = ...
    volumes: volumes_cls = ...
    cell_function: cell_function_cls = ...
    current_domain: current_domain_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
