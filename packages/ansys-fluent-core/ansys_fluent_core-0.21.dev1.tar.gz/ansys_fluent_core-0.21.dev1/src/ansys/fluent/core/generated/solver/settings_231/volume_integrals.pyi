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

from .report_type import report_type as report_type_cls
from .thread_id_list import thread_id_list as thread_id_list_cls
from .domain import domain as domain_cls
from .cell_function import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls

class volume_integrals(Command):
    fluent_name = ...
    argument_names = ...
    report_type: report_type_cls = ...
    thread_id_list: thread_id_list_cls = ...
    domain: domain_cls = ...
    cell_function: cell_function_cls = ...
    current_domain: current_domain_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
    overwrite: overwrite_cls = ...
