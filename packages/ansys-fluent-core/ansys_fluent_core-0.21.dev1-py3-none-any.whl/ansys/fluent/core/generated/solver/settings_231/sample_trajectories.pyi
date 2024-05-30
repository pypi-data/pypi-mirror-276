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

from .user_defined_functions_1 import user_defined_functions as user_defined_functions_cls
from .sort_sample_files import sort_sample_files as sort_sample_files_cls
from .sample_1 import sample as sample_cls

class sample_trajectories(Group):
    fluent_name = ...
    child_names = ...
    user_defined_functions: user_defined_functions_cls = ...
    sort_sample_files: sort_sample_files_cls = ...
    command_names = ...

    def sample(self, injections: List[str], boundaries: List[str], lines: List[str], planes: List[str], op_udf: str, append_sample: bool, accumulate_rates: bool):
        """
        'sample' command.
        
        Parameters
        ----------
            injections : typing.List[str]
                'injections' child.
            boundaries : typing.List[str]
                'boundaries' child.
            lines : typing.List[str]
                'lines' child.
            planes : typing.List[str]
                'planes' child.
            op_udf : str
                'op_udf' child.
            append_sample : bool
                'append_sample' child.
            accumulate_rates : bool
                'accumulate_rates' child.
        
        """

