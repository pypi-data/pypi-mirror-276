import enum
from typing import Annotated

from numpy.typing import ArrayLike


class ImageChannel(enum.Enum):
    one = 1

    three = 3

    four = 4

    unknown = 5

class ImagePrecision(enum.Enum):
    uint8 = 0

    int8 = 1

    uint32 = 2

    int32 = 3

    float32 = 4

    float64 = 5

    float16 = 6

    unknown = 7

class ImageStorage:
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None: ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    @property
    def stride(self) -> int: ...

    @property
    def data(self) -> Annotated[ArrayLike, dict(dtype='uint8', order='C', device='cpu')]: ...
