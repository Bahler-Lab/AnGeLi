import gzip
import requests
import gffutils
import io
import csv

# Pomebe base data URL, used as the common construct for other URLs
POMBE_BASE_URL = 'https://www.pombase.org/data'

# URLs for accessing data from the Pombase website
PEPTIDE_URL = POMBE_BASE_URL + "/Protein_data/PeptideStats.tsv"
PROTEIN_COMPOSITION_URL = POMBE_BASE_URL + "/Protein_data/aa_composition.tsv"
ALL_CHROMOSOMES_GFF3_URL = POMBE_BASE_URL + "/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3"


def download_file(url):
    """
    Downloads a file from a URL and returns the content as a BytesIO object.

    :param url: The URL of the file.
    :return: A BytesIO object containing the decompressed content.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Return the content as a BytesIO object
        return io.BytesIO(response.content)
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return None

def download_and_decompress_gzip(url):
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
    
def parse_tsv(file_obj):
    """
    Downloads a file from a URL and returns the content as a BytesIO object.

    :param url: The URL of the file.
    :return: A BytesIO object containing the decompressed content.
    """
    # Open the TSV file
    # Reset the BytesIO stream's position to the beginning if it was previously read
    file_obj.seek(0)
    
    # Create a CSV reader object with a tab delimiter
    reader = csv.DictReader(file_obj, delimiter='\t')
    return [row for row in reader]

def parse_gff3(file_obj):
    """
    Downloads a file from a URL and returns the content as a BytesIO object.

    :param url: The URL of the file.
    :return: A BytesIO object containing the decompressed content.
    """
    # Create a database from the GFF3 file object
    db = gffutils.create_db(file_obj, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)
    
    # Iterate through features in the database
    for feature in db.all_features():
        print(f"ID: {feature.id}, Type: {feature.featuretype}, Start: {feature.start}, End: {feature.end}, Strand: {feature.strand}")

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
    gff3_file_obj = download_file(ALL_CHROMOSOMES_GFF3_URL)
    parse_gff3(gff3_file_obj)