"""
	Filter sensor outputs.  User can choose from various filtering techniques:
		* Range Filter: truncate sensor readings to a (min, max) range
		* Temporal Median Filter: Return the median of the most recent D scans (by element)

"""
import abc 

import numpy as np
import numbers

class Filter(object):
	"""
		Abstract base class to structure specific filtering methods

	"""

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def update(self, sensor_data):
		return

class RangeFilter(Filter):
	"""
	Perform range filtering that bounds data output by user-specified 
	minimum and maximum values
	"""

	def __init__(self, min_val=-float("inf"), max_val=float("inf")):
		if not isinstance(min_val, numbers.Number) or not isinstance(max_val, numbers.Number):
			raise TypeError("Filter bounds must be of number type")

		self.min_val = min_val
		self.max_val = max_val

	def update(self, sensor_data):
		"""
		Truncate input data range to user-defined min and max values

		Input:
			sensor_data: list/array of sensor readings (floats)
		Output:
			new list of sensor readings, bounded by min and max values as 
			specified in class initialization

		"""

		return np.clip(sensor_data, self.min_val, self.max_val)

class MedianFilter(Filter):
	"""
	Filter sensor data by finding the element-wise median of latest sensor
	readings.  User decides how many prior readings should be included in 
	the median
	"""

	def __init__(self, num_scans_to_median):
		if isinstance(num_scans_to_median, (int, long)) and num_scans_to_median > 0:
			self.num_scans_to_median = num_scans_to_median + 1
			self.scan_history = None
			self.new_data_index = 0
			self.update_iteration = 0
		else:
			raise TypeError("Median history size must be a natural number (eg 1, 2, 3, ...)")

	def update(self, sensor_data):
		"""
		Get median values from most recent sensor readings

		Input:
			sensor_data: list/array of sensor readings (floats)
		Output:
			new list of sensor readings where each element is the median of
			respective elements from the last D sensor readings (including
			most recent).  D is specified in class initialization

		"""

		# Convert incoming data to numpy array for consistency
		sensor_data = np.asarray(sensor_data).flatten()
		self.update_iteration += 1	# Only look at valid portions of the history

		# Initialize an array to store historic values if not done already 
		# (eg first run of update)
		if self.scan_history is None:
			self.scan_history = np.empty((self.num_scans_to_median, sensor_data.shape[0]),
			 							dtype=np.float)
		
		# Test for data size mismatch
		if sensor_data.shape[0] != self.scan_history.shape[1]:
			raise IndexError("New data does not contain the same number of elements as prior data")

		# Overwrite the oldest data in the history with the newest data
		self.scan_history[self.new_data_index] = sensor_data
		self.new_data_index = (self.new_data_index + 1) % self.num_scans_to_median

		# Return index-wise median value of most recent historical data
		# Only look at the valid portions of the sensor history (when the number of 
		# updates is less than the sensor history size)
		if(self.update_iteration < self.num_scans_to_median ):
			return np.median(self.scan_history[:self.update_iteration][:], axis=0)
		else:
			return np.median(self.scan_history, axis=0)

