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

from .interface_name_4 import interface_name as interface_name_cls
from .bands import bands as bands_cls

class on_specified_interface(Command):
    fluent_name = ...
    argument_names = ...
    interface_name: interface_name_cls = ...
    bands: bands_cls = ...
