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
from .create_multiple_plane_surfaces import create_multiple_plane_surfaces as create_multiple_plane_surfaces_cls
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
        Provides access to creating new and editing multiple zone surfaces.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Enter zone name list.
        
        """

    def create_multiple_iso_surfaces(self, field: str, name: str, surfaces: List[str], zones: List[str], min: Union[float, str], max: Union[float, str], iso_value: Union[float, str], no_of_surfaces: int, spacing: Union[float, str]):
        """
        Provides access to creating new and editing multiple iso-surfaces.
        
        Parameters
        ----------
            field : str
                Select the field variable.
            name : str
                Specify the Iso-surface name.
            surfaces : typing.List[str]
                Select the surface(s) that will be used to define the iso-surface.
            zones : typing.List[str]
                Select the zone(s) that will be used to define the iso-surface.
            min : real
                Set min.
            max : real
                Set max.
            iso_value : real
                Specify the iso-value.
            no_of_surfaces : int
                Specify the number of surfaces to be created.
            spacing : real
                Specify the spacing.
        
        """

    def create_multiple_plane_surfaces(self, method: str, name_format: str, x: Union[float, str], y: Union[float, str], z: Union[float, str], point: List[Union[float, str]], normal_computation_method: str, surface_aligned_normal: str, normal: List[Union[float, str]], p0: List[Union[float, str]], p1: List[Union[float, str]], p2: List[Union[float, str]], bounded: bool, sample_points: bool, edges: List[int], surfaces: int, spacing: Union[float, str]):
        """
        Specify the attributes of plane surface.
        
        Parameters
        ----------
            method : str
                Select the method you want to use to create the plane surface. The required inputs vary by method.
            name_format : str
                Specify the Name Format.
            x : real
                Specify the location on the X-axis where the YZ plane will be created.
            y : real
                Specify the location on the Y-axis where the ZX plane will be created.
            z : real
                Specify the location on the Z-axis where the XY plane will be created.
            point : typing.List[real]
                Specify the XYZ coordinates of the point.
            normal_computation_method : str
                Specify the normal computation method.
            surface_aligned_normal : str
                Select the surface you want to compute the normal components.
            normal : typing.List[real]
                Specify the XYZ components of the normal.
            p0 : typing.List[real]
                Specify the XYZ coordinates of Point 1 for the Three Points plane creation method.
            p1 : typing.List[real]
                Specify the XYZ coordinates of Point 2 for the Three Points plane creation method.
            p2 : typing.List[real]
                Specify the XYZ coordinates of Point 3 for the Three Points plane creation method.
            bounded : bool
                Choose whether or not the plane is bounded by its defining points.
            sample_points : bool
                Choose whether or not you want to specify a uniform distribution of points on the plane.
            edges : typing.List[int]
                Specify the point density for edges.
            surfaces : int
                Specify the number of surfaces to be created.
            spacing : real
                Specify the spacing.
        
        """

    def create_group_surfaces(self, surfaces: List[str], name: str):
        """
        Create a group of surfaces.
        
        Parameters
        ----------
            surfaces : typing.List[str]
                Select list of surfaces.
            name : str
                Specify the name for the group surface.
        
        """

    def ungroup_surfaces(self, surface: str):
        """
        Ungroup previously-grouped surfaces.
        
        Parameters
        ----------
            surface : str
                Select the surface to ungroup.
        
        """

    def set_rendering_priority(self, surface: str, priority: str):
        """
        Set the surface rendering priority.
        
        Parameters
        ----------
            surface : str
                Select the surface(s) for surface rendering priority.
            priority : str
                Select the desired rendering priority.
        
        """

    def reset_zone_surfaces(self, ):
        """
        Recreates missing surface zones by resetting the case surface list.
        """

