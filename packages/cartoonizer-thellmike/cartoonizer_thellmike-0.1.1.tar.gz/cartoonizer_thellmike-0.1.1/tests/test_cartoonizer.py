import unittest
from cartoonizer import apply_cartoon_effect

class TestCartoonizer(unittest.TestCase):

    def test_apply_cartoon_effect(self):
        apply_cartoon_effect('input_image.jpg', 'output_image.png')
        self.assertTrue(True)  # Simple test to ensure the function runs without error

if __name__ == '__main__':
    unittest.main()
