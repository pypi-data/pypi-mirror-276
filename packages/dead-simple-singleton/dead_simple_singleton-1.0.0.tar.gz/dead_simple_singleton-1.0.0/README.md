# Singleton

Create Singleton classes simply by decorating them.


```python
from singleton import Singleton


@Singleton
class DummyClass:
    def __init__(self, dummy_var):
        self.dummy_var = dummy_var

t1 = DummyClass(5)
t2 = DummyClass(3)

assert t1 is t2 # True
assert t1.dummy_var == t2.dummy_var # True
```