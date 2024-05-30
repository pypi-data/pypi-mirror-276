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

from .max_epochs import max_epochs as max_epochs_cls
from .mini_batch_size import mini_batch_size as mini_batch_size_cls
from .learning_rate import learning_rate as learning_rate_cls
from .initialize_neural_network import initialize_neural_network as initialize_neural_network_cls
from .manage_data_1 import manage_data as manage_data_cls
from .train import train as train_cls
from .apply_trained_model import apply_trained_model as apply_trained_model_cls
from .default_7 import default as default_cls

class offline_training(Group):
    fluent_name = ...
    child_names = ...
    max_epochs: max_epochs_cls = ...
    mini_batch_size: mini_batch_size_cls = ...
    learning_rate: learning_rate_cls = ...
    initialize_neural_network: initialize_neural_network_cls = ...
    manage_data: manage_data_cls = ...
    command_names = ...

    def train(self, ):
        """
        Train the design variables using neural network.
        """

    def apply_trained_model(self, update_design_variables: bool):
        """
        Adopt the trained neural network for the turbulence modeling.
        
        Parameters
        ----------
            update_design_variables : bool
                Update design variables using the neural network model after applying the trained model.
        
        """

    def default(self, ):
        """
        Use the default training parameters.
        """

