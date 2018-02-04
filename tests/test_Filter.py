"""
	Unit testing for Filter modules:
		Range Filter
		Temporal Median Filter
"""

import numpy as np
import unittest

from Filter import Filter

class TestRangeFilter(unittest.TestCase):

	def setUp(self):
		pass

	def test_init_nonnum(self):
		"""
		Filter should return an error if non-float init arguments are provided
		"""
		self.assertRaises(TypeError, Filter.RangeFilter, "a")

	def test_init_none(self):
		"""
		No clipping should occur when RangeFilter is initialized with no args
		(defaults to bounding by [-inf, inf] )

		"""
		filt = Filter.RangeFilter();

		num_entries = 50
		size_entry = 20
		bounds = 5000
		for i in range(num_entries):
			random_data = np.random.uniform(-bounds, bounds, size_entry)
			self.assertTrue(np.array_equal(random_data, filt.update(random_data)))

	def test_clipping(self):
		"""
		Sense check that filtered elements are unchanged or set to bound values
		"""

		lower_bound = -100.9
		upper_bound = 222.22
		filt = Filter.RangeFilter(lower_bound, upper_bound)

		num_entries = 50
		size_entry = 20
		bounds = 5000
		for row in range(num_entries):
			random_data = np.random.uniform(-bounds, bounds, size_entry)
			filtered_data = filt.update(random_data)

			for elem_index in range(size_entry):
				if random_data[elem_index] > upper_bound:
					self.assertEqual(filtered_data[elem_index], upper_bound)
				elif random_data[elem_index] < lower_bound:
					self.assertEqual(filtered_data[elem_index], lower_bound)
				else:
					self.assertEqual(filtered_data[elem_index], random_data[elem_index])

	def test_list_clipping(self):
		"""
		Sense check that filtered elements are unchanged or set to bound values
		For this test, input data will be a list (vs numpy array)
		"""

		lower_bound = -100.9
		upper_bound = 222.22
		filt = Filter.RangeFilter(lower_bound, upper_bound)

		num_entries = 50
		size_entry = 20
		bounds = 5000
		for row in range(num_entries):
			random_data = [np.random.uniform(-bounds, bounds) for i in range(size_entry)]
			filtered_data = filt.update(random_data)

			for elem_index in range(size_entry):
				if random_data[elem_index] > upper_bound:
					self.assertEqual(filtered_data[elem_index], upper_bound)
				elif random_data[elem_index] < lower_bound:
					self.assertEqual(filtered_data[elem_index], lower_bound)
				else:
					self.assertEqual(filtered_data[elem_index], random_data[elem_index])

	def tearDown(self):
		pass


class TestMedianFilter(unittest.TestCase):

	def setUp(self):
		pass

	def test_init_none(self):
		"""
		Filter should return an error if no init arguments are provided
		"""
		self.assertRaises(TypeError, Filter.MedianFilter, )

	def test_init_nonnum(self):
		"""
		Filter should return an error if non-whole arguments are provided
		"""
		self.assertRaises(TypeError, Filter.MedianFilter, ("x"))

	def test_init_float(self):
		"""
		Filter should return an error if non-whole arguments are provided
		"""
		self.assertRaises(TypeError, Filter.MedianFilter, (2.5))

	def test_init_negative(self):
		"""
		Filter should return an error if non-whole arguments are provided
		"""
		self.assertRaises(TypeError, Filter.MedianFilter, (-5))

	def test_init_zero(self):
		"""
		Filter should return an error if non-whole arguments are provided
		"""
		self.assertRaises(TypeError, Filter.MedianFilter, 0)

	def test_promp_example(self):
		"""
		Use the example given by the question prompt
		"""
		filt = Filter.MedianFilter(3)
		input_scan = [[0., 1., 2., 1., 3.], 
					[1., 5., 7., 1., 3.],
					[2., 3., 4., 1., 0.],
					[3., 3., 3., 1., 3.],
					[10., 2., 4., 0., 0.]]
		update_expected = [[0., 1., 2., 1., 3.],
							[0.5, 3., 4.5, 1., 3.], 
							[1., 3., 4., 1., 3.], 
							[1.5, 3., 3.5, 1., 3.],
							[2.5, 3., 4., 1., 1.5] ]

		for row in range(len(input_scan)):
			output = filt.update(input_scan[row])
			self.assertTrue(np.array_equal(output, update_expected[row]))

	def test_promp_example_arrays(self):
		"""
		Use the example given by the question prompt
		This time input is provided as numpy arrays 
		"""
		filt = Filter.MedianFilter(3)
		input_scan = [[0., 1., 2., 1., 3.], 
					[1., 5., 7., 1., 3.],
					[2., 3., 4., 1., 0.],
					[3., 3., 3., 1., 3.],
					[10., 2., 4., 0., 0.]]
		update_expected = [[0., 1., 2., 1., 3.],
							[0.5, 3., 4.5, 1., 3.], 
							[1., 3., 4., 1., 3.], 
							[1.5, 3., 3.5, 1., 3.],
							[2.5, 3., 4., 1., 1.5] ]

		for row in range(len(input_scan)):
			output = filt.update(np.asarray(input_scan[row]))
			self.assertTrue(np.array_equal(output, update_expected[row]))

	def test_array_extra_dim(self):
		"""
		Try filtering data with dimension (1, N)
		"""

		filt = Filter.MedianFilter(2)
		num_entries = 50
		size_entry = 20
		input_data = np.zeros((1, size_entry), dtype = np.float)
		for i in range(num_entries):
			output = filt.update(input_data)
			self.assertTrue(np.array_equal(output, input_data[0]))

	def tearDown(self):
			pass
			
if __name__ == "__main__":
	unittest.main()