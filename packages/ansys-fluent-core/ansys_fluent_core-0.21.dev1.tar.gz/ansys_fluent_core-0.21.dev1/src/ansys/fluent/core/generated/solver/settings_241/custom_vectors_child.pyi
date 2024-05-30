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
from .x_component import x_component as x_component_cls
from .y_component import y_component as y_component_cls
from .z_component import z_component as z_component_cls

class custom_vectors_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    x_component: x_component_cls = ...
    y_component: y_component_cls = ...
    z_component: z_component_cls = ...
