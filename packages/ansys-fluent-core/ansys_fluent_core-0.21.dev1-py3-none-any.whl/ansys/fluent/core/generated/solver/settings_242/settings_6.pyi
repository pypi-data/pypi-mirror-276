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

from .smooth_sensitivities import smooth_sensitivities as smooth_sensitivities_cls
from .activation_function import activation_function as activation_function_cls
from .neural_network_topology import neural_network_topology as neural_network_topology_cls
from .input_features import input_features as input_features_cls

class settings(Group):
    fluent_name = ...
    child_names = ...
    smooth_sensitivities: smooth_sensitivities_cls = ...
    activation_function: activation_function_cls = ...
    neural_network_topology: neural_network_topology_cls = ...
    input_features: input_features_cls = ...
