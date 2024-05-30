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

from .skip_3 import skip as skip_cls
from .reverse_surfaces import reverse_surfaces as reverse_surfaces_cls

class orientation(Group):
    fluent_name = ...
    child_names = ...
    skip: skip_cls = ...
    command_names = ...

    def reverse_surfaces(self, surfaces: List[str]):
        """
        Reverse selected surfaces.
        
        Parameters
        ----------
            surfaces : typing.List[str]
                Surfaces orientations to be reverse.
        
        """

