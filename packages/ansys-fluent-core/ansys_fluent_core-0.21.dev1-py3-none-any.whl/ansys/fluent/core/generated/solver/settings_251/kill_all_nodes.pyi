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

from .delete_all_compute_nodes import delete_all_compute_nodes as delete_all_compute_nodes_cls

class kill_all_nodes(Command):
    fluent_name = ...
    argument_names = ...
    delete_all_compute_nodes: delete_all_compute_nodes_cls = ...
