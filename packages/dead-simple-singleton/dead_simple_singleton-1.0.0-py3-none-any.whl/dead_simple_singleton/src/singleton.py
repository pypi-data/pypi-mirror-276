"""
Create Singleton classes simply by decorating them.

@Singleton
class DummyClass:
    pass

t1 = DummyClass()
t2 = DummyClass()

assert t1 is t2 # True
"""

from collections.abc import Callable
import functools as ft


def Singleton[A](cls: type[A]) -> Callable[..., A]:
    singleton_value = None

    @ft.wraps(cls)
    def new_cls_constructor(*args, **kwargs) -> A:
        nonlocal singleton_value

        if singleton_value is None:
            singleton_value = cls(*args, **kwargs)

        return singleton_value

    return new_cls_constructor
