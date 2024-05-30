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

from .axis import axis as axis_cls
from .degassing import degassing as degassing_cls
from .exhaust_fan import exhaust_fan as exhaust_fan_cls
from .fan import fan as fan_cls
from .geometry_2 import geometry as geometry_cls
from .inlet_vent import inlet_vent as inlet_vent_cls
from .intake_fan import intake_fan as intake_fan_cls
from .interface import interface as interface_cls
from .interior import interior as interior_cls
from .mass_flow_inlet import mass_flow_inlet as mass_flow_inlet_cls
from .mass_flow_outlet import mass_flow_outlet as mass_flow_outlet_cls
from .network import network as network_cls
from .network_end import network_end as network_end_cls
from .outflow import outflow as outflow_cls
from .outlet_vent import outlet_vent as outlet_vent_cls
from .overset import overset as overset_cls
from .periodic import periodic as periodic_cls
from .porous_jump import porous_jump as porous_jump_cls
from .pressure_far_field import pressure_far_field as pressure_far_field_cls
from .pressure_inlet import pressure_inlet as pressure_inlet_cls
from .pressure_outlet import pressure_outlet as pressure_outlet_cls
from .radiator import radiator as radiator_cls
from .rans_les_interface import rans_les_interface as rans_les_interface_cls
from .recirculation_inlet import recirculation_inlet as recirculation_inlet_cls
from .recirculation_outlet import recirculation_outlet as recirculation_outlet_cls
from .shadow import shadow as shadow_cls
from .symmetry import symmetry as symmetry_cls
from .velocity_inlet import velocity_inlet as velocity_inlet_cls
from .wall import wall as wall_cls
from .copy_1 import copy as copy_cls
from .change_type import change_type as change_type_cls
from .slit_face_zone import slit_face_zone as slit_face_zone_cls
from .slit_interior_between_diff_solids import slit_interior_between_diff_solids as slit_interior_between_diff_solids_cls
from .create_all_shell_threads import create_all_shell_threads as create_all_shell_threads_cls
from .recreate_all_shells import recreate_all_shells as recreate_all_shells_cls
from .delete_all_shells import delete_all_shells as delete_all_shells_cls
from .orient_face_zone import orient_face_zone as orient_face_zone_cls

class boundary_conditions(Group, _ChildNamedObjectAccessorMixin):
    fluent_name = ...
    child_names = ...
    axis: axis_cls = ...
    degassing: degassing_cls = ...
    exhaust_fan: exhaust_fan_cls = ...
    fan: fan_cls = ...
    geometry: geometry_cls = ...
    inlet_vent: inlet_vent_cls = ...
    intake_fan: intake_fan_cls = ...
    interface: interface_cls = ...
    interior: interior_cls = ...
    mass_flow_inlet: mass_flow_inlet_cls = ...
    mass_flow_outlet: mass_flow_outlet_cls = ...
    network: network_cls = ...
    network_end: network_end_cls = ...
    outflow: outflow_cls = ...
    outlet_vent: outlet_vent_cls = ...
    overset: overset_cls = ...
    periodic: periodic_cls = ...
    porous_jump: porous_jump_cls = ...
    pressure_far_field: pressure_far_field_cls = ...
    pressure_inlet: pressure_inlet_cls = ...
    pressure_outlet: pressure_outlet_cls = ...
    radiator: radiator_cls = ...
    rans_les_interface: rans_les_interface_cls = ...
    recirculation_inlet: recirculation_inlet_cls = ...
    recirculation_outlet: recirculation_outlet_cls = ...
    shadow: shadow_cls = ...
    symmetry: symmetry_cls = ...
    velocity_inlet: velocity_inlet_cls = ...
    wall: wall_cls = ...
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

    def slit_face_zone(self, zone_id: int):
        """
        Slit a two-sided wall into two connected wall zones.
        
        Parameters
        ----------
            zone_id : int
                'zone_id' child.
        
        """

    def slit_interior_between_diff_solids(self, ):
        """
        Slit interior created between different solids into coupled walls.
        """

    def create_all_shell_threads(self, ):
        """
        Mark all finite thickness wall for shell creation. Shell zones will be created at the start of iterations.
        """

    def recreate_all_shells(self, ):
        """
        Create shell on all the walls where which were deleted using the command delete-all-shells.
        """

    def delete_all_shells(self, ):
        """
        'delete_all_shells' command.
        """

    def orient_face_zone(self, face_zone_id: int):
        """
        Orient the face zone.
        
        Parameters
        ----------
            face_zone_id : int
                'face_zone_id' child.
        
        """

