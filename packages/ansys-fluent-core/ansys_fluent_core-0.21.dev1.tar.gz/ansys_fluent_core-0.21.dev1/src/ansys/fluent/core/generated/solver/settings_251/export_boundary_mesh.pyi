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

from .filename_2_1 import filename_2 as filename_2_cls
from .boundary_list_1 import boundary_list as boundary_list_cls
from .global_ import global_ as global__cls

class export_boundary_mesh(Command):
    fluent_name = ...
    argument_names = ...
    filename: filename_2_cls = ...
    boundary_list: boundary_list_cls = ...
    global_: global__cls = ...
