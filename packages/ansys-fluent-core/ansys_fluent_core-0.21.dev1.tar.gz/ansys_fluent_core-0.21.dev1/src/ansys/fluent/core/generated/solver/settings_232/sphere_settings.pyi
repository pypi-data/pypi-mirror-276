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

from .scale_2 import scale as scale_cls
from .sphere_lod import sphere_lod as sphere_lod_cls
from .options_12 import options as options_cls

class sphere_settings(Group):
    fluent_name = ...
    child_names = ...
    scale: scale_cls = ...
    sphere_lod: sphere_lod_cls = ...
    options: options_cls = ...
