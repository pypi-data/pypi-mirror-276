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

from .multi_grid_controls import multi_grid_controls as multi_grid_controls_cls
from .algebric_mg_controls import algebric_mg_controls as algebric_mg_controls_cls
from .fas_mg_controls import fas_mg_controls as fas_mg_controls_cls
from .amg_gpgpu_options import amg_gpgpu_options as amg_gpgpu_options_cls

class multi_grid(Group):
    fluent_name = ...
    child_names = ...
    multi_grid_controls: multi_grid_controls_cls = ...
    algebric_mg_controls: algebric_mg_controls_cls = ...
    fas_mg_controls: fas_mg_controls_cls = ...
    amg_gpgpu_options: amg_gpgpu_options_cls = ...
