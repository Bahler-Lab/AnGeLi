# Test the files to make sure we have the enums correct.
# All files are located in /test_data
import unittest
from angeli import AnGeLi

class TestAnGeLi(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        # Create a new MyClass instance for testing
        self.db = AnGeLi()

    def read_test_tsv(self, file_name):
        """Read a test TSV file and return the content as a list of dictionaries."""
        # Open the test TSV file
        with open(f"test_data/{file_name}", "rb") as file:
            # Parse the TSV file using the parse_tsv method
            return self.db.parse_tsv(file)

    def test_peptides(self):
        """Test the greet function."""
        # Expected greeting string
        expected_greeting = "Hello, my name is Alice and I am 30 years old."
        # Actual greeting from the greet function
        actual_greeting = self.person.greet()
        # Assert that the actual greeting matches the expected greeting
        self.assertEqual(actual_greeting, expected_greeting)