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

from .profile_name_1 import profile_name as profile_name_cls
from .field_contour import field_contour as field_contour_cls
from .field_variable import field_variable as field_variable_cls

class display_profile_point_cloud_data(Command):
    fluent_name = ...
    argument_names = ...
    profile_name: profile_name_cls = ...
    field_contour: field_contour_cls = ...
    field_variable: field_variable_cls = ...
