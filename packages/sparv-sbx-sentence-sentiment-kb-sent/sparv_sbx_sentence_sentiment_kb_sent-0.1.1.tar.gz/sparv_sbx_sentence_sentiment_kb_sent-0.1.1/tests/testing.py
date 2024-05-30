from typing import Dict, Generator, Generic, List, Optional, Tuple, TypeVar

from sparv.api.classes import Annotation, BaseAnnotation, Output  # type: ignore [import-untyped]
from sparv.core import log_handler  # type: ignore [import-untyped] # noqa: F401


class MockAnnotation(Annotation):
    def __init__(
        self,
        name: str = "",
        source_file: Optional[str] = None,
        values: Optional[List[str]] = None,
        children: Optional[Dict[str, List[List[int]]]] = None,
    ) -> None:
        super().__init__(name)
        self._values = values or []
        self._children = children or {}

    def read(self, allow_newlines: bool = False) -> Generator[str, None, None]:
        """Yield each line from the annotation."""
        if not self._values:
            return
        yield from self._values

    def get_children(
        self,
        child: BaseAnnotation,
        *,
        orphan_alert: bool = False,
        preserve_parent_annotation_order: bool = False,
    ) -> Tuple[List, List]:
        """Return two lists.

        The first one is a list with n (= total number of parents) elements where every element is a list
        of indices in the child annotation.
        The second one is a list of orphans, i.e. containing indices in the child annotation that have no parent.
        Both parents and children are sorted according to their position in the source file, unless
        preserve_parent_annotation_order is set to True, in which case the parents keep the order from the parent
        annotation.
        """
        return self._children[child.name], []

    def create_empty_attribute(self) -> List:
        return [None] * max(len(val) for val in self._children.values())


T = TypeVar("T")


class MemoryOutput(Output, Generic[T]):
    def __init__(self) -> None:
        self.values: List[T] = []

    def write(
        self,
        values: List[T],
        *,
        append: bool = False,
        allow_newlines: bool = False,
        source_file: Optional[str] = None,
    ) -> None:
        """Write an annotation to file. Existing annotation will be overwritten.

        'values' should be a list of values.
        """
        if append:
            self.values.extend(values)
        else:
            self.values = values
