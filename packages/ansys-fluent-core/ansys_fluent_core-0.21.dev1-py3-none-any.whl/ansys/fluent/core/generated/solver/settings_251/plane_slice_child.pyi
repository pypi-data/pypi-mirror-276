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
from .normal import normal as normal_cls
from .distance_from_origin import distance_from_origin as distance_from_origin_cls
from .display_4 import display as display_cls

class plane_slice_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    normal: normal_cls = ...
    distance_from_origin: distance_from_origin_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display a surface.
        """

