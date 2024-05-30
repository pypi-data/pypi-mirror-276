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

from .surfaces_19 import surfaces as surfaces_cls
from .reset_reference_mesh import reset_reference_mesh as reset_reference_mesh_cls
from .overlay_reference import overlay_reference as overlay_reference_cls
from .export_displacements import export_displacements as export_displacements_cls

class history(Group):
    fluent_name = ...
    child_names = ...
    surfaces: surfaces_cls = ...
    command_names = ...

    def reset_reference_mesh(self, ):
        """
        Save the current mesh as the reference mesh.
        """

    def overlay_reference(self, ):
        """
        Overlay reference mesh.
        """

    def export_displacements(self, file_name: str):
        """
        Export the total computed optimal displacements.
        
        Parameters
        ----------
            file_name : str
                Displacements file name.
        
        """

