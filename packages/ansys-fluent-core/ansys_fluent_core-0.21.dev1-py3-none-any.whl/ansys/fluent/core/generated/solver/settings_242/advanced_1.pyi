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

from .contact_resis import contact_resis as contact_resis_cls
from .coolant_channel import coolant_channel as coolant_channel_cls
from .stack_management import stack_management as stack_management_cls

class advanced(Group):
    fluent_name = ...
    child_names = ...
    contact_resis: contact_resis_cls = ...
    coolant_channel: coolant_channel_cls = ...
    stack_management: stack_management_cls = ...
