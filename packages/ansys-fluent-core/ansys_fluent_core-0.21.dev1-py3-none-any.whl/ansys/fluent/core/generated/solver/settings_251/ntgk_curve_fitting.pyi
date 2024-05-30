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

from .filename_4 import filename as filename_cls
from .capacity import capacity as capacity_cls
from .number_dod_level import number_dod_level as number_dod_level_cls
from .min_dod import min_dod as min_dod_cls
from .max_dod import max_dod as max_dod_cls
from .capacity_fade_enabled import capacity_fade_enabled as capacity_fade_enabled_cls

class ntgk_curve_fitting(Command):
    fluent_name = ...
    argument_names = ...
    filename: filename_cls = ...
    capacity: capacity_cls = ...
    number_dod_level: number_dod_level_cls = ...
    min_dod: min_dod_cls = ...
    max_dod: max_dod_cls = ...
    capacity_fade_enabled: capacity_fade_enabled_cls = ...
