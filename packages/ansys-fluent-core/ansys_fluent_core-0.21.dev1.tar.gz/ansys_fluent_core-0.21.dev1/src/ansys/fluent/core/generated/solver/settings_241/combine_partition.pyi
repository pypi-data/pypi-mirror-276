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

from .number_of_partitions import number_of_partitions as number_of_partitions_cls

class combine_partition(Command):
    fluent_name = ...
    argument_names = ...
    number_of_partitions: number_of_partitions_cls = ...
