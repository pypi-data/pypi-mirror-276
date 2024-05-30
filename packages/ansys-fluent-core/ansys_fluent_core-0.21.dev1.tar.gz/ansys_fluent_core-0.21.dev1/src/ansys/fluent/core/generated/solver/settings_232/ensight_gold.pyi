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
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class ensight_gold(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    cell_func_domain_export: cell_func_domain_export_cls = ...
