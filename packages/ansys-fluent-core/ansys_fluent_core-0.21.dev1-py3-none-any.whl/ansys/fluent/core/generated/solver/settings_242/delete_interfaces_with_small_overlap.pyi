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

from .delete_3 import delete as delete_cls
from .overlapping_percentage_threshold import overlapping_percentage_threshold as overlapping_percentage_threshold_cls

class delete_interfaces_with_small_overlap(Command):
    fluent_name = ...
    argument_names = ...
    delete: delete_cls = ...
    overlapping_percentage_threshold: overlapping_percentage_threshold_cls = ...
