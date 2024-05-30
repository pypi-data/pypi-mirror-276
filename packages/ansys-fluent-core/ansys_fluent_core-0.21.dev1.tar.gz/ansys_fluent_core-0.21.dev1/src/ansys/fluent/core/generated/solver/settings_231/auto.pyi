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

from .across_zones import across_zones as across_zones_cls
from .method_1 import method as method_cls
from .load_vector import load_vector as load_vector_cls
from .pre_test import pre_test as pre_test_cls
from .use_case_file_method import use_case_file_method as use_case_file_method_cls

class auto(Group):
    fluent_name = ...
    child_names = ...
    across_zones: across_zones_cls = ...
    method: method_cls = ...
    load_vector: load_vector_cls = ...
    pre_test: pre_test_cls = ...
    command_names = ...

    def use_case_file_method(self, file_partition_method: bool):
        """
        Enable the use-case-file method for auto partitioning.
        
        Parameters
        ----------
            file_partition_method : bool
                'file_partition_method' child.
        
        """

