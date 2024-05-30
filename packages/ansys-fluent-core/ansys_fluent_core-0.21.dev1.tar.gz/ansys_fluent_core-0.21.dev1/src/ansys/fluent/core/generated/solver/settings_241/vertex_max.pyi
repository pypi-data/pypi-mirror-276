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

from .surface_names_2 import surface_names as surface_names_cls
from .geometry_names import geometry_names as geometry_names_cls
from .cust_vec_func import cust_vec_func as cust_vec_func_cls
from .report_of import report_of as report_of_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class vertex_max(Command):
    fluent_name = ...
    argument_names = ...
    surface_names: surface_names_cls = ...
    geometry_names: geometry_names_cls = ...
    cust_vec_func: cust_vec_func_cls = ...
    report_of: report_of_cls = ...
    current_domain: current_domain_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
