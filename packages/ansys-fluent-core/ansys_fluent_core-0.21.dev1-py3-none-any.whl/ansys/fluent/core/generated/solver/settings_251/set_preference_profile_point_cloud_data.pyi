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

from .profile_point_marker import profile_point_marker as profile_point_marker_cls
from .profile_point_marker_size import profile_point_marker_size as profile_point_marker_size_cls
from .profile_point_marker_color import profile_point_marker_color as profile_point_marker_color_cls

class set_preference_profile_point_cloud_data(Command):
    fluent_name = ...
    argument_names = ...
    profile_point_marker: profile_point_marker_cls = ...
    profile_point_marker_size: profile_point_marker_size_cls = ...
    profile_point_marker_color: profile_point_marker_color_cls = ...
