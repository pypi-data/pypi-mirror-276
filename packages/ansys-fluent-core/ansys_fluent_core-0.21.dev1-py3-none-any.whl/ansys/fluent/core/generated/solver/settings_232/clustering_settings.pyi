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

from .enable_mesh_interface_clustering import enable_mesh_interface_clustering as enable_mesh_interface_clustering_cls
from .split_angle import split_angle as split_angle_cls
from .clustering_algorithm import clustering_algorithm as clustering_algorithm_cls
from .faces_per_cluster import faces_per_cluster as faces_per_cluster_cls
from .print_thread_clusters import print_thread_clusters as print_thread_clusters_cls

class clustering_settings(Group):
    fluent_name = ...
    child_names = ...
    enable_mesh_interface_clustering: enable_mesh_interface_clustering_cls = ...
    split_angle: split_angle_cls = ...
    clustering_algorithm: clustering_algorithm_cls = ...
    faces_per_cluster: faces_per_cluster_cls = ...
    command_names = ...

    def print_thread_clusters(self, ):
        """
        Prints the following for all boundary threads: thread-id, number of faces, faces per surface cluster, and the number of surface clusters.
        """

