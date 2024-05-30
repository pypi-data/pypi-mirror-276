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
from .surface_name_list import surface_name_list as surface_name_list_cls
from .wall_function import wall_function as wall_function_cls
from .htc_on_walls import htc_on_walls as htc_on_walls_cls

class taitherm(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    surface_name_list: surface_name_list_cls = ...
    wall_function: wall_function_cls = ...
    htc_on_walls: htc_on_walls_cls = ...
