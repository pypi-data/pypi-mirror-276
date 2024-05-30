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

from .edc_choice import edc_choice as edc_choice_cls
from .edc_constant_coefficient_options import edc_constant_coefficient_options as edc_constant_coefficient_options_cls
from .edc_pasr_model_options import edc_pasr_model_options as edc_pasr_model_options_cls
from .user_defined_edc_scales import user_defined_edc_scales as user_defined_edc_scales_cls

class edc_model_options(Group):
    fluent_name = ...
    child_names = ...
    edc_choice: edc_choice_cls = ...
    edc_constant_coefficient_options: edc_constant_coefficient_options_cls = ...
    edc_pasr_model_options: edc_pasr_model_options_cls = ...
    user_defined_edc_scales: user_defined_edc_scales_cls = ...
