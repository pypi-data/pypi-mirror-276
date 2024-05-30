# pylint: disable=line-too-long
"""
Histogram and Group Library

This library provides two main classes: Histogram and Group. The Histogram class is a generic data structure for
storing and sampling data points, while the Group class represents a collection of Histogram instances or other Group
instances.

The Histogram class supports various operations, such as observing new data points, sampling, computing percentiles,
combining histograms, and applying transformations like shifting, scaling, and capping values. It is designed to be
memory-efficient by limiting the maximum number of data points stored.

The Group class allows you to combine multiple Histogram instances or other Group instances into a single entity.
You can sample values from the group and obtain an explanation of the sampled value, breaking it down into
contributions from each element.

Classes:
    Histogram: A generic data structure for storing and sampling data points.
    Group: A collection of Histogram instances or other Group instances.

Functions:
    Max: Adjust the histogram such that no data point exceeds the given value.
    MaxAtPercentile: Adjust the histogram such that no data point exceeds the value at the given percentile.
    Min: Adjust the histogram such that no data point is less than the given value.
    MinAtPercentile: Adjust the histogram such that no data point is less than the value at the given percentile.
    Shift: Shift all data points in the histogram by the given value.
    Scale: Scale all data points in the histogram by the given scalar.

Example:
    >>> import heare.histograms as hgl
    >>> hist = hgl.Histogram[int](max_size=1000)
    >>> hist.observe([1, 2, 3, 4, 5])
    >>> sample = hist.sample()
    >>> group = hgl.Group[int]([("hist", hist)])
    >>> group_sample = group.sample()
    >>> explanation = group.explain_sample()
"""

import math
from typing import TypeVar, Generic, List, Union, Callable, Self, Dict, Tuple, Any
import random

T = TypeVar('T')


class Histogram(Generic[T]):
    """
    A simple Histogram class to store and sample data points. Based on
    [Uniform Distributions](https://en.wikipedia.org/wiki/Continuous_uniform_distribution).

    Attributes:
        _data (List[T]): A list to store the observed data points.
        _max_size (int): The maximum number of data points to keep in the histogram.
        _dirty (bool): Indicates whether the contents of data are currently sorted, or need to be.
    """

    def __init__(self, max_size: int = 1000, data: List[T] = None):
        self._data: List[T] = data or []
        self._data.sort()
        self._max_size: int = max_size
        self._dirty = False

    def __add__(self, other: Union[T, List[T], Self]) -> Self:
        """
        Overloading the + operator to combine two histograms or observe new data.

        Args:
            other (Union[T, List[T], Self]): A data point, list of
                data points, or another Histogram.

        Returns:
            Self: A new Histogram instance with the combined data.
        """
        if isinstance(other, Histogram):
            return self.clone().combine(other)

        return self.clone().observe(other)

    def __iadd__(self, other: Union[T, List[T], Self]) -> Self:
        """
        Overloading the += operator to combine two histograms or observe new data.

        Args:
            other (Union[T, List[T], Self]): A data point, list of
                data points, or another Histogram.

        Returns:
            Self: The current Histogram instance with the combined data.
        """
        if isinstance(other, Histogram):
            self.combine(other)
        else:
            # NOTE: better typing here
            self.observe(other)
        return self

    def combine(self, other: Self) -> Self:
        """
        Combine two histograms by merging their data points.

        Args:
            other (Self): Another Histogram instance.

        Returns:
            Self: A new Histogram instance with the combined data.
        """
        # pylint: disable=protected-access
        all_data = self._data + other._data
        size = max(self._max_size, other._max_size)
        if len(all_data) > self._max_size:
            all_data = random.sample(all_data, size)
        result = Histogram(max_size=size, data=all_data)
        result.sample_n = self.sample_n
        return result

    def observe(self, point_or_points: Union[T, List[T]]) -> None:
        """
        Add new data point(s) to the histogram.

        Args:
            point_or_points (Union[T, List[T]]): A single data point or a list of data points.
        """
        if not isinstance(point_or_points, list):
            point_or_points = [point_or_points]
        for point in point_or_points:
            if len(self._data) == self._max_size:
                self._data[random.randint(0, self._max_size - 1)] = point
            else:
                self._data.append(point)
        self._dirty = True

    def sample(self) -> T:
        """
        Sample a single data point from the histogram.

        Returns:
            T: A sampled data point.
        """
        return self.sample_n(1)[0]

    # pylint: disable=method-hidden
    def percentile(self, p: float) -> T:
        """
        Return the data point at the given percentile.

        Args:
            p (float): The percentile value (between 0 and 1).

        Returns:
            T: The data point at the given percentile.
        """
        if self._dirty:
            self._data.sort()
            self._dirty = False
        idx = math.floor(len(self._data) * p)
        return self._data[min(idx, len(self._data) - 1)]

    def mean(self) -> float:
        total = sum(self._data)
        return float(total) / len(self._data)

    # pylint: disable=method-hidden
    def sample_n(self, n: int) -> List[T]:
        """
        Sample n data points from the histogram.

        Args:
            n (int): The number of data points to sample.

        Returns:
            List[T]: A list of sampled data points.
        """
        return random.sample(self._data, n)

    def clone(self) -> Self:
        """
        Create a deep copy of the histogram.

        Returns:
            Self: A new Histogram instance with the same data and max size.
        """
        c = Histogram(max_size=self._max_size, data=self._data)
        c.sample_n = self.sample_n
        c.percentile = self.percentile
        return c

    def resize(self, size: int) -> Self:
        """
        Resize the histogram to a new maximum size.

        Args:
            size (int): The new maximum size for the histogram.

        Returns:
            Self: The current Histogram instance with the new maximum size.
        """
        if size < self._max_size:
            self._data = random.sample(self._data, size)
        self._max_size = size
        return self


