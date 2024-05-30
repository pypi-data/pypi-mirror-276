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

from .nodes import nodes as nodes_cls
from .edges_1 import edges as edges_cls
from .faces_1 import faces as faces_cls
from .partitions import partitions as partitions_cls
from .overset_2 import overset as overset_cls
from .gap import gap as gap_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    nodes: nodes_cls = ...
    edges: edges_cls = ...
    faces: faces_cls = ...
    partitions: partitions_cls = ...
    overset: overset_cls = ...
    gap: gap_cls = ...
