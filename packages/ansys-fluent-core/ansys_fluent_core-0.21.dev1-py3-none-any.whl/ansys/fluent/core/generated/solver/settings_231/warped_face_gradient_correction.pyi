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

from .turbulence_options import turbulence_options as turbulence_options_cls
from .enable_8 import enable as enable_cls

class warped_face_gradient_correction(Group):
    fluent_name = ...
    child_names = ...
    turbulence_options: turbulence_options_cls = ...
    command_names = ...

    def enable(self, enable: bool, gradient_correction_mode: str):
        """
        Enable Warped-Face Gradient Correction.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
            gradient_correction_mode : str
                'gradient_correction_mode' child.
        
        """

