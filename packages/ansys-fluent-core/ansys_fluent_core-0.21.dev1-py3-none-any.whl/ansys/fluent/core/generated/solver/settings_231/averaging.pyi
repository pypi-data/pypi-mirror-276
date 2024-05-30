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

from .enable_node_based_averaging import enable_node_based_averaging as enable_node_based_averaging_cls
from .average_source_terms import average_source_terms as average_source_terms_cls
from .average_every_step import average_every_step as average_every_step_cls
from .averaging_kernel import averaging_kernel as averaging_kernel_cls

class averaging(Group):
    fluent_name = ...
    child_names = ...
    enable_node_based_averaging: enable_node_based_averaging_cls = ...
    average_source_terms: average_source_terms_cls = ...
    average_every_step: average_every_step_cls = ...
    averaging_kernel: averaging_kernel_cls = ...
