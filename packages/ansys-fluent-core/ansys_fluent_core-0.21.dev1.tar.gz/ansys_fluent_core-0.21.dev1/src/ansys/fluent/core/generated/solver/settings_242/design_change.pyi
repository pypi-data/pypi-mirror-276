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

from .parameters_4 import parameters as parameters_cls
from .results_1 import results as results_cls
from .export_2 import export as export_cls
from .preview_1 import preview as preview_cls
from .history import history as history_cls
from .check_1 import check as check_cls
from .calculate_design_change import calculate_design_change as calculate_design_change_cls
from .print_expected_changes import print_expected_changes as print_expected_changes_cls
from .modify import modify as modify_cls
from .revert import revert as revert_cls
from .remesh import remesh as remesh_cls

class design_change(Group):
    fluent_name = ...
    child_names = ...
    parameters: parameters_cls = ...
    results: results_cls = ...
    export: export_cls = ...
    preview: preview_cls = ...
    history: history_cls = ...
    command_names = ...

    def check(self, ):
        """
        Design tool check.
        """

    def calculate_design_change(self, ):
        """
        Calculates design change.
        """

    def print_expected_changes(self, ):
        """
        Print expected changes.
        """

    def modify(self, ):
        """
        Apply the computed optimal displacement to the mesh.
        """

    def revert(self, ):
        """
        Revert to the unmodified mesh.
        """

    def remesh(self, ):
        """
        Remesh.
        """

