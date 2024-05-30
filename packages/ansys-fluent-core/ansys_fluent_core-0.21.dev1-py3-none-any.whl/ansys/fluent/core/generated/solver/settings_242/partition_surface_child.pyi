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

from .name import name as name_cls
from .partition_1 import partition_1 as partition_1_cls
from .partition_2 import partition_2 as partition_2_cls
from .interior_cell_faces import interior_cell_faces as interior_cell_faces_cls
from .display_4 import display as display_cls

class partition_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    partition_1: partition_1_cls = ...
    partition_2: partition_2_cls = ...
    interior_cell_faces: interior_cell_faces_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display a surface.
        """

