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

from .scheme_proc import scheme_proc as scheme_proc_cls
from .udf_side import udf_side as udf_side_cls
from .expression_2 import expression as expression_cls
from .list_4 import list as list_cls

class input_parameters(Group):
    fluent_name = ...
    child_names = ...
    scheme_proc: scheme_proc_cls = ...
    udf_side: udf_side_cls = ...
    expression: expression_cls = ...
    command_names = ...

    def list(self, ):
        """
        List all input parameters.
        """

