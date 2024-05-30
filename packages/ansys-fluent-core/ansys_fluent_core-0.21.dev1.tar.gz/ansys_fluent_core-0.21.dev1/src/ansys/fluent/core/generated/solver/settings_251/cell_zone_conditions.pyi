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
from .solid_2 import solid as solid_cls
from .copy_1 import copy as copy_cls
from .set_zone_type import set_zone_type as set_zone_type_cls
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
        Copy boundary conditions to another zone.
        
        Parameters
        ----------
            from_ : str
                Copy boundary conditions from zone.
            to : typing.List[str]
                Copy boundary conditions to zone.
            verbosity : bool
                Copy boundary conditions: Print more information.
        
        """

    def set_zone_type(self, zone_list: List[str], new_type: str):
        """
        Set a zone's type.
        
        Parameters
        ----------
            zone_list : typing.List[str]
                Enter zone name list.
            new_type : str
                Give new zone type.
        
        """

    def activate_cell_zone(self, cell_zone_list: List[str]):
        """
        Activate a cell thread.
        
        Parameters
        ----------
            cell_zone_list : typing.List[str]
                Enter id/name of cell-zones to activate.
        
        """

    def mrf_to_sliding_mesh(self, cell_zone_name: str):
        """
        Change motion specification from MRF to moving mesh.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a cell zone name.
        
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
                Enter a zone name.
            overwrite : bool
                Specify if you want to overwrite the motion variables.
        
        """

    def copy_mesh_to_mrf_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
            overwrite : bool
                Specify if you want to overwrite the motion variables.
        
        """

