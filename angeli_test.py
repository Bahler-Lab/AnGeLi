# Test the files to make sure we have the enums correct.
# All files are located in /test_data
import unittest
from angeli import AnGeLi, Peptide

class TestAnGeLi(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        # Create a new MyClass instance for testing
        self.db = AnGeLi()

    def test_peptides(self):
        """Test the peptide stats function."""
        systematic_id = "SPAC1002.03c"
        expected_mass = "106.28"

        data = self.db.search_protein_features(systematic_id)
        # Assert that the actual greeting matches the expected greeting
        self.assertEqual(data[0][Peptide.MASS.value], expected_mass)
    
    def test_amino_acids(self):
        """Test the amnino acid function function."""

        systematic_id = "SPAC1002.03c"

        data = self.db.search_amino_acids(systematic_id)
        # Assert that the actual greeting matches the expected greeting
        self.assertEqual(data[0][Peptide.MASS.value], expected_mass)

if __name__ == '__main__':
    unittest.main()