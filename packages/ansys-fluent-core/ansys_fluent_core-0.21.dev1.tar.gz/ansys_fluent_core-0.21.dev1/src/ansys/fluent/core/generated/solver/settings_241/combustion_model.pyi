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

from .option_7 import option as option_cls
from .cbk import cbk as cbk_cls
from .kinetics_diffusion_limited import kinetics_diffusion_limited as kinetics_diffusion_limited_cls
from .intrinsic_model import intrinsic_model as intrinsic_model_cls
from .multiple_surface_reactions import multiple_surface_reactions as multiple_surface_reactions_cls

class combustion_model(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    cbk: cbk_cls = ...
    kinetics_diffusion_limited: kinetics_diffusion_limited_cls = ...
    intrinsic_model: intrinsic_model_cls = ...
    multiple_surface_reactions: multiple_surface_reactions_cls = ...
