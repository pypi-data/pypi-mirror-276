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
from .center import center as center_cls
from .radius import radius as radius_cls
from .display_3 import display as display_cls

class sphere_slice_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    center: center_cls = ...
    radius: radius_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

