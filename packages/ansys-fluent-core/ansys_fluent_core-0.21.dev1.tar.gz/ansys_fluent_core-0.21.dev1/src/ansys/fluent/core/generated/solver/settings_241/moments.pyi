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

from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_of_moments import num_of_moments as num_of_moments_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .filename_1 import filename as filename_cls

class moments(Command):
    fluent_name = ...
    argument_names = ...
    surface_list: surface_list_cls = ...
    volume_list: volume_list_cls = ...
    num_of_moments: num_of_moments_cls = ...
    write_to_file: write_to_file_cls = ...
    filename: filename_cls = ...
