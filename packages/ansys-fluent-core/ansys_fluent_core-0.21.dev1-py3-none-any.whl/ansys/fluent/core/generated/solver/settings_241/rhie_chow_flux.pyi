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

from .low_order_rhie_chow import low_order_rhie_chow as low_order_rhie_chow_cls

class rhie_chow_flux(Group):
    fluent_name = ...
    child_names = ...
    low_order_rhie_chow: low_order_rhie_chow_cls = ...
