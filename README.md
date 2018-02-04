# Sensor Data Filter

This module provides filtering capability for real-valued sensor data.  Currently supported filters are:

* Range Filter - bound data values to user-specified min and max values
* Temporal Median Filter - generate element-wise median of rolling historical data

For more information on possible use cases and intended functionality, please look at the included 'Lidar_Fitler_Request.pdf' file that inspired this project

### Prerequisites

This module has been tested on Python 2.7 and requires Numpy.  You can use PiP to install Numpy:

```
pip install numpy
```
or view alternative installation instructions on the [Numpy site](https://www.scipy.org/scipylib/download.html).


### Use

All filters inherit from the Filter class and support an *update()* method that takes in a real-valued list/array of sensor data and returns the filtered result.

To use a Range Filter, specify minimum and maximum values to bound the sensor readings.  Unspecified range values will default to negative and positive infinity, respectively:

```
from Filter import Filter
									# Filtered Output Bounds:
filt1 = Filter.RangeFilter()		# [-inf, inf]
filt2 = Filter.RangeFilter(-5)		# [-5,   inf]
filt3 = Filter.RangeFilter(,15)		# [-inf, 15 ]
filt4 = Filter.RangeFilter(-7, 250)	# [-7,   250]

filt4.update([-100, 7.4, 0, 650])	# Returns: [-7., 7.4, 0., 250.]
```

The Temporal Median Filter takes exactly one arguement, a whole number of prior scans for which the median should be taken (the data sent in the calling update() method is automatically included)

```
from Filter import Filter

filt1 = Filter.MedianFilter(3)			# Returns:
filt.update([0., 1., 2., 1., 3.])		# [0.,  1., 2.,  1., 3.]
filt.update([1., 5., 7., 1., 3.])		# [0.5, 3., 4.5, 1., 3.]
filt.update([2., 3., 4., 1., 0.])		# [1.,  3., 4.,  1., 3.]
filt.update([3., 3., 3., 1., 3.])		# [1.5, 3., 3.5, 1., 3.]
filt.update([10., 2., 4., 0., 0.])		# [2.5, 3., 4.,  1., 1.5]
```

Note that the Range Filter will work for any 1D list/array but the Temporal Median Filter requires that all calls to update use the same length of sensor data

## Running the tests

All included tests can be run by executing the following from the root project directory:
```
python -m unittest discover
```

## Authors

* **Osman Shawkat** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* README template courtesy of Bille Thompson - [PurpleBooth](https://github.com/PurpleBooth)

