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

from .start import start as start_cls
from .stop import stop as stop_cls

class web_server(Group):
    fluent_name = ...
    command_names = ...

    def start(self, address: str, port: int):
        """
        'start' command.
        
        Parameters
        ----------
            address : str
                'address' child.
            port : int
                'port' child.
        
        """

    def stop(self, ):
        """
        'stop' command.
        """

