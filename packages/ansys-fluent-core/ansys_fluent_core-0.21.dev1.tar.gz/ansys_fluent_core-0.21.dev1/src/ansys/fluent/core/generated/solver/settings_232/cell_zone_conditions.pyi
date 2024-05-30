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

from .fluid_1 import fluid as fluid_cls
from .solid_1 import solid as solid_cls
from .copy_1 import copy as copy_cls
from .change_type import change_type as change_type_cls
from .activate_cell_zone import activate_cell_zone as activate_cell_zone_cls
from .mrf_to_sliding_mesh import mrf_to_sliding_mesh as mrf_to_sliding_mesh_cls
from .convert_all_solid_mrf_to_solid_motion import convert_all_solid_mrf_to_solid_motion as convert_all_solid_mrf_to_solid_motion_cls
from .copy_mrf_to_mesh_motion import copy_mrf_to_mesh_motion as copy_mrf_to_mesh_motion_cls
from .copy_mesh_to_mrf_motion import copy_mesh_to_mrf_motion as copy_mesh_to_mrf_motion_cls

class cell_zone_conditions(Group, _ChildNamedObjectAccessorMixin):
    fluent_name = ...
    child_names = ...
    fluid: fluid_cls = ...
    solid: solid_cls = ...
    command_names = ...

    def copy(self, from_: str, to: List[str], verbosity: bool):
        """
        'copy' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : typing.List[str]
                'to' child.
            verbosity : bool
                'verbosity' child.
        
        """

    def change_type(self, zone_list: List[str], new_type: str):
        """
        'change_type' command.
        
        Parameters
        ----------
            zone_list : typing.List[str]
                'zone_list' child.
            new_type : str
                'new_type' child.
        
        """

    def activate_cell_zone(self, cell_zone_list: List[str]):
        """
        'activate_cell_zone' command.
        
        Parameters
        ----------
            cell_zone_list : typing.List[str]
                'cell_zone_list' child.
        
        """

    def mrf_to_sliding_mesh(self, zone_id: int):
        """
        Change motion specification from MRF to moving mesh.
        
        Parameters
        ----------
            zone_id : int
                'zone_id' child.
        
        """

    def convert_all_solid_mrf_to_solid_motion(self, ):
        """
        Change all solid zones motion specification from MRF to solid motion.
        """

    def copy_mrf_to_mesh_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def copy_mesh_to_mrf_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

