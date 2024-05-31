import unittest
from mltoolkit_laht import visualization

class TestVisualization(unittest.TestCase):
    def test_plot_data(self):
        # Assume we have some data for testing
        data = [1, 2, 3, 4, 5]
        
        # Assume plot_data function returns a matplotlib object
        result = visualization.plot_data(data)
        
        # Check if the function returns the correct type
        self.assertIsInstance(result, matplotlib.figure.Figure)

if __name__ == '__main__':
    unittest.main()