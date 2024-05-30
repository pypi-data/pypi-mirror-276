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

from .point_surface import point_surface as point_surface_cls
from .line_surface import line_surface as line_surface_cls
from .rake_surface import rake_surface as rake_surface_cls
from .plane_surface import plane_surface as plane_surface_cls
from .iso_surface import iso_surface as iso_surface_cls
from .iso_clip import iso_clip as iso_clip_cls
from .zone_surface import zone_surface as zone_surface_cls
from .partition_surface import partition_surface as partition_surface_cls
from .transform_surface import transform_surface as transform_surface_cls
from .imprint_surface import imprint_surface as imprint_surface_cls
from .plane_slice import plane_slice as plane_slice_cls
from .sphere_slice import sphere_slice as sphere_slice_cls
from .quadric_surface import quadric_surface as quadric_surface_cls
from .surface_cells import surface_cells as surface_cells_cls
from .create_multiple_zone_surfaces import create_multiple_zone_surfaces as create_multiple_zone_surfaces_cls
from .create_multiple_iso_surfaces import create_multiple_iso_surfaces as create_multiple_iso_surfaces_cls
from .create_group_surfaces import create_group_surfaces as create_group_surfaces_cls
from .ungroup_surfaces import ungroup_surfaces as ungroup_surfaces_cls
from .set_rendering_priority import set_rendering_priority as set_rendering_priority_cls
from .reset_zone_surfaces import reset_zone_surfaces as reset_zone_surfaces_cls

class surfaces(Group):
    fluent_name = ...
    child_names = ...
    point_surface: point_surface_cls = ...
    line_surface: line_surface_cls = ...
    rake_surface: rake_surface_cls = ...
    plane_surface: plane_surface_cls = ...
    iso_surface: iso_surface_cls = ...
    iso_clip: iso_clip_cls = ...
    zone_surface: zone_surface_cls = ...
    partition_surface: partition_surface_cls = ...
    transform_surface: transform_surface_cls = ...
    imprint_surface: imprint_surface_cls = ...
    plane_slice: plane_slice_cls = ...
    sphere_slice: sphere_slice_cls = ...
    quadric_surface: quadric_surface_cls = ...
    surface_cells: surface_cells_cls = ...
    command_names = ...

    def create_multiple_zone_surfaces(self, zone_names: List[str]):
        """
        'create_multiple_zone_surfaces' command.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Enter zone name list.
        
        """

    def create_multiple_iso_surfaces(self, field: str, name: str, surfaces: List[str], zones: List[str], iso_value: Union[float, str], no_of_surfaces: int, spacing: Union[float, str]):
        """
        'create_multiple_iso_surfaces' command.
        
        Parameters
        ----------
            field : str
                Specify Field.
            name : str
                'name' child.
            surfaces : typing.List[str]
                Select surface.
            zones : typing.List[str]
                Enter cell zone name list.
            iso_value : real
                'iso_value' child.
            no_of_surfaces : int
                'no_of_surfaces' child.
            spacing : real
                'spacing' child.
        
        """

    def create_group_surfaces(self, surfaces: List[str], name: str):
        """
        'create_group_surfaces' command.
        
        Parameters
        ----------
            surfaces : typing.List[str]
                Select list of surfaces.
            name : str
                'name' child.
        
        """

    def ungroup_surfaces(self, surface: str):
        """
        'ungroup_surfaces' command.
        
        Parameters
        ----------
            surface : str
                'surface' child.
        
        """

    def set_rendering_priority(self, surface: str, priority: str):
        """
        'set_rendering_priority' command.
        
        Parameters
        ----------
            surface : str
                Select surface.
            priority : str
                Select surface.
        
        """

    def reset_zone_surfaces(self, ):
        """
        'reset_zone_surfaces' command.
        """

