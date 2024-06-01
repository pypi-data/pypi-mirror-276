import unittest
from color_mapper import value_to_color

class TestColorMapper(unittest.TestCase):

    def test_value_to_color(self):
        values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        color_bases = ['blue', 'yellow', 'red']
        result = value_to_color(values, color_bases)
        self.assertEqual(len(result), len(values))
        for item in result:
            self.assertIn('value', item)
            self.assertIn('color', item)
            self.assertTrue(item['color'].startswith('#'))

if __name__ == '__main__':
    unittest.main()
