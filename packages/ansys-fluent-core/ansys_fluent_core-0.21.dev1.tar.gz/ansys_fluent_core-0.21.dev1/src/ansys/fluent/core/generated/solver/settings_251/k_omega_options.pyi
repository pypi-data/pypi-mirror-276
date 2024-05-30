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

from .kw_low_re_correction import kw_low_re_correction as kw_low_re_correction_cls
from .kw_shear_correction import kw_shear_correction as kw_shear_correction_cls

class k_omega_options(Group):
    fluent_name = ...
    child_names = ...
    kw_low_re_correction: kw_low_re_correction_cls = ...
    kw_shear_correction: kw_shear_correction_cls = ...
