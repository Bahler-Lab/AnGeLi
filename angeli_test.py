# Test the files to make sure we have the enums correct.
# All files are located in /test_data
import unittest
from angeli import AnGeLi, Peptide

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
        # file name
        filename = "PeptideStats.tsv"
        
        systematic_id = "SPAC1002.03c"
        expected_mass = "106.28"

        data = self.db.search_protein_features(systematic_id)
        # Assert that the actual greeting matches the expected greeting
        self.assertEqual(data[0][Peptide.MASS.value], expected_mass)

if __name__ == '__main__':
    unittest.main()