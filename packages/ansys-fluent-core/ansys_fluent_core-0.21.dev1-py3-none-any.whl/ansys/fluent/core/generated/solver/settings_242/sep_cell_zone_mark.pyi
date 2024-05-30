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

from .cell_zone_name_1 import cell_zone_name as cell_zone_name_cls
from .register import register as register_cls
from .move_faces import move_faces as move_faces_cls

class sep_cell_zone_mark(Command):
    fluent_name = ...
    argument_names = ...
    cell_zone_name: cell_zone_name_cls = ...
    register: register_cls = ...
    move_faces: move_faces_cls = ...
