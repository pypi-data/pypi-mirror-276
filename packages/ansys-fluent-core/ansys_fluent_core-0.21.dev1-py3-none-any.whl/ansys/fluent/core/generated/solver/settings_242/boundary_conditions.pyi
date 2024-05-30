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

from .axis_1 import axis as axis_cls
from .degassing import degassing as degassing_cls
from .exhaust_fan import exhaust_fan as exhaust_fan_cls
from .fan import fan as fan_cls
from .geometry_4 import geometry as geometry_cls
from .inlet_vent import inlet_vent as inlet_vent_cls
from .intake_fan import intake_fan as intake_fan_cls
from .interface_1 import interface as interface_cls
from .interior_1 import interior as interior_cls
from .mass_flow_inlet import mass_flow_inlet as mass_flow_inlet_cls
from .mass_flow_outlet import mass_flow_outlet as mass_flow_outlet_cls
from .network import network as network_cls
from .network_end_1 import network_end as network_end_cls
from .outflow import outflow as outflow_cls
from .outlet_vent import outlet_vent as outlet_vent_cls
from .overset import overset as overset_cls
from .periodic_1 import periodic as periodic_cls
from .porous_jump_1 import porous_jump as porous_jump_cls
from .pressure_far_field import pressure_far_field as pressure_far_field_cls
from .pressure_inlet import pressure_inlet as pressure_inlet_cls
from .pressure_outlet import pressure_outlet as pressure_outlet_cls
from .radiator_1 import radiator as radiator_cls
from .rans_les_interface import rans_les_interface as rans_les_interface_cls
from .recirculation_inlet_1 import recirculation_inlet as recirculation_inlet_cls
from .recirculation_outlet_1 import recirculation_outlet as recirculation_outlet_cls
from .shadow import shadow as shadow_cls
from .symmetry import symmetry as symmetry_cls
from .velocity_inlet import velocity_inlet as velocity_inlet_cls
from .wall import wall as wall_cls
from .non_reflecting_bc import non_reflecting_bc as non_reflecting_bc_cls
from .perforated_wall import perforated_wall as perforated_wall_cls
from .settings_1 import settings as settings_cls
from .copy_1 import copy as copy_cls
from .set_zone_type import set_zone_type as set_zone_type_cls
from .slit_face_zone import slit_face_zone as slit_face_zone_cls
from .non_overlapping_zone_name import non_overlapping_zone_name as non_overlapping_zone_name_cls
from .slit_interior_between_diff_solids import slit_interior_between_diff_solids as slit_interior_between_diff_solids_cls
from .create_all_shell_threads import create_all_shell_threads as create_all_shell_threads_cls
from .recreate_all_shells import recreate_all_shells as recreate_all_shells_cls
from .delete_all_shells import delete_all_shells as delete_all_shells_cls
from .orient_face_zone import orient_face_zone as orient_face_zone_cls
from .knudsen_number_calculator import knudsen_number_calculator as knudsen_number_calculator_cls
from .set_zone_name import set_zone_name as set_zone_name_cls
from .add_suffix_or_prefix import add_suffix_or_prefix as add_suffix_or_prefix_cls
from .rename_by_adjacency import rename_by_adjacency as rename_by_adjacency_cls
from .rename_to_default import rename_to_default as rename_to_default_cls

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
    non_reflecting_bc: non_reflecting_bc_cls = ...
    perforated_wall: perforated_wall_cls = ...
    settings: settings_cls = ...
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

    def slit_face_zone(self, zone_name: str):
        """
        Slit a two-sided wall into two connected wall zones.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
        
        """

    def non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
        
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
        Delete all shell zones and switch off shell conduction on all the walls. These zones can be recreated using the command recreate-all-shells.
        """

    def orient_face_zone(self, zone_name: str):
        """
        Orient the face zone.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
        
        """

    def knudsen_number_calculator(self, length: Union[float, str], boundary: str):
        """
        Utility to compute Kudsen number based on characteristic length and boundary information.
        
        Parameters
        ----------
            length : real
                Characteristic physics length.
            boundary : str
                Give flow boundary name.
        
        """

    def set_zone_name(self, zonename: str, newname: str):
        """
        Give a zone a new name.
        
        Parameters
        ----------
            zonename : str
                Enter a zone name.
            newname : str
                Give a new zone name.
        
        """

    def add_suffix_or_prefix(self, zone_name: List[str], append: bool, text: str):
        """
        Add suffix or prefix to zone name.
        
        Parameters
        ----------
            zone_name : typing.List[str]
                Enter zone name list.
            append : bool
                Add suffix to zone name.
            text : str
                Add prefix to zone name.
        
        """

    def rename_by_adjacency(self, zone_name: List[str], abbreviate_types: bool, exclude: bool):
        """
        Rename zone to adjacent zones.
        
        Parameters
        ----------
            zone_name : typing.List[str]
                Enter zone name list.
            abbreviate_types : bool
                Select to provide abbreviate types.
            exclude : bool
                Select to exclude custom names.
        
        """

    def rename_to_default(self, zone_name: List[str], abbrev: bool, exclude: bool):
        """
        Rename zone to default name.
        
        Parameters
        ----------
            zone_name : typing.List[str]
                Enter zone name list.
            abbrev : bool
                Select to provide abbreviate types.
            exclude : bool
                Select to exclude custom names.
        
        """

