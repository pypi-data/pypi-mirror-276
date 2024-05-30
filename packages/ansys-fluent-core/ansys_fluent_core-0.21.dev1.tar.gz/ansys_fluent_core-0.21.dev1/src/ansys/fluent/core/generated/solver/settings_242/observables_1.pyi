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

from .selection_2 import selection as selection_cls
from .evaluation import evaluation as evaluation_cls
from .default_6 import default as default_cls

class observables(Group):
    fluent_name = ...
    child_names = ...
    selection: selection_cls = ...
    evaluation: evaluation_cls = ...
    command_names = ...

    def default(self, ):
        """
        If no observables are selected, include a default
                      observable. Does nothing if there is already a selection.
        """

