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

from .file_name_1 import file_name as file_name_cls
from .surface_name_list_1 import surface_name_list as surface_name_list_cls
from .delimiter import delimiter as delimiter_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls
from .location import location as location_cls

class ascii(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    surface_name_list: surface_name_list_cls = ...
    delimiter: delimiter_cls = ...
    cell_func_domain: cell_func_domain_cls = ...
    location: location_cls = ...
