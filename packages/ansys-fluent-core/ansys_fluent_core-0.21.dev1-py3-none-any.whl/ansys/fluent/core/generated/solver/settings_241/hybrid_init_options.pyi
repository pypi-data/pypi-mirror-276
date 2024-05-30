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

from .general_settings_1 import general_settings as general_settings_cls
from .turbulent_setting import turbulent_setting as turbulent_setting_cls
from .species_setting import species_setting as species_setting_cls

class hybrid_init_options(Group):
    fluent_name = ...
    child_names = ...
    general_settings: general_settings_cls = ...
    turbulent_setting: turbulent_setting_cls = ...
    species_setting: species_setting_cls = ...
