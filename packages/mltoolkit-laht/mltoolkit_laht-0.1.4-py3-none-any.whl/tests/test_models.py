import unittest
from mltoolkit_laht import models

class TestModels(unittest.TestCase):

    def test_model1(self):
        # Initialize model
        model = models.Model1()

        # Test model methods
        self.assertIsNotNone(model.train)
        self.assertIsNotNone(model.predict)
        self.assertIsNotNone(model.evaluate)

if __name__ == '__main__':
    unittest.main()