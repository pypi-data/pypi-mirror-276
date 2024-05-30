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

from .pressure_corr_grad import pressure_corr_grad as pressure_corr_grad_cls
from .face_pressure_calculation_method import face_pressure_calculation_method as face_pressure_calculation_method_cls
from .exclude_transient_term_in_face_pressure_calc import exclude_transient_term_in_face_pressure_calc as exclude_transient_term_in_face_pressure_calc_cls

class face_pressure_options(Group):
    fluent_name = ...
    child_names = ...
    pressure_corr_grad: pressure_corr_grad_cls = ...
    face_pressure_calculation_method: face_pressure_calculation_method_cls = ...
    exclude_transient_term_in_face_pressure_calc: exclude_transient_term_in_face_pressure_calc_cls = ...
