import unittest
import tempfile
import os
from gpt_repository_loader.loader import process_repository, get_ignore_list

class TestGPTRepositoryLoader(unittest.TestCase):

    def setUp(self):
        self.test_data_path = os.path.join(os.path.dirname(__file__), '../test_data')
        self.example_repo_path = os.path.join(self.test_data_path, 'example_repo')

    def test_end_to_end(self):
        output_file_path = os.path.join(tempfile.mkdtemp(), 'output.txt')
        expected_output_file_path = os.path.join(self.test_data_path, 'expected_output.txt')

        ignore_file_path = os.path.join(self.example_repo_path, ".gptignore")
        ignore_list = get_ignore_list(ignore_file_path) if os.path.exists(ignore_file_path) else []

        with open(output_file_path, 'w') as output_file:
            process_repository(self.example_repo_path, ignore_list, output_file)

        with open(output_file_path, 'r') as output_file, open(expected_output_file_path, 'r') as expected_output_file:
            self.assertEqual(output_file.read(), expected_output_file.read())

    def test_placeholder(self):
        self.assertTrue(True)

    def test_get_ignore_list(self):
        # Create temporary ignore files
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write("*.txt\n#comment\n*.pyc\n")
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write("*.jpg\n*.png\n")
        
        ignore_list = get_ignore_list([f1.name, f2.name])
        
        self.assertEqual(len(ignore_list), 4)
        self.assertIn("*.txt", ignore_list)
        self.assertIn("*.pyc", ignore_list)
        self.assertIn("*.jpg", ignore_list)
        self.assertIn("*.png", ignore_list)
        self.assertNotIn("#comment", ignore_list)
        
        # Cleanup
        os.unlink(f1.name)
        os.unlink(f2.name)

if __name__ == '__main__':
    unittest.main()
