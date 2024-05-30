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

from .domain_val import domain_val as domain_val_cls
from .all_bndry_zones import all_bndry_zones as all_bndry_zones_cls
from .zone_list_1 import zone_list as zone_list_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls

class electric_current(Command):
    fluent_name = ...
    argument_names = ...
    domain_val: domain_val_cls = ...
    all_bndry_zones: all_bndry_zones_cls = ...
    zone_list: zone_list_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
    overwrite: overwrite_cls = ...
