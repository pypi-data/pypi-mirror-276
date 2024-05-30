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

from .interface_2 import interface as interface_cls
from .auto_options import auto_options as auto_options_cls
from .turbo_interface import turbo_interface as turbo_interface_cls
from .verbosity_7 import verbosity as verbosity_cls
from .enforce_continuity_after_bc import enforce_continuity_after_bc as enforce_continuity_after_bc_cls
from .coupled_interfaces_inherit_bcs import coupled_interfaces_inherit_bcs as coupled_interfaces_inherit_bcs_cls
from .enable_si_with_nodes import enable_si_with_nodes as enable_si_with_nodes_cls
from .enforce_coupled_wall_between_solids import enforce_coupled_wall_between_solids as enforce_coupled_wall_between_solids_cls
from .enable_visualization_of_interfaces import enable_visualization_of_interfaces as enable_visualization_of_interfaces_cls
from .mapped_interface_options import mapped_interface_options as mapped_interface_options_cls
from .non_conformal_interface_numerics import non_conformal_interface_numerics as non_conformal_interface_numerics_cls
from .delete_2 import delete as delete_cls
from .list_1 import list as list_cls
from .delete_all import delete_all as delete_all_cls
from .display_1 import display as display_cls
from .one_to_one_pairing import one_to_one_pairing as one_to_one_pairing_cls
from .delete_interfaces_with_small_overlap import delete_interfaces_with_small_overlap as delete_interfaces_with_small_overlap_cls
from .create_manually import create_manually as create_manually_cls
from .auto_pairing import auto_pairing as auto_pairing_cls
from .improve_quality_1 import improve_quality as improve_quality_cls
from .make_phaselag_from_boundaries import make_phaselag_from_boundaries as make_phaselag_from_boundaries_cls
from .make_phaselag_from_periodic import make_phaselag_from_periodic as make_phaselag_from_periodic_cls
from .transfer_motion_across_interfaces import transfer_motion_across_interfaces as transfer_motion_across_interfaces_cls
from .remove_left_handed_interface_faces import remove_left_handed_interface_faces as remove_left_handed_interface_faces_cls
from .non_overlapping_zone_name_1 import non_overlapping_zone_name as non_overlapping_zone_name_cls

class mesh_interfaces(Group):
    fluent_name = ...
    child_names = ...
    interface: interface_cls = ...
    auto_options: auto_options_cls = ...
    turbo_interface: turbo_interface_cls = ...
    verbosity: verbosity_cls = ...
    enforce_continuity_after_bc: enforce_continuity_after_bc_cls = ...
    coupled_interfaces_inherit_bcs: coupled_interfaces_inherit_bcs_cls = ...
    enable_si_with_nodes: enable_si_with_nodes_cls = ...
    enforce_coupled_wall_between_solids: enforce_coupled_wall_between_solids_cls = ...
    enable_visualization_of_interfaces: enable_visualization_of_interfaces_cls = ...
    mapped_interface_options: mapped_interface_options_cls = ...
    non_conformal_interface_numerics: non_conformal_interface_numerics_cls = ...
    command_names = ...

    def delete(self, name: str):
        """
        Delete a mesh interface.
        
        Parameters
        ----------
            name : str
                Mesh interface name to be deleted.
        
        """

    def list(self, ):
        """
        List all mesh-interfaces.
        """

    def delete_all(self, ):
        """
        Delete all mesh interfaces.
        """

    def display(self, zones: List[str]):
        """
        Display specified mesh interface zone.
        
        Parameters
        ----------
            zones : typing.List[str]
                Zone-name to be displayed.
        
        """

    def one_to_one_pairing(self, one_to_one_interface: bool, proceed: bool, delete_empty: bool):
        """
        Use the default one-to-one interface creation method?.
        
        Parameters
        ----------
            one_to_one_interface : bool
                Use the default one-to-one interface creation method?.
            proceed : bool
                Would you like to proceed?.
            delete_empty : bool
                Delete empty interface interior zones from non-overlapping interfaces?.
        
        """

    def delete_interfaces_with_small_overlap(self, delete: bool, overlapping_percentage_threshold: Union[float, str]):
        """
        Delete mesh interfaces that have an area percentage under a specified value.
        
        Parameters
        ----------
            delete : bool
                Delete mesh interfaces that have an area percentage under a specified value?.
            overlapping_percentage_threshold : real
                Enter the area percentage used for deletion (%).
        
        """

    def create_manually(self, name: str, zone_list_1: List[str], zone_list_2: List[str]):
        """
        Create one-to-one interfaces between two groups of boundary zones even if they do not currently overlap.
        
        Parameters
        ----------
            name : str
                Enter a prefix for mesh interface names.
            zone_list_1 : typing.List[str]
                Enter the boundary zones belonging to the first group.
            zone_list_2 : typing.List[str]
                Enter the boundary zones belonging to the second group.
        
        """

    def auto_pairing(self, pair_all: bool, one_to_one_pairs: bool, interface_zones: List[str], create: bool, name: str, apply_mapped: bool, static_interface: bool):
        """
        Automatically pair and create mesh interfaces for some or all interface zones.
        
        Parameters
        ----------
            pair_all : bool
                Automatic pairing of all unintersected interface zones?.
            one_to_one_pairs : bool
                Create one-to-one pairs only?.
            interface_zones : typing.List[str]
                Select unintersected interface zones for pairing.
            create : bool
                Create mesh interfaces with all these pairs?.
            name : str
                Enter a prefix for mesh interface names.
            apply_mapped : bool
                Apply Mapped option at solids.
            static_interface : bool
                Static?.
        
        """

    def improve_quality(self, check_mapped_interface_quality: bool, proceed: bool, tol_percentage_increment: Union[float, str]):
        """
        Improve mesh interface quality.
        
        Parameters
        ----------
            check_mapped_interface_quality : bool
                Check Mapped Interface Qaulity.
            proceed : bool
                Continue to improve the mapped interface quality.
            tol_percentage_increment : real
                Enter a percentage increment for tolerance (%).
        
        """

    def make_phaselag_from_boundaries(self, side_1: str, side_2: str, angle: Union[float, str], interface_name: str):
        """
        Make interface zones phase lagged.
        
        Parameters
        ----------
            side_1 : str
                Enter id/name of zone to convert to phase lag side 1.
            side_2 : str
                Enter id/name of zone to convert to phase lag side 2.
            angle : real
                Enter rotation angle.
            interface_name : str
                Enter a name for this phaselag interface.
        
        """

    def make_phaselag_from_periodic(self, periodic_zone_name: str):
        """
        Convert periodic interface to phase lagged.
        
        Parameters
        ----------
            periodic_zone_name : str
                Enter periodic zone id/name.
        
        """

    def transfer_motion_across_interfaces(self, enabled: bool, option_name: str):
        """
        Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
        
        Parameters
        ----------
            enabled : bool
                Enable motion transfer across mesh interfaces?.
            option_name : str
                Enter transfer type.
        
        """

    def remove_left_handed_interface_faces(self, enable: bool, update: bool):
        """
        Remove left-handed faces during mesh interface creation.
        
        Parameters
        ----------
            enable : bool
                Remove left-handed faces on mesh interfaces.
            update : bool
                Update existing mesh interfaces?.
        
        """

    def non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Enter zone id/name.
        
        """

