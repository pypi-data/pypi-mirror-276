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

from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .tolerance1 import tolerance1 as tolerance1_cls
from .tolerance2 import tolerance2 as tolerance2_cls
from .update import update as update_cls

class tolerance(Command):
    fluent_name = ...
    argument_names = ...
    use_local_edge_length_factor: use_local_edge_length_factor_cls = ...
    tolerance1: tolerance1_cls = ...
    tolerance2: tolerance2_cls = ...
    update: update_cls = ...
