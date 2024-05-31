from functools import cached_property
from typing import Union, Tuple, List
import numpy as np

__docformat__ = "google"

# Valid slices:
#
# Label = Union(str, int)
#
# Slice                                             ->      item
#       shape                                               size
#
# array['A:1'] or array['A', '1'] or array[1, 1]    ->      str or Tuple[Label, Label]
#       ()                                                  1
#
# array[i:j]                                        ->      Slice
#       (n, n_cols)                                         n * n_cols
#
# array[i:j, 1]                                     ->      Tuple[Slice, Label]
#       (n,)                                                n
#
# array[1, i:j]                                     ->      Tuple[Label, Slice]
#       (n,)                                                n
#
# array[i:j, k:l]                                   ->      Tuple[Slice, Slice]
#       (n, o)                                              n * o
#
# array[['A:1', ('A', '1'), (1,1)]]                 ->      List[Union[Label, Tuple[Label, Label]]
#       (3,)                                                3


Label = Union[str, int]
"""@private"""
Single = Union[Label, Tuple[Label, Label]]
"""@private"""
Singles = Union[List[Single], Single]
"""@private"""
Slice = Union[Singles, slice, Tuple[slice, Label], Tuple[Label, slice], Tuple[slice, slice]]
"""@private"""


class Slicer:
    """
    This is a helper class designed to facilitate slicing operations on composed numpy ndarrays.

    To use this class for a specific application, it needs to be extended.

    The class supports one-based integer indexing, meaning array[1,1] refers to the upper left element.
    Negative indexing is not currently supported.

    The item to be sliced can be specified in several ways:
    - A single label or integer (for a row)
    - A label or integer and a slice (for a row and multiple columns)
    - A slice and a label or integer (for multiple rows and a column)
    - Two slices (for a row and column)
    - A list of labels or integers and a slice
    - A slice and a list of labels or integers
    - Two lists of labels or integers (for multiple rows and columns)
    - A string in the format 'A:1' (for a single element)
    - A tuple in the format (1, 1) (for a single element)
    - A list of strings in the format ['A:1', 'B:2'] (for multiple elements)
    - A list of tuples in the format [(1,1), (2,2)] (for multiple elements)

    Examples of valid slicing operations include:
    - Single label or integer: [1], ['A']
    - Label or integer and a slice: [1, 1:], ['A', 1:], [1, '1':]
    - Slice and a label or integer: [1:, 1], ['A':, 1], [1:, '1'], ['A':, '1']
    - Two slices: [1:, 1:], ['A':, 1:], [1:, '1':], ['A':, '1':]
    - List of labels or integers and a slice: [[1, 2], 1:], [['A', 'B'], 1:], [[1, 2], '1':], [['A', 'B'], '1':]
    - Slice and a list of labels or integers: [1:, [1, 2]], ['A':, ['1', '2']], [1, ['1', '2']], ['A', [1, 2]]
    - Two lists of labels or integers: [[1, 2], [2, 3]], [['A', 'B'], [2, 3]], [['A', 'B'], [2, 3]], [['A', 'B'], ['2', '3']]
    - Single string: ['A:1'], ['1:1']
    - Single tuple: [(1, 1)], [('A', '1')]
    - List of strings: [['A:1', 'B:2']], [['1:1', '2:2']]
    - List of tuples: [[(1,1), (2,2)]], [[('A','1'), ('B','2')]]
    """

    def __init__(self, array_obj: np.ndarray, row_labels: tuple | list, col_labels: tuple | list,
                 item: Slice | list):
        """

        Args:
            array_obj (numpy.ndarry): Array to slice.
            row_labels (list): Row labels.
            col_labels (list): Column labels.
            item: Slice(s) passed to __getitem__.
        """

        if not isinstance(array_obj, np.ndarray):
            raise TypeError("array must be a numpy.ndarray.")
        self.array = array_obj
        if not isinstance(row_labels, list) or not all(isinstance(elem, str) for elem in row_labels):
            raise TypeError("row_labels myst be a list of strings.")
        if not isinstance(col_labels, list) or not all(isinstance(elem, str) for elem in col_labels):
            raise TypeError("col_labels myst be a list of strings.")
        self.row_labels = row_labels
        self.n_rows = len(row_labels)
        self.col_labels = col_labels
        self.n_cols = len(col_labels)
        self.item = item

        if array_obj.shape != (self.n_rows, self.n_cols):
            raise ValueError("Length of labels must match shape of array.")

        if isinstance(item, str):
            self.slices = self.parse_single(item)
        elif isinstance(item, list):
            if len(item) == 0:
                raise ValueError("Empty list.")
            self.slices = self.parse_single(item)
        elif isinstance(item, int):
            if not 1 <= item <= self.n_rows:
                raise ValueError("Row index out of range.")
            self.slices = item - 1
        else:
            self.slices = self.parse_tuple(item)

    def copy(self):
        return Slicer(self.array, self.row_labels, self.col_labels, self.item)

    def parse_single(self, single) -> Tuple[int, int] | List[Tuple[int, int]] | List[int]:
        """
        Convert a single index to a tuple of integers.

        Args:
            single: Index to parse, i.e. 'A:1' or ('A','1') or (1, 1).

        """
        if isinstance(single, str) and ':' in single:
            single = tuple(single.split(':'))
        if isinstance(single, tuple) and len(single) == 2:
            return (self.resolve_labels(single[0], self.row_labels),
                    self.resolve_labels(single[1], self.col_labels))
        if isinstance(single, list):
            if all(isinstance(i, (str, tuple)) for i in single):
                return [self.parse_single(i) for i in single]
            else:
                return self.resolve_labels(single, self.row_labels)
        raise TypeError("Invalid slice.")

    def parse_tuple(self, item):
        """
        Handle cases where item is a tuple.

        Args:
            item: Tuples from slice(s) passed to __getitem__.

        Returns:
            Resolved tuples(s).

        """
        if isinstance(item, tuple) and len(item) == 1:
            item = item[0]
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(item[0], list) and isinstance(item[1], list):
                return ([self.resolve_labels(i, self.row_labels) for i in item[0]],
                        [self.resolve_labels(i, self.col_labels) for i in item[1]])
            elif isinstance(item[0], list):
                return ([self.resolve_labels(i, self.row_labels) for i in item[0]],
                        self.resolve_labels(item[1], self.col_labels))
            elif isinstance(item[1], list):
                return (self.resolve_labels(item[0], self.row_labels),
                        [self.resolve_labels(i, self.col_labels) for i in item[1]])
            else:
                return (self.resolve_labels(item[0], self.row_labels),
                        self.resolve_labels(item[1], self.col_labels))
        elif isinstance(item, tuple):
            raise ValueError("We only have two axes.")
        else:
            return self.resolve_labels(item, self.row_labels)

    def resolve_labels(self, item, labels: List[str]) -> Union[int, slice, List[int]]:
        """
        Convert argument passed into __getitem__ to only contain integer indices.

        Args:
            item: Slice(s) passed to __getitem__.
            labels: Row or column labels.

        Raises:
            ValueError: Label not found, or index out of range.
            TypeError:  Invalid type for start, stop, or step.
                        Invalid type for item.
        """
        if isinstance(item, int):
            if not 1 <= item <= len(labels):
                raise ValueError("Index out of range")
            return item - 1  # Use one-based indexing
        if isinstance(item, str):
            try:
                return labels.index(item)
            except ValueError:
                raise ValueError(f"Label not found: {item}")
        if isinstance(item, list):
            return [self.resolve_labels(i, labels) for i in item]
        if isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            if not (step is None or isinstance(step, int)):
                raise TypeError("Step must be None or an integer")
            if isinstance(start, str):
                start = labels.index(start)
            elif isinstance(start, int):
                if not 1 <= start <= len(labels):
                    raise ValueError("Index out of range")
                start -= 1  # Use one-based indexing
            elif start is not None:
                raise TypeError("Start value must be a label or int.")

            if isinstance(stop, str):
                stop = labels.index(stop)
            elif isinstance(stop, int):
                if not 1 <= stop <= len(labels):
                    raise ValueError("Index out of range")
                stop -= 1  # Use one-based indexing
            elif stop is not None:
                raise TypeError("Stop value must be a label or int.")

            if stop is not None:
                stop += 1  # We want values up to and including stop.
            return slice(start, stop, step)
        raise TypeError("Invalid type for a slice.")

    def get(self):
        """
        Get data pointed to by slices.
        """
        if isinstance(self.slices, list):
            return np.array(list(map(self.array.__getitem__, self.slices)))
        return self.array.__getitem__(self.slices)

    def set(self, values):
        """
        Replace data pointed to by slice(s).

        Shape and size of values must match the shape and size of stored slice(s).

        Args:
            values: Data to store.

        Raises:
            ValueError: Shape or size don't match.
        """
        if np.shape(values) != self.shape or np.size(values) != self.size:
            raise ValueError("Shape or size of values doesn't match.")
        if isinstance(self.slices, list):
            for index, value in zip(self.slices, values):
                self.array.__setitem__(index, value)
        else:
            self.array.__setitem__(self.slices, values)

    @cached_property
    def shape(self):
        """
        Gets shape of selected slice(s).
        """
        return np.shape(self.get())

    @cached_property
    def size(self):
        """
        Gets size of selected slice(s).
        """
        return np.size(self.get())

    def __getitem__(self, item: slice | tuple):
        """
        Get a sub-slice of the current slice.
        """
        shape = self.shape
        if isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            if step is not None:
                raise ValueError("Steps are not supported.")
            if start is None and stop is None:
                return self
            if stop is None:
                if (len(shape) == 0 and start != 0) or start >= shape[0]:
                    raise ValueError("Index out of range.")
                return Slicer(self.array, self.row_labels, self.col_labels, self.item[start:])
            if start is None:
                if (len(shape) == 0 and stop != 0) or stop > shape[0]:
                    raise ValueError("Index out of range.")
                return Slicer(self.array, self.row_labels, self.col_labels, self.item[:stop])
            if start >= shape[0] or stop > shape[0]:
                raise ValueError("Index out of range.")
            return Slicer(self.array, self.row_labels, self.col_labels, self.item[start:stop])

    def _subscript_row(self, item: slice | tuple):
        new_slicer = self.copy()

    def __repr__(self):
        return f"Slice: [{self.slices}]"
