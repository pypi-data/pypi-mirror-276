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

from .enabled_all_1 import enabled_all as enabled_all_cls
from .disabled_all_1 import disabled_all as disabled_all_cls
from .interface_name_3 import interface_name as interface_name_cls
from .nps_min_po_loss import nps_min_po_loss as nps_min_po_loss_cls

class nps_minimize_po_loss(Command):
    fluent_name = ...
    argument_names = ...
    enabled_all: enabled_all_cls = ...
    disabled_all: disabled_all_cls = ...
    interface_name: interface_name_cls = ...
    nps_min_po_loss: nps_min_po_loss_cls = ...
