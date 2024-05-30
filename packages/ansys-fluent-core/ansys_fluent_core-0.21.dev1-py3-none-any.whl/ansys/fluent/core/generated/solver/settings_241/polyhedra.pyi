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

from .options import options as options_cls
from .convert_domain import convert_domain as convert_domain_cls
from .convert_hanging_nodes import convert_hanging_nodes as convert_hanging_nodes_cls
from .convert_hanging_node_zones import convert_hanging_node_zones as convert_hanging_node_zones_cls
from .convert_skewed_cells_1 import convert_skewed_cells as convert_skewed_cells_cls

class polyhedra(Group):
    fluent_name = ...
    child_names = ...
    options: options_cls = ...
    command_names = ...

    def convert_domain(self, ):
        """
        Convert entire domain to polyhedra cells.
        """

    def convert_hanging_nodes(self, ):
        """
        Convert cells with hanging nodes and faces to polyhedra.
        """

    def convert_hanging_node_zones(self, ):
        """
        Convert selected cell zones with hanging nodes and faces to polyhedra. 
        The selected cell zones cannot be connected to other zones.
        """

    def convert_skewed_cells(self, cell_thread_list: List[str], max_cell_skewness: Union[float, str], convert_skewed_cells: bool):
        """
        'convert_skewed_cells' command.
        
        Parameters
        ----------
            cell_thread_list : typing.List[str]
                Set zones where cells should be converted.
            max_cell_skewness : real
                Set target maximum cell skewness.
            convert_skewed_cells : bool
                'convert_skewed_cells' child.
        
        """

