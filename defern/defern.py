import re
import itertools
from warnings import warn
from typing import Callable, Tuple, AnyStr, Optional
from types import FrameType
import inspect
import uuid
from functools import wraps


def _outer_frame(frame: FrameType = None) -> FrameType:
    return frame or inspect.currentframe().f_back.f_back


class Defern:
    def __init__(self, func: Callable, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.func(*self.args, **self.kwargs)


def defern(func: Callable, *args, frame: FrameType = None, **kwargs) -> Tuple[AnyStr, Defern]:
    deferer = Defern(func, args, kwargs)

    new_variable_name = 'defern-{}'.format(uuid.uuid4())
    frame = _outer_frame(frame)
    frame.f_locals[new_variable_name] = deferer

    return new_variable_name, deferer


def deferner(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, frame: FrameType = None, **kwargs) -> Tuple[AnyStr, Defern]:
        deferer = Defern(func, args, kwargs)

        new_variable_name = 'defern-{}'.format(uuid.uuid4())
        frame = _outer_frame(frame)
        frame.f_locals[new_variable_name] = deferer
        return new_variable_name, deferer

    return wrapper


def defern_this(func: Callable) -> Callable:
    deferer = Defern(func, tuple(), dict())

    new_variable_name = 'defern{}'.format(uuid.uuid4())
    frame = _outer_frame()
    frame.f_locals[new_variable_name] = deferer

    return func


def here() -> FrameType:
    return inspect.currentframe().f_back


def defer_multiple_function(frame):
    defern(lambda: print("it's middle 7th"), frame=frame)
    defern(lambda: print("it's middle 8th"), frame=frame)
