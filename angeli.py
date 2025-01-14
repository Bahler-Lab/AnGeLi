import gzip
import io
import csv
from enum import Enum
import requests

# Pomebe base data URL, used as the common construct for other URLs
POMBE_BASE_URL = 'https://www.pombase.org/data'

# URLs for accessing data from the Pombase website
PEPTIDE_URL = POMBE_BASE_URL + "/Protein_data/PeptideStats.tsv"
PROTEIN_COMPOSITION_URL = POMBE_BASE_URL + "/Protein_data/aa_composition.tsv"
ALL_CHROMOSOMES_GFF3_URL = POMBE_BASE_URL + "/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3"
GO_TERMS = "/releases/latest/pombase-2025-01-01.gaf.gz"
FYPO_TERMS = "/releases/latest/pombase-2025-01-01.phaf.gz"

class Peptide(Enum):
    SYSTEMATIC_ID = 0
    MASS = 1
    PI = 2
    CHARGE = 3

class ProteinComposition(Enum):
    SYSTEMATIC_ID = 0
    A = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    K = 9
    L = 10
    M = 11
    N = 12
    P = 13   
    Q = 14
    R = 15
    S = 16
    T = 17
    V = 18
    W = 19
    Y = 20

    class AnGeLi:
        def __init__(self):
            """Constructor lazy loads the data, so declare values and assign them as None"""
            self.peptides = None
            self.amino_acids = None
            self.chromosome = None
            self.go_terms = None
            self.fypo_terms = None

        def download_file(self, url):
            """
            Downloads a file from a URL and returns the content as a BytesIO object.

            :param url: The URL of the file.
            :return: A BytesIO object containing the content.
            """
            # Send a GET request to the URL
            response = requests.get(url)

            if response.status_code == 200:
                # Return the content as a BytesIO object
                return io.BytesIO(response.content)
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
                return None

        def download_and_decompress_gzip(self, url):
            """
            Downloads a file from a URL, decompresses it using gzip, and returns the decompressed content as a BytesIO object.

            :param url: The URL of the gzip-compressed file.
            :return: A BytesIO object containing the decompressed content.
            """
            # Send a GET request to the URL
            response = requests.get(url, stream=True)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Create a GzipFile object from the downloaded content
                with gzip.GzipFile(fileobj=io.BytesIO(response.content), mode='rb') as gz:
                    # Read the decompressed content into a BytesIO object
                    decompressed_content = io.BytesIO(gz.read())
                
                print("File successfully downloaded and decompressed.")
                return decompressed_content
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
                return None
            
        def parse_tsv(self, file_obj, encoding='utf-8'):
            """
            Parses a TSV (Tab-Separated Values) stream and returns a list of rows.

            Args:
            - byte_stream (BytesIO): The input TSV stream (in bytes).

            Returns:
            - List[List[str]]: A list of rows, where each row is a list of columns.
            """
            # Rewind the BytesIO stream to the beginning
            file_obj.seek(0)

            # Decode the byte stream into a string (text mode)
            decoded_stream = file_obj.read().decode(encoding)

            # Convert the decoded text into a file-like object (string input stream)
            text_stream = io.BytesIO(decoded_stream.encode(encoding))

            # Create a CSV reader with tab delimiter
            tsv_reader = csv.reader(decoded_stream.splitlines(), delimiter='\t')

            # Parse the TSV content and store it as a list of rows
            parsed_data = [row for row in tsv_reader]

            return parsed_data

        def parse_gff3(self, file_obj):
            """
            Parses a GG3 file and returns the features.

            :param url: The gff file object
            :return: A gffutils database object
            """
            # Create a database from the GFF3 file object
            db = None
            # gffutils.create_db(file_obj, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)
            
            return db

        def build_file_headers(self):
            print("Building file headers")

        def search_protein_features(self, protein_id):
            """
            Parses a GG3 file and returns the features.

            :param url: The gff file object
            :return: A gffutils database object
            """
            if self.peptides is None:   
                print("Loading protein features")
                self.peptides = self.parse_tsv(self.download_file(PEPTIDE_URL))
            
            return list(filter(lambda sublist: sublist[Peptide.SYSTEMATIC_ID.value] == protein_id, self.peptides))
            

        def search_amino_acids(self, protein_id):
            """
            Finds the amino acid composition of a protein and returns the percentage composition of each amino acid.

            :param url: The protein to search for
            :return: A list of the percentage composition of amino acids in the protein
            """
            if self.amino_acids is None:   
                print("Loading Amino acids")
                self.amino_acids = self.parse_tsv(self.download_file(PROTEIN_COMPOSITION_URL))
            
            data = list(filter(lambda sublist: sublist[Peptide.SYSTEMATIC_ID.value] == protein_id, self.peptides))

            # There should only be one result! 
            if len(self.amino_acids) == 0:
                print("No amino acid data found")
                return None
            elif len(self.amino_acids) > 1:
                print("Multiple amino acid data found")
                return None
            else:

                return None


            return None

        def search_chromosome_features(self):
            """
            

            :param url: 
            :return: 
            """
            if self.chromosome is None:   
                print("Loading Amino acids")
                self.chromosome = self.parse_gff3(self.download_file(ALL_CHROMOSOMES_GFF3_URL))

        def find_go_terms(self):
            """
            

            :param url: 
            :return: 
            """
            if self.go_terms is None:   
                print("Loading Amino acids")
                self.go_terms = self.parse(self.download_and_decompress_gzip(GO_TERMS))

        def find_fypo_terms(self):
            """
            

            :param url: 
            :return: 
            """
            if self.chromosome is None:   
                print("Loading Amino acids")
                self.chromosome = self.parse_gff3(self.download_and_decompress_gzip(FYPO_TERMS))

        def parse_original_AnGeLiDatabase(self):
            print("Parsing the original AnGeLiDatabase.txt file")

def main():
    """
    Reconstruct the AnGeLiDatabase.txt file 

    The method opens and parses the AnGeLiDatabase.txt file
    It then iterates over the various components and downloads the relevant sources and updates the fields.
    For GO and FYPO terms, the entire structure is rebuilt. See the README for more information.
    """
    print("hellow world")

# Example usage
if __name__ == "__main__":
    main()