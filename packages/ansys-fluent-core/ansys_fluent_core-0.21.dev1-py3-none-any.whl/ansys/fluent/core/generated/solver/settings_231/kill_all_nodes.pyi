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

from .invalidate_case import invalidate_case as invalidate_case_cls
from .delete_all_compute_nodes import delete_all_compute_nodes as delete_all_compute_nodes_cls

class kill_all_nodes(Command):
    fluent_name = ...
    argument_names = ...
    invalidate_case: invalidate_case_cls = ...
    delete_all_compute_nodes: delete_all_compute_nodes_cls = ...
