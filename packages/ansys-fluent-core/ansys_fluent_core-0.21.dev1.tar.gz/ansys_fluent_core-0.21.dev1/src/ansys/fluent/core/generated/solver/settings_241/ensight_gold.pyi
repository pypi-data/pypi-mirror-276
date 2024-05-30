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
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
from .binary_format import binary_format as binary_format_cls
from .cellzones import cellzones as cellzones_cls
from .interior_zone_surfaces import interior_zone_surfaces as interior_zone_surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls

class ensight_gold(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    cell_func_domain_export: cell_func_domain_export_cls = ...
    binary_format: binary_format_cls = ...
    cellzones: cellzones_cls = ...
    interior_zone_surfaces: interior_zone_surfaces_cls = ...
    cell_centered: cell_centered_cls = ...
