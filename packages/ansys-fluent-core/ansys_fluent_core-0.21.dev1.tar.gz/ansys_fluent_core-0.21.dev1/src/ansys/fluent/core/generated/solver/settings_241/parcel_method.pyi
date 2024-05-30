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

from .option import option as option_cls
from .const_number_in_parcel import const_number_in_parcel as const_number_in_parcel_cls
from .const_parcel_mass import const_parcel_mass as const_parcel_mass_cls
from .const_parcel_diameter import const_parcel_diameter as const_parcel_diameter_cls

class parcel_method(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    const_number_in_parcel: const_number_in_parcel_cls = ...
    const_parcel_mass: const_parcel_mass_cls = ...
    const_parcel_diameter: const_parcel_diameter_cls = ...
