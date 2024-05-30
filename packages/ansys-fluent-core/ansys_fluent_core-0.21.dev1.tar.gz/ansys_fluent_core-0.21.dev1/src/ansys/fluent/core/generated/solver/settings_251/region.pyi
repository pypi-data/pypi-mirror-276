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

from .modifiable_zones import modifiable_zones as modifiable_zones_cls
from .region_type import region_type as region_type_cls
from .show_bounding_region import show_bounding_region as show_bounding_region_cls
from .auto_display import auto_display as auto_display_cls
from .cartesian import cartesian as cartesian_cls
from .cylindrical import cylindrical as cylindrical_cls
from .get_bounds import get_bounds as get_bounds_cls
from .larger_region import larger_region as larger_region_cls
from .smaller_region import smaller_region as smaller_region_cls

class region(Group):
    fluent_name = ...
    child_names = ...
    modifiable_zones: modifiable_zones_cls = ...
    region_type: region_type_cls = ...
    show_bounding_region: show_bounding_region_cls = ...
    auto_display: auto_display_cls = ...
    cartesian: cartesian_cls = ...
    cylindrical: cylindrical_cls = ...
    command_names = ...

    def get_bounds(self, bounded_zones: List[str], comfortable_region: bool, automatic_coordinate: bool):
        """
        Get bounds based on selects zones.
        
        Parameters
        ----------
            bounded_zones : typing.List[str]
                Zones used to determine region bounds.
            comfortable_region : bool
                Use comfortable region than the selected zones.
            automatic_coordinate : bool
                Update the cylindrical coordinate system automatically.
        
        """

    def larger_region(self, ):
        """
        Enlarge current region extent.
        """

    def smaller_region(self, ):
        """
        Shrink current region extent.
        """

