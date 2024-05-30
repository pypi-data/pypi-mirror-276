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

from .zone_name_1 import zone_name as zone_name_cls
from .overwrite import overwrite as overwrite_cls

class copy_mesh_to_mrf_motion(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    overwrite: overwrite_cls = ...
