# This is a test script to check the basic functionality of the foo_param package
# If the package is updated, this script should be run to ensure that the essential functions are working as expected.

# Import the unittest module
import unittest
from foo_param.core import calculate_volume

# Define a class that inherits from unittest.TestCase
class TestCoreFunctions(unittest.TestCase):

    # Define a test method to check the calculate_volume function
    def test_calculate_volume(self):
        # Check the volume calculation for a high-precision value
        self.assertAlmostEqual(calculate_volume(1), 4.18879, places=5)
        # Check the volume calculation for a larger radius
        self.assertAlmostEqual(calculate_volume(0), 0)
    
    # Define a test method to check the behavior of calculate_volume with negative input
    def test_calculate_volume_negative(self):
        # Check that a ValueError is raised for a negative radius
        with self.assertRaises(ValueError):
            calculate_volume(-1)

# Run the test script
if __name__ == '__main__':
    unittest.main()
