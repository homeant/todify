from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def batch_list(iterable: Iterable[T], size: int) -> Generator[Iterable[T], None, None]:
    iterable = list(iterable)
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]
