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

from .number_of_iterations_1 import number_of_iterations as number_of_iterations_cls

class iterate(Command):
    fluent_name = ...
    argument_names = ...
    number_of_iterations: number_of_iterations_cls = ...