def _adjust(h: Histogram[T], func: Callable[[T], T]) -> Histogram[T]:
    """
    Helper function to adjust the data points in a histogram using a given function.

    Args:
        h (Histogram[T]): The input Histogram instance.
        func (Callable[[T], T]): A function to apply to each data point.

    Returns:
        Histogram[T]: A new Histogram instance with the adjusted data points.
    """
    result = h.clone()
    orig_sample_n = h.sample_n

    def scaled_sample_n(*args: int) -> T:
        n = args[-1]
        return [
            func(v) for v in orig_sample_n(n)
        ]
    result.sample_n = scaled_sample_n

    orig_percentile = h.percentile

    def scaled_percentile(*args: float) -> T:
        p = args[-1]
        return func(orig_percentile(p))
    result.percentile = scaled_percentile

    return result


# pylint: disable=invalid-name
def Max(h: Histogram[T], val: T) -> Histogram[T]:
    """
    Adjust the histogram such that no data point exceeds the given value.

    Args:
        h (Histogram[T]): The input Histogram instance.
        val (T): The maximum value for the data points.

    Returns:
        Histogram[T]: A new Histogram instance with the adjusted data points.
    """
    def f(v: T) -> T:
        return min(v, val)
    return _adjust(h, f)


# pylint: disable=invalid-name
def MaxAtPercentile(h: Histogram[T], p: float) -> Histogram[T]:
    """
    Adjust the histogram such that no data point exceeds the value at the given percentile.

    Args:
        h (Histogram[T]): The input Histogram instance.
        p (float): The percentile value (between 0 and 1).

    Returns:
        Histogram[T]: A new Histogram instance with the adjusted data points.
    """
    def f(v: T) -> T:
        val = h.percentile(p)
        return min(v, val)
    return _adjust(h, f)


# pylint: disable=invalid-name
def Min(h: Histogram[T], val: T) -> Histogram[T]:
    """
    Adjust the histogram such that no data point is less than the given value.

    Args:
        h (Histogram[T]): The input Histogram instance.
        val (T): The minimum value for the data points.

    Returns:
        Histogram[T]: A new Histogram instance with the adjusted data points.
    """
    def f(v: T) -> T:
        return max(v, val)
    return _adjust(h, f)


