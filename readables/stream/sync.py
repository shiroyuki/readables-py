from typing import Iterable, Any, Generic, TypeVar, Callable, List, Iterator, Generator

T = TypeVar('T')
S = TypeVar('S')
R = TypeVar('R')


class Filter(Generic[T]):
    def __init__(self, fn: Callable[[T], bool]):
        self._fn = fn

    def __call__(self, t: T):
        return self._fn(t)


class Map(Generic[S, R]):
    def __init__(self, fn: Callable[[S], R]):
        self._fn = fn

    def __call__(self, s: S) -> R:
        return self._fn(s)


class FlatMap(Generic[S, R]):
    """
    Flat map an iterable object

    While code is identical to Map, how it is used is different.
    """
    def __init__(self, fn: Callable[[S], R]):
        self._fn = fn

    def __call__(self, s: S) -> Generator[R, Any, None]:
        yield self._fn(s)


class Stream(Generic[T, S]):
    def __init__(self, source: Iterator[T]):
        self._source = source
        self._chain: List[Filter | Map | FlatMap] = []

    def observe(self):
        for item in self._source:
            included = True
            iterated_value = item

            for act in self._chain:
                if isinstance(act, Filter) and not act(iterated_value):
                    included = False
                    break

                if isinstance(act, Map):
                    iterated_value = act(iterated_value)

                if isinstance(act, FlatMap):
                    raise NotImplementedError('To be implemented')

            if not included:
                continue

            yield iterated_value
