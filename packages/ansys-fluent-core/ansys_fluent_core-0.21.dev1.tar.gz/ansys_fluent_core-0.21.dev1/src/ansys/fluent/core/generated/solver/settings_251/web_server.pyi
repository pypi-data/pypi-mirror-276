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
from .print_server_info import print_server_info as print_server_info_cls
from .get_server_info import get_server_info as get_server_info_cls

class web_server(Group):
    fluent_name = ...
    command_names = ...

    def start(self, session_name: str, port: int, port_span: int, job_service_url: str):
        """
        Start the web server.
        
        Parameters
        ----------
            session_name : str
                Name for the web server.
            port : int
                Listening port for the web server.
            port_span : int
                Number of ports to try starting from given 'port' for the web server.
            job_service_url : str
                Job service URL to register Fluent.
        
        """

    def stop(self, ):
        """
        Stop the web server.
        """

    def print_server_info(self, ):
        """
        Print the web server information.
        """

    query_names = ...

    def get_server_info(self, ):
        """
        Get the web server information.
        """

