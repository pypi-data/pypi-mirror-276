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

from .enable_scale_all import enable_scale_all as enable_scale_all_cls
from .disable_scale_all import disable_scale_all as disable_scale_all_cls
from .interface_name_2 import interface_name as interface_name_cls
from .scale_2 import scale as scale_cls

class enforce_flux_scaling(Command):
    fluent_name = ...
    argument_names = ...
    enable_scale_all: enable_scale_all_cls = ...
    disable_scale_all: disable_scale_all_cls = ...
    interface_name: interface_name_cls = ...
    scale: scale_cls = ...
