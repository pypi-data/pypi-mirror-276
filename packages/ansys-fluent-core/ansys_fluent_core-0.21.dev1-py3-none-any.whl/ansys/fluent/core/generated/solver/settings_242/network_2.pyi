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

from .shell_script_path import shell_script_path as shell_script_path_cls
from .kill_all_nodes import kill_all_nodes as kill_all_nodes_cls
from .kill_node import kill_node as kill_node_cls
from .spawn_node import spawn_node as spawn_node_cls
from .load_hosts import load_hosts as load_hosts_cls
from .save_hosts import save_hosts as save_hosts_cls

class network(Group):
    fluent_name = ...
    child_names = ...
    shell_script_path: shell_script_path_cls = ...
    command_names = ...

    def kill_all_nodes(self, delete_all_compute_nodes: bool):
        """
        Delete all compute nodes from virtual machine.
        
        Parameters
        ----------
            delete_all_compute_nodes : bool
                'delete_all_compute_nodes' child.
        
        """

    def kill_node(self, compute_node: int, invalidate_case: bool):
        """
        'kill_node' command.
        
        Parameters
        ----------
            compute_node : int
                'compute_node' child.
            invalidate_case : bool
                'invalidate_case' child.
        
        """

    def spawn_node(self, hostname: str, username: str):
        """
        Spawn a compute node process on a specified machine.
        
        Parameters
        ----------
            hostname : str
                'hostname' child.
            username : str
                'username' child.
        
        """

    def load_hosts(self, host_file: str):
        """
        Read a hosts file.
        
        Parameters
        ----------
            host_file : str
                'host_file' child.
        
        """

    def save_hosts(self, host_file_1: str):
        """
        Write a hosts file.
        
        Parameters
        ----------
            host_file_1 : str
                'host_file' child.
        
        """

