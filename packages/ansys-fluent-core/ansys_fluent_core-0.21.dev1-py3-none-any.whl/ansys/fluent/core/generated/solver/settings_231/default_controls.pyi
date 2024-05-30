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

from .recommended_defaults_for_existing_cases import recommended_defaults_for_existing_cases as recommended_defaults_for_existing_cases_cls
from .revert_to_pre_r20_1_default_settings import revert_to_pre_r20_1_default_settings as revert_to_pre_r20_1_default_settings_cls

class default_controls(Group):
    fluent_name = ...
    child_names = ...
    recommended_defaults_for_existing_cases: recommended_defaults_for_existing_cases_cls = ...
    revert_to_pre_r20_1_default_settings: revert_to_pre_r20_1_default_settings_cls = ...
