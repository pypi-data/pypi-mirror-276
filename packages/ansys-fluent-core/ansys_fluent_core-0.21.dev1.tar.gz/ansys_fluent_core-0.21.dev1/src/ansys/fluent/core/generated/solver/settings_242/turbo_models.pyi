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

from .enabled_36 import enabled as enabled_cls
from .general_turbo_interface import general_turbo_interface as general_turbo_interface_cls
from .export_boundary_mesh import export_boundary_mesh as export_boundary_mesh_cls

class turbo_models(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    general_turbo_interface: general_turbo_interface_cls = ...
    command_names = ...

    def export_boundary_mesh(self, filename_2: str, boundary_list: List[str], global_: bool):
        """
        Export boundary mesh file.
        
        Parameters
        ----------
            filename_2 : str
                Output file name.
            boundary_list : typing.List[str]
                Select boundary zones for exporting mesh.
            global_ : bool
                Enable/disable output of mesh global number.
        
        """

