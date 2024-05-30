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

from .all_1 import all as all_cls
from .one_to_one_pairing_1 import one_to_one_pairing as one_to_one_pairing_cls
from .new_interface_zones import new_interface_zones as new_interface_zones_cls
from .si_create import si_create as si_create_cls
from .si_name import si_name as si_name_cls
from .apply_mapped import apply_mapped as apply_mapped_cls
from .static_interface import static_interface as static_interface_cls

class auto_pairing(Command):
    fluent_name = ...
    argument_names = ...
    all: all_cls = ...
    one_to_one_pairing: one_to_one_pairing_cls = ...
    new_interface_zones: new_interface_zones_cls = ...
    si_create: si_create_cls = ...
    si_name: si_name_cls = ...
    apply_mapped: apply_mapped_cls = ...
    static_interface: static_interface_cls = ...
