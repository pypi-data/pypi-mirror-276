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

from .les_zone import les_zone as les_zone_cls
from .laminar_mut_zero import laminar_mut_zero as laminar_mut_zero_cls
from .les_embedded_spec import les_embedded_spec as les_embedded_spec_cls
from .les_embedded_mom_scheme import les_embedded_mom_scheme as les_embedded_mom_scheme_cls
from .les_embedded_c_wale import les_embedded_c_wale as les_embedded_c_wale_cls
from .les_embedded_c_smag import les_embedded_c_smag as les_embedded_c_smag_cls

class embedded_les(Group):
    fluent_name = ...
    child_names = ...
    les_zone: les_zone_cls = ...
    laminar_mut_zero: laminar_mut_zero_cls = ...
    les_embedded_spec: les_embedded_spec_cls = ...
    les_embedded_mom_scheme: les_embedded_mom_scheme_cls = ...
    les_embedded_c_wale: les_embedded_c_wale_cls = ...
    les_embedded_c_smag: les_embedded_c_smag_cls = ...
