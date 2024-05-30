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

from .confirm_overwrite import confirm_overwrite as confirm_overwrite_cls
from .exit_on_error import exit_on_error as exit_on_error_cls
from .hide_answer import hide_answer as hide_answer_cls
from .redisplay_question import redisplay_question as redisplay_question_cls

class batch_options(Group):
    fluent_name = ...
    child_names = ...
    confirm_overwrite: confirm_overwrite_cls = ...
    exit_on_error: exit_on_error_cls = ...
    hide_answer: hide_answer_cls = ...
    redisplay_question: redisplay_question_cls = ...
