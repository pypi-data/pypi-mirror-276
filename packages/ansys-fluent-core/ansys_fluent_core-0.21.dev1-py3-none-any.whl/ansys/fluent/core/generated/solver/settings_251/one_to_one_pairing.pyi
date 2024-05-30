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

from .one_to_one_interface import one_to_one_interface as one_to_one_interface_cls
from .proceed import proceed as proceed_cls
from .delete_empty import delete_empty as delete_empty_cls

class one_to_one_pairing(Command):
    fluent_name = ...
    argument_names = ...
    one_to_one_interface: one_to_one_interface_cls = ...
    proceed: proceed_cls = ...
    delete_empty: delete_empty_cls = ...
