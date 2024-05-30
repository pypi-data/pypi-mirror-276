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

from .surfaces_19 import surfaces as surfaces_cls
from .scale_7 import scale as scale_cls
from .transparency_2 import transparency as transparency_cls
from .displayed_meshes import displayed_meshes as displayed_meshes_cls
from .outline_1 import outline as outline_cls
from .interior_3 import interior as interior_cls
from .display_10 import display as display_cls
from .export_stl import export_stl as export_stl_cls

class preview(Group):
    fluent_name = ...
    child_names = ...
    surfaces: surfaces_cls = ...
    scale: scale_cls = ...
    transparency: transparency_cls = ...
    displayed_meshes: displayed_meshes_cls = ...
    command_names = ...

    def outline(self, ):
        """
        Select boundary surfaces.
        """

    def interior(self, ):
        """
        Select interior surfaces.
        """

    def display(self, ):
        """
        Select interior surfaces.
        """

    def export_stl(self, file_name: str):
        """
        Export specified surfaces from as an .stl file.
        
        Parameters
        ----------
            file_name : str
                Export specified surfaces from 3D cases as an .stl file.
        
        """

