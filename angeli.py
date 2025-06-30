import argparse
from datetime import datetime
import gzip
import io
import csv
from enum import Enum
import os
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re 

from OrderedMatrix import OrderedMatrix 

logging.basicConfig(
    filename='angeli_output.log',  # Log file name
    filemode='a',  # Append mode ('w' for overwrite)
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO)

# Pomebe base data URL, used as the common construct for other URLs
POMBE_BASE_URL = 'https://www.pombase.org/data'

# URLs for accessing data from the Pombase website
POMBASE_LATEST_URL = POMBE_BASE_URL + "/releases/latest"
PEPTIDE_URL = POMBE_BASE_URL + "/Protein_data/PeptideStats.tsv"
PROTEIN_COMPOSITION_URL = POMBE_BASE_URL + "/Protein_data/aa_composition.tsv"
ALL_CHROMOSOMES_GFF3_URL = POMBE_BASE_URL + "/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3"
GO_TERMS_PATTERN = ".gaf.gz"
FYPO_TERMS_PATTERN = ".phaf.gz"

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
        self.original_file = None

    def _download_file(self, url):
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
            logging.error(f"Failed to download the file. Status code: {response.status_code}")
            return None

    def _get_files_with_suffix(self, base_url, suffix):
        """
        Fetches all files from a directory listing at the given URL
        and returns filenames that end with the specified suffix.

        Args:
            base_url (str): The URL of the directory to search.
            suffix (str): File suffix to filter by (e.g. '.gaf.gz').

        Returns:
            List[str]: A list of matching filenames or full URLs.
        """
        if not base_url.startswith("http"):
            raise ValueError("URL must start with 'http' or 'https'.")
        
        if not base_url.endswith("/"):
            base_url += "/"

        try:
            response = requests.get(base_url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch URL: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        matched_files = []

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                href = href.strip()
                if href.lower().endswith(suffix.lower()):
                    matched_files.append(urljoin(base_url, href))

        return matched_files

    def _download_and_decompress_gzip(self, url):
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
            
            logging.info("File successfully downloaded and decompressed.")
            return io.TextIOWrapper(decompressed_content, encoding='utf-8')
        else:
            logging.error(f"Failed to download the file. Status code: {response.status_code}")
            return None
        
    def _parse_tsv(self, file_obj, encoding='utf-8'):
        """
        Parses a TSV (Tab-Separated Values) stream and returns a list of rows.

        Args:
        - byte_stream (BytesIO): The input TSV stream (in bytes).

        Returns:
        - List[List[str]]: A list of rows, where each row is a list of columns.
        """
        if hasattr(file_obj, 'read'):
            file_obj.seek(0)
            decoded_text = file_obj.read().decode(encoding)
        elif isinstance(file_obj, str):
            decoded_text = file_obj
        else:
            raise TypeError("Input must be a bytes stream or a string.")

        tsv_reader = csv.reader(decoded_text.splitlines(), delimiter='\t')
        return [row for row in tsv_reader]

    def _parse_gff3(self, file_obj):
        """
        Parses a GG3 file and returns the features.

        :param url: The gff file object
        :return: A gffutils database object
        """
        # Create a database from the GFF3 file object
        db = None
        # gffutils.create_db(file_obj, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)
        
        return db

    def _parse_gaf(self, file_obj):
        annotations = []

        reader = csv.reader(file_obj, delimiter='\t')
        for row in reader:
            if not row or row[0].startswith('!'):
                continue  

            annotation = {
                'DB': row[0],
                'DB_Object_ID': row[1],
                'DB_Object_Symbol': row[2],
                'Qualifier': row[3],
                'GO_ID': row[4],
                'DB_Reference': row[5],
                'Evidence_Code': row[6],
                'With_From': row[7],
                'Aspect': row[8],
                'DB_Object_Name': row[9],
                'DB_Object_Synonym': row[10],
                'DB_Object_Type': row[11],
                'Taxon': row[12],
                'Date': row[13],
                'Assigned_By': row[14],
                'Annotation_Extension': row[15],
                'Gene_Product_Form_ID': row[16]
            }

            annotations.append(annotation)

        return annotations
    
    def _parse_phaf(self, file_obj):
        annotations = []

        reader = csv.reader(file_obj, delimiter='\t')
        for row in reader:
            if not row or row[0].startswith('#'):
                continue  
            # Database name,	Gene systematic ID, FYPO ID	
            # Allele description, Expression, Parental strain
            # Strain name (background), Genotype description
            # Gene symbol, 	Allele name, Allele synonym
            # Allele type, Evidence, Condition
            # Penetrance, Severity, Extension	
            # Reference,	Taxon,	Date,	Ploidy
            annotation = {
                'DB': row[0],
                'GENE_ID': row[1],
                'FYPO_ID': row[2],
                'ALLELE_DESC': row[3],
                'EXPRESSION': row[4],
                'PARENT_STRAIN': row[5],
                'STRAIN_NAME': row[6],
                'GENOTYPE_DESC': row[7],
                'GENE_SYMBOL': row[8],
                'ALLELE_NAME': row[9],
                'ALLELE_SYNON': row[10],
                'ALLELE_TYPE': row[11],
                'EVIDENCE': row[12],
                'CONDITION': row[13],
                'PENETRANCE': row[14],
                'SEVERITY': row[15],
                'EXTENSION': row[16],
                'REFERENCE': row[17],
                'TAXON': row[18],
                'DATE': row[19],
                'PLOIDY': row[20]
            }

            annotations.append(annotation)

        return annotations
    
    def search_protein_features(self, protein_id):
        """
        NOT used at present since this data should be relatively static.
        Keeping in case it is needed in the future.
        
        Parses a GG3 file and returns the features.

        :param url: The gff file object
        :return: A gffutils database object
        """
        if self.peptides is None:   
            logging.info("Loading protein features")
            self.peptides = self._parse_tsv(self._download_file(PEPTIDE_URL))
        
        return list(filter(lambda sublist: sublist[Peptide.SYSTEMATIC_ID.value] == protein_id, self.peptides))
        

    def search_amino_acids(self, protein_id):
        """
        NOT used at present since this data should be relatively static.
        Keeping in case it is needed in the future.
        
        Finds the amino acid composition of a protein and returns the percentage composition of each amino acid.

        :param url: The protein to search for
        :return: A list of the percentage composition of amino acids in the protein
        """
        if self.amino_acids is None:   
            logging.info("Loading Amino acids")
            self.amino_acids = self._parse_tsv(self._download_file(PROTEIN_COMPOSITION_URL))
        
        data = list(filter(lambda sublist: sublist[Peptide.SYSTEMATIC_ID.value] == protein_id, self.peptides))

        # There should only be one result! 
        if len(self.amino_acids) == 0:
            logging.info("No amino acid data found")
            return None
        elif len(self.amino_acids) > 1:
            logging.info("Multiple amino acid data found")
            return None
        else:

            return None

    def search_chromosome_features(self):
        """
        NOT used at present since this data should be relatively static.
        Keeping in case it is needed in the future.
        :return: 
        """
        if self.chromosome is None:   
            logging.info("Loading Chromosome features")
            self.chromosome = self._parse_gff3(self._download_file(ALL_CHROMOSOMES_GFF3_URL))

    def find_go_terms(self):
        """
        Load the GO terms from the Pombase website and parse them.
        They will then be added to the output file

        :return: 
        """
        if self.go_terms is None:   
            logging.info("Loading GO Terms")
            files = self._get_files_with_suffix(POMBASE_LATEST_URL, GO_TERMS_PATTERN)
            if len(files) == 1:
                self.go_terms = self._parse_gaf(self._download_and_decompress_gzip(files[0]))

        
    def find_fypo_terms(self):
        """
        Load the FYPO terms from the Pombase website and parse them.
        They will then be added to the output file

        :return: 
        """
        if self.fypo_terms is None:   
            logging.info("Loading FYPO Terms")
            files = self._get_files_with_suffix(POMBASE_LATEST_URL, FYPO_TERMS_PATTERN)
            for file in files:
                if re.search(r"pombase-\d{4}-\d{2}-\d{2}\.phaf\.gz", file):
                    self.fypo_terms = self._parse_phaf(self._download_and_decompress_gzip(file))


    def parse_original_AnGeLiDatabase(self, file_path='AnGeLiDatabase.txt') -> bool:
        """
        :param file_path: The path to the original AnGeLiDatabase.txt file.
        :return: True if the file was parsed successfully, False otherwise.
        """
        logging.info("Parsing the original AnGeLiDatabase.txt file")
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None

        self.original_file = self._parse_tsv(file_path)
        return True
    
    def build_GO_matrix(self) -> OrderedMatrix:
        """
        Builds a matrix of GO terms and their associated information.
        This is a placeholder for the actual implementation.
        """
        if self.go_terms is None:
            logging.error("GO terms not found. Cannot build GO matrix.")
            return None
        
        header_set = set()
        # Build the GO term headers
        for term in self.go_terms:
            header_set.add(term['GO_ID'])
            
        # Sort the headers
        header_list = sorted(header_set)
   
        go_matrix = OrderedMatrix()
        go_matrix.set_header(header_list)
        # Iterate over the GO terms, build a row and add it to the matrix
        row = []
        for term in self.go_terms:
            if len(row) == 0:
                row.append(term['DB_Object_ID'])
                row.append(term['GO_ID'])
            else:
                if term['DB_Object_ID'] != row[0]:
                    go_matrix.insert_row(row[0], row[1:])
                    row = []
                    row.append(term['DB_Object_ID'])
                    row.append(term['GO_ID'])
                else:
                    row.append(term['GO_ID'])
        # Add the last row
        if len(row) > 0:
            go_matrix.insert_row(row[0], row[1:])
            logging.info("GO matrix built successfully.")
        else:
            logging.error("Failed to build GO matrix. No data found.")
            return None
                
        # Return the matrix
        return go_matrix
 
    
    def build_FYPO_matrix(self):
        """
        Builds a matrix of FYPO terms and their associated information.
        This is a placeholder for the actual implementation.
        """
        if self.fypo_terms is None:
            logging.error("FYPO terms not found. Cannot build FYPO matrix.")
            return None
        
        header_set = set()
        # Build the GO term headers
        for term in self.fypo_terms:
            header_set.add(term['FYPO_ID'])
            
        # Sort the headers
        header_list = sorted(header_set)
            
        fypo_matrix = OrderedMatrix()
        fypo_matrix.set_header(header_list)
        # Iterate over the GO terms, build a row and add it to the matrix
        row = []
        for term in self.fypo_terms:
            if len(row) == 0:
                row.append(term['GENE_ID'])
                row.append(term['FYPO_ID'])
            else:
                if term['GENE_ID'] != row[0]:
                    fypo_matrix.insert_row(row[0], row[1:])
                    row = []
                    row.append(term['GENE_ID'])
                    row.append(term['FYPO_ID'])
                else:
                    row.append(term['FYPO_ID'])
        # Add the last row
        if len(row) > 0:
            fypo_matrix.insert_row(row[0], row[1:])
            logging.info("FYPO matrix built successfully.")
        else:
            logging.error("Failed to build FYPO matrix. No data found.")
            return None
                
        # Return the matrix
        return fypo_matrix
     
    def regenerate_file(self, output_path='AnGeLiDatabase.txt'):
        """
        Regenerates the AnGeLiDatabase.txt file with updated information.
        """
        logging.info("Regenerating the AnGeLiDatabase.txt file")
        if self.original_file is None:
            logging.error("Original file not parsed. Cannot regenerate.")
            return None
        
        # Load the data from the PomBase website
        self.find_go_terms()
        self.find_fypo_terms()
        
        # Build the matrix of GO terms and FYPO terms to replace the existing data 
        go_matrix = self.build_GO_matrix()
        fypo_matrix = self.build_FYPO_matrix()
        
        # Iterate over the original file and update the fields
        for i, row in enumerate(self.original_file):
            # Update the fields as needed
            # Example: row[0] = "Updated value"
            # You can use self.peptides, self.amino_acids, etc. to get the updated values
            row[4] = "Test"


        # Save the updated data to a new file
        with open(output_path, 'w') as f:
            for row in self.original_file:
                f.write('\t'.join(row) + '\n')
        
        logging.info("AnGeLiDatabase.txt file regenerated successfully.")

def main():
    """
    Reconstruct the AnGeLiDatabase.txt file 

    The method opens and parses the AnGeLiDatabase.txt file
    It then iterates over the various components and downloads the relevant sources and updates the fields.
    For GO and FYPO terms, the entire structure is rebuilt. See the README for more information.
    """
    logging.info("Starting the AnGeLi database reconstruction at %s", datetime.now())
    
    parser = argparse.ArgumentParser(description="Reconstruct the AnGeLi database")
    parser.add_argument("--path", type=str, default=None, help="Input file (incuding path)")
    parser.add_argument("--output_path", type=str, default=None, help="Output file (incuding path)")

    args = parser.parse_args()

    # Initialize the AnGeLi database
    db = AnGeLi()
    parsed = db.parse_original_AnGeLiDatabase(args.path)
    if not parsed:
        logging.error("Failed to parse the original AnGeLiDatabase.txt file.")
        return
    
    db.regenerate_file(args.output_path)
    
    logging.info("Finished AnGeLi database reconstruction at %s", datetime.now())

# Example usage
if __name__ == "__main__":
    main()