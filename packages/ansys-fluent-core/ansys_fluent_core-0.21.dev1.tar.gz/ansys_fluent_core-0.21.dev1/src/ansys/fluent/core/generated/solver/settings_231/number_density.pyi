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
from .disc_output_type import disc_output_type as disc_output_type_cls
from .qmom_output_type import qmom_output_type as qmom_output_type_cls
from .smm_output_type import smm_output_type as smm_output_type_cls
from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_dens_func import num_dens_func as num_dens_func_cls
from .dia_upper_limit import dia_upper_limit as dia_upper_limit_cls
from .file_name_1 import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls

class number_density(Command):
    fluent_name = ...
    argument_names = ...
    report_type: report_type_cls = ...
    disc_output_type: disc_output_type_cls = ...
    qmom_output_type: qmom_output_type_cls = ...
    smm_output_type: smm_output_type_cls = ...
    surface_list: surface_list_cls = ...
    volume_list: volume_list_cls = ...
    num_dens_func: num_dens_func_cls = ...
    dia_upper_limit: dia_upper_limit_cls = ...
    file_name: file_name_cls = ...
    overwrite: overwrite_cls = ...
