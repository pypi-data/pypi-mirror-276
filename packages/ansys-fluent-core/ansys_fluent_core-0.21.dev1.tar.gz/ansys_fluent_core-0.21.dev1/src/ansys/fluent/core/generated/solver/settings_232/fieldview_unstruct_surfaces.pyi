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

from .options import options as options_cls
from .name import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls

class fieldview_unstruct_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    options: options_cls = ...
    name: name_cls = ...
    surfaces: surfaces_cls = ...
    cell_func_domain: cell_func_domain_cls = ...
