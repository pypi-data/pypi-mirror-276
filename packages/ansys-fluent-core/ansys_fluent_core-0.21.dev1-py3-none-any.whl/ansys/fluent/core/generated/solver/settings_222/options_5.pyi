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

from .oil_flow import oil_flow as oil_flow_cls
from .reverse import reverse as reverse_cls
from .node_values_1 import node_values as node_values_cls
from .relative_1 import relative as relative_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    oil_flow: oil_flow_cls = ...
    reverse: reverse_cls = ...
    node_values: node_values_cls = ...
    relative: relative_cls = ...
