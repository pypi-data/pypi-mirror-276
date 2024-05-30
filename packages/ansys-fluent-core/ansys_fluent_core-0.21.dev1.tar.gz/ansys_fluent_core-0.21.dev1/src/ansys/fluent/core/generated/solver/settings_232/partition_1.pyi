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

from .auto_1 import auto as auto_cls
from .set_3 import set as set_cls
from .combine_partition import combine_partition as combine_partition_cls
from .merge_clusters import merge_clusters as merge_clusters_cls
from .method_5 import method as method_cls
from .print_partitions import print_partitions as print_partitions_cls
from .print_active_partitions import print_active_partitions as print_active_partitions_cls
from .print_stored_partitions import print_stored_partitions as print_stored_partitions_cls
from .reorder_partitions import reorder_partitions as reorder_partitions_cls
from .reorder_partitions_to_architecture import reorder_partitions_to_architecture as reorder_partitions_to_architecture_cls
from .smooth_partition import smooth_partition as smooth_partition_cls
from .use_stored_partitions import use_stored_partitions as use_stored_partitions_cls

class partition(Group):
    fluent_name = ...
    child_names = ...
    auto: auto_cls = ...
    set: set_cls = ...
    command_names = ...

    def combine_partition(self, number_of_partitions: int):
        """
        Merge every N partitions.
        
        Parameters
        ----------
            number_of_partitions : int
                'number_of_partitions' child.
        
        """

    def merge_clusters(self, merge_iterations: int):
        """
        Merge partition clusters.
        
        Parameters
        ----------
            merge_iterations : int
                'merge_iterations' child.
        
        """

    def method(self, partition_method: str, count: int):
        """
        Partition the domain.
        
        Parameters
        ----------
            partition_method : str
                'partition_method' child.
            count : int
                'count' child.
        
        """

    def print_partitions(self, ):
        """
        Print partition information.
        """

    def print_active_partitions(self, ):
        """
        Print active partition information.
        """

    def print_stored_partitions(self, ):
        """
        Print stored partition information.
        """

    def reorder_partitions(self, ):
        """
        Reorder partitions.
        """

    def reorder_partitions_to_architecture(self, ):
        """
        Reorder partitions to architecture.
        """

    def smooth_partition(self, smoothing_iteration: int):
        """
        Smooth partition interface.
        
        Parameters
        ----------
            smoothing_iteration : int
                Set maximum number of smoothing iterations.
        
        """

    def use_stored_partitions(self, ):
        """
        Use stored partitioning.
        """

