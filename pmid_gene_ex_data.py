
import csv
import logging
from wsgiref import headers

logger = logging.getLogger(__name__)

class PMIDGeneExtractor:
    
    # The filename is fixed and this is a point in time reference 
    FILE_NAME = "PMID_40015273_gaf.tsv"
    
    def __init__(self):
        self.raw_data = []
        self.headers = []

    def __extract_genes(self):
        with open(self.FILE_NAME, 'r', newline='', encoding='utf-8') as file:
            tsv_reader = csv.reader(file, delimiter='\t')
            for row in tsv_reader:
                self.raw_data.append(row)

    #  short name:   Caffeine.and.Rapamycin.induced
    # Long name : Caffeine and Rapamycin induced
    # Scale: Binary
    # Group: Gene Expression
    # Source TORC1 signaling inhibition by rapamycin and caffeine affect lifespan, global gene expression, and cell proliferation of fission yeast
    # Author: DB
    # Update: 02/03/2020
    # Link: http://www.ncbi.nlm.nih.gov/pubmed/23551936
    def __build_headers(self):
        if not self.raw_data:
            return []
        
        for row in self.raw_data:
            column = []
            column.append(row[2])  # Short name
            column.append(row[2])  # Long name, we have nothing better
            column.append("Binary")  # Scale
            column.append("Gene Expression")  # Group
            column.append(row[6])  # Source
            column.append("DB")  # Author
            column.append(row[8])  # Update
            column.append(row[9])  # Link

            self.headers.append(column)
  

    def get_gene_data(self):
        if not self.raw_data:
            self.__extract_genes()
            
        # Convert each row in to the desired format 
        return self.raw_data
    
    