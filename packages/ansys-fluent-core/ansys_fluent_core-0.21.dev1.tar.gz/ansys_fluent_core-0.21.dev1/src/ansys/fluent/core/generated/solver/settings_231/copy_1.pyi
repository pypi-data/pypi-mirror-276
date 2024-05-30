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

from .copy_from import copy_from as copy_from_cls
from .copy_to import copy_to as copy_to_cls

class copy(Command):
    fluent_name = ...
    argument_names = ...
    copy_from: copy_from_cls = ...
    copy_to: copy_to_cls = ...
