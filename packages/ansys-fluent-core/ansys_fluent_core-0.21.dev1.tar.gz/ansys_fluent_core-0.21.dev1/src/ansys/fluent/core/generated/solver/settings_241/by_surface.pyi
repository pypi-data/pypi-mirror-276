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

from .use_inherent_material_color_1 import use_inherent_material_color as use_inherent_material_color_cls
from .reset_2 import reset as reset_cls
from .list_surfaces_by_color import list_surfaces_by_color as list_surfaces_by_color_cls
from .list_surfaces_by_material import list_surfaces_by_material as list_surfaces_by_material_cls
from .surfaces_8 import surfaces as surfaces_cls

class by_surface(Group):
    fluent_name = ...
    child_names = ...
    use_inherent_material_color: use_inherent_material_color_cls = ...
    command_names = ...

    def reset(self, ):
        """
        To reset colors and/or materials to the defaults.
        """

    def list_surfaces_by_color(self, ):
        """
        To list the surfaces by its color.
        """

    def list_surfaces_by_material(self, ):
        """
        To list the surfaces by its material.
        """

    def surfaces(self, surface_names: List[str], color: str, material: str):
        """
        Select the surface(s) to specify colors and/or materials.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Enter the list of surfaces to set color and material.
            color : str
                'color' child.
            material : str
                'material' child.
        
        """

