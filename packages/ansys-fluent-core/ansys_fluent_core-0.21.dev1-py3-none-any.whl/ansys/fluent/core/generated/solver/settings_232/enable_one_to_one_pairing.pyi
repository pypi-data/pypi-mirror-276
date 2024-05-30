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

from .o2o_flag import o2o_flag as o2o_flag_cls
from .toggle import toggle as toggle_cls
from .delete_empty import delete_empty as delete_empty_cls

class enable_one_to_one_pairing(Command):
    fluent_name = ...
    argument_names = ...
    o2o_flag: o2o_flag_cls = ...
    toggle: toggle_cls = ...
    delete_empty: delete_empty_cls = ...
