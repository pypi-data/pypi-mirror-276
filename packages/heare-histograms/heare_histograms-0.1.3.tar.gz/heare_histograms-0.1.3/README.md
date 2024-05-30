# Heare Histograms Library
This library provides two main classes: Histogram and Group. The Histogram class is a generic data structure for storing and sampling data points, while the Group class represents a collection of Histogram instances or other Group instances. 
Groups can be used to generate synthetic composite histograms. 

# Installation
To install the library, you can use pip:


```sh
pip install heare-histograms
```

# Usage
## Histogram
The Histogram class can be imported and used as follows:

```python
from heare.histograms import Histogram, Shift, Scale, Max

# Create a new histogram
hist = Histogram[int](max_size=1000)

# Observe data points
hist.observe([1, 2, 3, 4, 5])

# Sample a data point
sample = hist.sample()

# Get the value at a given percentile
percentile_val = hist.percentile(0.9)

# Combine two histograms
hist2 = Histogram[int](data=[10, 20, 30])
combined = hist + hist2

# Apply transformations to the histogram
shifted_hist = Shift(hist, 10)
scaled_hist = Scale(hist, 2.0)
capped_hist = Max(hist, 100)
```
The Histogram class supports various operations, such as observing new data points, sampling, computing percentiles, combining histograms, and applying transformations like shifting, scaling, and capping values.

# Group
The Group class can be imported and used as follows:

```python
from heare.histograms import Histogram, Group

# Create a new group with two histograms
hist1 = Histogram[int](data=[1, 2, 3])
hist2 = Histogram[int](data=[10, 20, 30])
group = Group[int]([("hist1", hist1), ("hist2", hist2)])

# Sample a value from the group
sample = group.sample()

# Explain the sampled value
explanation = group.explain_sample()
```
The Group class allows you to combine multiple Histogram instances or other Group instances into a single entity. You can sample values from the group and obtain an explanation of the sampled value, breaking it down into contributions from each element.


# Contributing
Contributions to the library are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/heare-io/heare-histograms).

# License
This library is released under the [MIT License](https://opensource.org/license/mit).