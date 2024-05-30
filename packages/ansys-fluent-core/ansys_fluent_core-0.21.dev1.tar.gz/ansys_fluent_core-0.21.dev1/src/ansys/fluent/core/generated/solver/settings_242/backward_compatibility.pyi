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

from .pre_24r2_mp_discretization import pre_24r2_mp_discretization as pre_24r2_mp_discretization_cls

class backward_compatibility(Group):
    fluent_name = ...
    command_names = ...

    def pre_24r2_mp_discretization(self, enabled: bool):
        """
        Pre 24R2 discretization for the mixing-plane.
        
        Parameters
        ----------
            enabled : bool
                Enable/Disable enhanced discretization for the mixing-plane.
        
        """

