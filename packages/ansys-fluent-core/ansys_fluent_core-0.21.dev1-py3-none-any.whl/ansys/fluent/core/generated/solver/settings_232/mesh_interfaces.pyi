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

from .auto_options import auto_options as auto_options_cls
from .interface_1 import interface as interface_cls
from .turbo_interface import turbo_interface as turbo_interface_cls
from .continuity_after_bc import continuity_after_bc as continuity_after_bc_cls
from .verbosity_4 import verbosity as verbosity_cls
from .si_with_nodes import si_with_nodes as si_with_nodes_cls
from .coupled_wall_between_solids import coupled_wall_between_solids as coupled_wall_between_solids_cls
from .enable_visualization_of_interfaces import enable_visualization_of_interfaces as enable_visualization_of_interfaces_cls
from .mapped_interface_options import mapped_interface_options as mapped_interface_options_cls
from .non_conformal_interface_numerics import non_conformal_interface_numerics as non_conformal_interface_numerics_cls
from .delete_1 import delete as delete_cls
from .display_1 import display as display_cls
from .list_1 import list as list_cls
from .make_phaselag_from_boundaries import make_phaselag_from_boundaries as make_phaselag_from_boundaries_cls
from .make_phaselag_from_periodic import make_phaselag_from_periodic as make_phaselag_from_periodic_cls
from .delete_all import delete_all as delete_all_cls
from .improve_quality_1 import improve_quality as improve_quality_cls
from .enable_one_to_one_pairing import enable_one_to_one_pairing as enable_one_to_one_pairing_cls
from .auto_pairing import auto_pairing as auto_pairing_cls
from .enable_motion_transfer_across_interfaces import enable_motion_transfer_across_interfaces as enable_motion_transfer_across_interfaces_cls
from .remove_left_handed_interface_faces import remove_left_handed_interface_faces as remove_left_handed_interface_faces_cls
from .get_non_overlapping_zone_name import get_non_overlapping_zone_name as get_non_overlapping_zone_name_cls

class mesh_interfaces(Group):
    fluent_name = ...
    child_names = ...
    auto_options: auto_options_cls = ...
    interface: interface_cls = ...
    turbo_interface: turbo_interface_cls = ...
    continuity_after_bc: continuity_after_bc_cls = ...
    verbosity: verbosity_cls = ...
    si_with_nodes: si_with_nodes_cls = ...
    coupled_wall_between_solids: coupled_wall_between_solids_cls = ...
    enable_visualization_of_interfaces: enable_visualization_of_interfaces_cls = ...
    mapped_interface_options: mapped_interface_options_cls = ...
    non_conformal_interface_numerics: non_conformal_interface_numerics_cls = ...
    command_names = ...

    def delete(self, si_delete: str):
        """
        Delete a mesh interface.
        
        Parameters
        ----------
            si_delete : str
                'si_delete' child.
        
        """

    def display(self, zones: List[int]):
        """
        Display specified mesh interface zone.
        
        Parameters
        ----------
            zones : typing.List[int]
                'zones' child.
        
        """

    def list(self, ):
        """
        List all mesh-interfaces.
        """

    def make_phaselag_from_boundaries(self, sb0: int, sb1: int, angle: Union[float, str], pl_name: str):
        """
        Make interface zones phase lagged.
        
        Parameters
        ----------
            sb0 : int
                Enter id/name of zone to convert to phase lag side 1.
            sb1 : int
                Enter id/name of zone to convert to phase lag side 2.
            angle : real
                'angle' child.
            pl_name : str
                'pl_name' child.
        
        """

    def make_phaselag_from_periodic(self, per_id: int):
        """
        Convert periodic interface to phase lagged.
        
        Parameters
        ----------
            per_id : int
                'per_id' child.
        
        """

    def delete_all(self, ):
        """
        Delete all mesh interfaces.
        """

    def improve_quality(self, check_mapped_interface_quality: bool, complete: bool, tol_percentage_increment: Union[float, str]):
        """
        Improve mesh interface quality.
        
        Parameters
        ----------
            check_mapped_interface_quality : bool
                Check Mapped Interface Qaulity.
            complete : bool
                Continue to improve the mapped interface quality.
            tol_percentage_increment : real
                'tol_percentage_increment' child.
        
        """

    def enable_one_to_one_pairing(self, o2o_flag: bool, toggle: bool, delete_empty: bool):
        """
        Use the default one-to-one interface creation method?.
        
        Parameters
        ----------
            o2o_flag : bool
                Use the default one-to-one interface creation method?.
            toggle : bool
                Would you like to proceed?.
            delete_empty : bool
                Delete empty interface interior zones from non-overlapping interfaces?.
        
        """

    def auto_pairing(self, all: bool, one_to_one_pairing: bool, new_si_id: List[str], si_create: bool, si_name: str, apply_mapped: bool, static_interface: bool):
        """
        Automatically pair and create mesh interfaces for some or all interface zones.
        
        Parameters
        ----------
            all : bool
                'all' child.
            one_to_one_pairing : bool
                'one_to_one_pairing' child.
            new_si_id : typing.List[str]
                Select unintersected interface zones for pairing.
            si_create : bool
                'si_create' child.
            si_name : str
                Enter a prefix for mesh interface names.
            apply_mapped : bool
                Apply Mapped option at solids.
            static_interface : bool
                'static_interface' child.
        
        """

    def enable_motion_transfer_across_interfaces(self, enabled: bool, option_name: str):
        """
        Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
        
        Parameters
        ----------
            enabled : bool
                'enabled' child.
            option_name : str
                'option_name' child.
        
        """

    def remove_left_handed_interface_faces(self, enable: bool, update: bool):
        """
        Remove left-handed faces during mesh interface creation.
        
        Parameters
        ----------
            enable : bool
                Remove left-handed faces on mesh interfaces.
            update : bool
                'update' child.
        
        """

    query_names = ...

    def get_non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Enter zone name.
        
        """

