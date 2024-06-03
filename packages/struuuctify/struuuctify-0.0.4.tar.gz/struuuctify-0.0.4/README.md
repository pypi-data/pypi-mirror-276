# struuuctify

# Installation

`pip install struuuctify`

## Rust like struct for python

Define a new struct:

```python
from structify import struct, impl


@struct
class Point:
    x: float
    y: float
```


And add method implementation on that struct

```python
@impl
def add(
    self: Point,
) -> float:
    return self.x + self.y
```

You can now instanciate the struct and call the method as if it was defined in the class:

```python
p = Point(1, 2)

p.add()
>> 3
```


# Limitation

This project is more of a gimmick-y pattern and experimentation around rust-like struct in Python !

- Mypy and type checkers will not be aware of the method declared on your struct as they are added at runtime.
- If you define methods on the same struct from different locations, you could end up having clash  
