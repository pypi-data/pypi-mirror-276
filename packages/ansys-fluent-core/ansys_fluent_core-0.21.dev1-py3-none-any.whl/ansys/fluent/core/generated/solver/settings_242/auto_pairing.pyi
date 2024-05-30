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

from .pair_all import pair_all as pair_all_cls
from .one_to_one_pairs import one_to_one_pairs as one_to_one_pairs_cls
from .interface_zones import interface_zones as interface_zones_cls
from .create_2 import create as create_cls
from .name_2 import name as name_cls
from .apply_mapped import apply_mapped as apply_mapped_cls
from .static_interface import static_interface as static_interface_cls

class auto_pairing(Command):
    fluent_name = ...
    argument_names = ...
    pair_all: pair_all_cls = ...
    one_to_one_pairs: one_to_one_pairs_cls = ...
    interface_zones: interface_zones_cls = ...
    create: create_cls = ...
    name: name_cls = ...
    apply_mapped: apply_mapped_cls = ...
    static_interface: static_interface_cls = ...
