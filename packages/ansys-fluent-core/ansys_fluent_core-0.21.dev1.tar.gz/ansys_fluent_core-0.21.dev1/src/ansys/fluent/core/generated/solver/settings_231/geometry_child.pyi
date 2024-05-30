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

from .radius_ratio import radius_ratio as radius_ratio_cls
from .chord import chord as chord_cls
from .twist import twist as twist_cls
from .airfoil_data_file import airfoil_data_file as airfoil_data_file_cls

class geometry_child(Group):
    fluent_name = ...
    child_names = ...
    radius_ratio: radius_ratio_cls = ...
    chord: chord_cls = ...
    twist: twist_cls = ...
    airfoil_data_file: airfoil_data_file_cls = ...
