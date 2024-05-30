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

from .save_mode import save_mode as save_mode_cls
from .continue_with_current_mesh import continue_with_current_mesh as continue_with_current_mesh_cls
from .discard_all_data import discard_all_data as discard_all_data_cls

class execute_strategy(Command):
    fluent_name = ...
    argument_names = ...
    save_mode: save_mode_cls = ...
    continue_with_current_mesh: continue_with_current_mesh_cls = ...
    discard_all_data: discard_all_data_cls = ...
