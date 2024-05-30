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

from .file import file as file_cls
from .mesh import mesh as mesh_cls
from .server import server as server_cls
from .setup import setup as setup_cls
from .solution import solution as solution_cls
from .results import results as results_cls
from .parametric_studies import parametric_studies as parametric_studies_cls
from .current_parametric_study import current_parametric_study as current_parametric_study_cls
from .parameters_2 import parameters as parameters_cls
from .parallel_1 import parallel as parallel_cls
from .exit import exit as exit_cls

class root(Group):
    fluent_name = ...
    child_names = ...
    file: file_cls = ...
    mesh: mesh_cls = ...
    server: server_cls = ...
    setup: setup_cls = ...
    solution: solution_cls = ...
    results: results_cls = ...
    parametric_studies: parametric_studies_cls = ...
    current_parametric_study: current_parametric_study_cls = ...
    parameters: parameters_cls = ...
    parallel: parallel_cls = ...
    command_names = ...

    def exit(self, ):
        """
        Exit program.
        """