# pylint: disable=invalid-name
def MinAtPercentile(h: Histogram[T], p: float) -> Histogram[T]:
    """
    Adjust the histogram such that no data point is less than the value at the given percentile.

    Args:
        h (Histogram[T]): The input Histogram instance.
        p (float): The percentile value (between 0 and 1).

    Returns:
        Histogram[T]: A new Histogram instance with the adjusted data points.
   """
    def f(v: T) -> T:
        val = h.percentile(p)
        return max(v, val)

    return _adjust(h, f)


# pylint: disable=invalid-name
def Shift(h: Histogram[T], val: T) -> Histogram[T]:
    """
   Shift all data points in the histogram by the given value.

   Args:
       h (Histogram[T]): The input Histogram instance.
       val (T): The value to shift the data points by.

   Returns:
       Histogram[T]: A new Histogram instance with the shifted data points.
   """

    def f(v: T) -> T:
        return v + val

    return _adjust(h, f)


# pylint: disable=invalid-name
def Scale(h: Histogram[T], scalar: T) -> Histogram[T]:
    """
   Scale all data points in the histogram by the given scalar.

   Args:
       h (Histogram[T]): The input Histogram instance.
       scalar (T): The scalar value to multiply the data points by.

   Returns:
       Histogram[T]: A new Histogram instance with the scaled data points.
   """

    def f(v: T) -> T:
        return v * scalar

    return _adjust(h, f)


class Group(Generic[T]):
    """
   A Group class to represent a collection of Histograms or other Groups.

   Attributes:
       _elements (List[Tuple[str, Union[Histogram, Self]]]): A list of
            tuples containing the name and Histogram/Group instances.
       _name (str): The name of the Group.
   """

    def __init__(
            self,
            elements: List[Tuple[str, Union[Histogram, Self]]] = None,
            name: str = 'root'):
        self._elements: List[Tuple[str, Union[Histogram, Self]]] = elements or []
        self._name = name

    def __add__(self, other: Union[Tuple[str, Histogram], Self]) -> Self:
        """
       Overloading the + operator to add a new Histogram or Group to the Group.

       Args:
           other (Union[Tuple[str, Histogram], Self]): A tuple containing
            the name and Histogram instance, or another Group instance.

       Returns:
           Self: A new Group instance with the added element.
       """
        result = self.clone()
        result += other._name, other
        return result

    def __iadd__(self, other: Tuple[str, Union[Histogram, Self]]) -> Self:
        """
       Overloading the += operator to add a new Histogram or Group to the Group.

       Args:
           other (Tuple[str, Union[Histogram, Self]]): A tuple
                containing the name and Histogram/Group instance.

       Returns:
           Self: The current Group instance with the added element.
       """
        _, val = other
        if isinstance(other, Tuple) and isinstance(val, (Group, Histogram)):
            self._elements += [other]
        else:
            return NotImplemented

        return self

    def sample(self) -> T:
        """
       Sample a value from the Group by summing samples from its elements.

       Returns:
           T: The sampled value.
       """
        return sum(
            el.sample() for _, el in self._elements
        )

    def explain_sample(self, group_name: str = None) -> Dict[str, Any]:
        """
       Explain the sampled value by breaking it down into contributions from each element.

       Args:
           group_name (str, optional): The name of the Group to explain.
                Defaults to the Group's own name.

       Returns:
           Dict[str, Any]: A dictionary explaining the sampled value,
                with keys 'name', 'elements', and 'total'.
       """
        if not group_name:
            group_name = self._name
        total = 0
        elements = []
        for name, el in self._elements:
            if isinstance(el, Group):
                expl = el.explain_sample(group_name=name)
                elements.append(expl)
                total += expl.get('total', 0)
            else:
                val = el.sample()
                total += val
                elements.append({
                    'name': name,
                    'total': val
                })

        return {
            'name': group_name,
            'elements': elements,
            'total': total
        }

    def clone(self) -> Self:
        """
        Create a deep copy of the Group instance.

        This method creates a new instance of the Group class with a copy of the internal
        elements list. The new instance is a separate object from the original, and modifications
        to one instance will not affect the other.

        Returns:
            Self: A new Group instance with the same elements as the original.
        """
        result = Group[T]([], self._name)
        for name, el in self._elements:
            result += name, el.clone()
        return result
