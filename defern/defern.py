import inspect
import uuid
import warnings
from types import FrameType
from typing import Any, Tuple, Callable
from typing import AnyStr, Optional
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
    """
    defern(func, *args, frame: FrameType = None, **kwargs)

    Defer the callback to the end of the frame.

    :param func: The callback function.
    :param args: The arguments to pass to the callback function.
    :param frame: The frame to defer the callback to.
    :param kwargs: The keyword arguments to pass to the callback function.
    """
    warnings.warn("defern(func, *args, frame, **kwargs) is deprecated, use defer(func, frame)(*args, **kwargs) instead",
                  DeprecationWarning)
    deferer = Defern(func, args, kwargs)

    new_variable_name = 'defern-{}'.format(uuid.uuid4())
    frame = _outer_frame(frame)
    frame.f_locals[new_variable_name] = deferer

    return new_variable_name, deferer


def deferner(func: Callable) -> Callable:
    """
    deferner(func)

    Wrap the callback function to defer the callback to the end of the frame.

    :param func: The callback function.
    :return: The callback function.
    """
    warnings.warn(
        'deferner(func)(*args, frame, **kwargs) is deprecated, use defer(func, frame)(*args, **kwargs) instead',
        DeprecationWarning)

    @wraps(func)
    def wrapper(*args, frame: FrameType = None, **kwargs) -> Tuple[AnyStr, Defern]:
        deferer = Defern(func, args, kwargs)

        new_variable_name = 'defern-{}'.format(uuid.uuid4())
        frame = _outer_frame(frame)
        frame.f_locals[new_variable_name] = deferer
        return new_variable_name, deferer

    return wrapper


def defern_this(func: Callable) -> Callable:
    """
    defern_this(func)

    Wrap the callback function to defer the callback to the end of the frame.

    :param func: The callback function.
    :return: The callback function.
    """
    warnings.warn('defern_this(func) is deprecated, use defer(func)() instead', DeprecationWarning)
    deferer = Defern(func, tuple(), dict())

    new_variable_name = 'defern-{}'.format(uuid.uuid4())
    frame = _outer_frame()
    frame.f_locals[new_variable_name] = deferer

    return func


class DeferStack:
    def __init__(self, frame: FrameType):
        self.frame = frame

    @property
    def back(self) -> 'DeferStack':
        return DeferStack(self.frame.f_back)


def here() -> DeferStack:
    return DeferStack(inspect.currentframe().f_back)


class DefernCaller:
    namespace = 'DefernCaller'

    def __init__(self):
        self.callback = []

    def set(self, func: Callable, args: Tuple[Any], kwargs: [str, Any], frame: DeferStack):
        caller_name = frame.frame.f_code.co_name
        caller_locals = frame.frame.f_locals
        defern_id = 'Defern_' + uuid.uuid3(uuid.NAMESPACE_DNS, caller_name).hex.replace('-', '_')
        if defern_id in caller_locals:
            defern_caller = caller_locals[defern_id]
            if defern_caller is not self:
                caller_locals[defern_id].set(func, args, kwargs, frame)
                return
        else:
            caller_locals[defern_id] = self
        self.callback.append((func, args, kwargs))

    def __del__(self):
        while self.callback:
            func, args, kwargs = self.callback.pop()
            func(*args, **kwargs)


def defer(callback, frame: Optional[DeferStack] = None):
    """
    defer(callback, frame: Optional[DeferStack] = None)

    Defer the callback to the end of the frame.

    :param callback: The callback function.
    :param frame: The frame to defer the callback to.
    :return: The callback function.

    """

    @wraps(callback)
    def func(*args, **kwargs):
        nonlocal frame
        if frame is None:
            frame = here().back
        DefernCaller().set(callback, args, kwargs, frame)

    return func
