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

from .surface_id_val import surface_id_val as surface_id_val_cls
from .min_feature_size import min_feature_size as min_feature_size_cls
from .proj_plane_norm_comp import proj_plane_norm_comp as proj_plane_norm_comp_cls

class projected_surface_area(Command):
    fluent_name = ...
    argument_names = ...
    surface_id_val: surface_id_val_cls = ...
    min_feature_size: min_feature_size_cls = ...
    proj_plane_norm_comp: proj_plane_norm_comp_cls = ...
