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

from .applied_conditions import applied_conditions as applied_conditions_cls
from .fix_surfaces import fix_surfaces as fix_surfaces_cls
from .display_9 import display as display_cls

class selection(Group):
    fluent_name = ...
    child_names = ...
    applied_conditions: applied_conditions_cls = ...
    fix_surfaces: fix_surfaces_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display the applied design conditions.
        """

