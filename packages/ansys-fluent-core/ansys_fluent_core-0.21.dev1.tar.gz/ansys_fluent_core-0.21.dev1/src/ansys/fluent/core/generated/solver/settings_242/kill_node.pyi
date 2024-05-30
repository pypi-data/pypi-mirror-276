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

from .compute_node import compute_node as compute_node_cls
from .invalidate_case import invalidate_case as invalidate_case_cls

class kill_node(Command):
    fluent_name = ...
    argument_names = ...
    compute_node: compute_node_cls = ...
    invalidate_case: invalidate_case_cls = ...
