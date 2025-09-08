# Database for the AnGeLi tool

The AnGeLi tool on the Bahler Lab website http://bahlerweb.cs.ucl.ac.uk/cgi-bin/GLA/GLA_input is used to look up terms associated with gene lists e.g. FPYO or GO terms. 

It runs on a webserver controlled by the UCL CS department. 
<server details here>

The data is stored in a flat, tab-seperated value file with a txt extension.
<data file location details here>

# Prequisities
Python 3
    pip install gffutils requests

# Methodology 
Please refer to the code for exact implementation :)

This script focuses on updating the GO and FYPO terms associated with the genes. Thus, where a field is noted as not having a source (NA) then the value from the original file is used. Otherwise, the latest values are deemed to be correct. 

The script will open the original AnGeLiDatabase file and parse the content into a map.
The sources will then be downloaded into memory and parsed.
Values will be calculated (see code for particular details) and a new results map will be created
The script will output the new AnGeLiDatabase file.

# Data Mapping

The original file, AnGeLiDatabase.txt downloaded 18/12/2024, is stored alongside this README.md file. It is used as the original source for some values that are considered static. 

There is also a test list of genes in the file XXXXX. The output from the updated database can be compared to the original output to confirm that the changes are working as expected.

# Test cases

SPAC1F8.01
SPAC31A2.12
SPAC22F3.10c
SPAC1687.21
SPAC222.06
SPAC56F8.03
SPAC56F8.11
SPAC17A5.14
SPAC9G1.12
SPAC688.11
SPAC1142.04
SPAC25B8.02
SPAC144.03
SPAC17D4.01
SPAPYUG7.05
SPAC1B3.05
SPAC11E3.06
SPAC3G6.01
SPAC29B12.04
SPAC24B11.11c
SPAC806.02c
SPAC23G3.12c
SPAC10F6.03c
SPAC6F12.16c
SPAC9.03c
SPAC23H4.04
SPAC1399.03
SPAC17H9.04c
SPAC18G6.04c
SPAC4G9.20c
SPAC22H10.12c
SPAC19A8.04
SPAC4A8.07c
SPAC823.08c
SPAC1786.01c
SPAC3G9.08
SPAC3G9.06
SPAC3G9.05
SPAC6G9.02c
SPAC3A11.09
SPAC17G6.15c
SPAP7G5.02c
SPAC4H3.11c
SPAC27E2.03c
SPAC25G10.05c
SPAC29E6.10c
SPAC458.02c
SPAC4F10.09c
SPAC4F10.13c
SPAPB8E5.07c
SPAC29A4.20
SPAC26F1.07
SPAC14C4.12c
SPBC359.06
SPBC1683.05
SPBC660.16
SPBC800.11
SPBC106.15
SPBC1685.11
SPBC530.01
SPBC530.02
SPBC530.04
SPBC1709.06
SPBC19C2.08
SPBP16F5.06
SPBC1711.04
SPBC12D12.03
SPBC24C6.06
SPBC29A10.07
SPBC2G5.03
SPBC4F6.04
SPBC4F6.09
SPBC19C7.03
SPBC19C7.06
SPBP4H10.15
SPBC4C3.05c
SPBC405.01
SPBC20F10.01
SPBC17D11.05
SPBC17D1.05
SPBPB7E8.01
SPBC19F5.04
SPBC26H8.10
SPBC3F6.05
SPBC16A3.15c
SPBC839.05c
SPBC530.15c
SPBC36.02c
SPBC713.04c
SPBC1734.01c
SPBC651.01c
SPBC651.08c
SPBC27B12.12c
SPBC17A3.04c
SPBC19G7.08c
SPBC1826.01c
SPBC1703.03c
SPBC25H2.05
SPBC887.04c
SPBP8B7.20c
SPBC23E6.07c
SPBC26H8.08c
SPBC14F5.05c
SPBC1539.09c
SPCC1529.01
SPCC1183.07
SPCC895.06
SPCC550.11
SPCC645.13
SPCC285.17
SPCC1223.01
SPCC737.08
SPCC1739.14
SPCC1494.07
SPCC1672.05c
SPCC1672.11c
SPCC18B5.01c
SPCP25A2.02c
SPCC1281.06c
SPCC1450.16c

NOTES:

* The primary field of joining is the Systematic_ID e.g. SPAC1002.01
* Mapped value is fomrfrom source noted below, if there is no value then the original value is used.
* GO and FYPO fields are ordered, it has not been verified is this is a requirement, but for sake of simplicity this convention has been retained.
* For GO and FYPO we will scan the directory and fetch the latest file. This is because the date is embedded in the file name

Heading details
| Header Name | Description | Sample Value | 
| :---: | :---: | :---: |
| Short name | A shorthand name for the field | Mass |
| Long name | A slightly more descriptive name | Molecular weight (kDa) |
| Scale of measurement | What is the measure, typically this is a unit measurement or a flag | Metric OR Binary |
| Group | The type of the field | Protein Feature |
| Source | Where the data comes from| PomBase |
| Author | The author? | This will be copied from the "old" file | 
| Update | The date the data was last updated | 2025-01-05 | 
| Link | A link to the source or reference | http://www.ebi.ac.uk/QuickGO/GTerm?id=GO:0005826 | 


Field Details

| Shortfield | Longfield | Source | File | Position in File |
| :---: | :---: | :---: | :---: | :---: |
| Mass | Molecular weight (kDa)   | PomBase   | https://www.pombase.org/data/Protein_data/PeptideStats.tsv | col 2 |
| pI | Isoelectric point (predicted pH)   | PomBase   | https://www.pombase.org/data/Protein_data/PeptideStats.tsv | col 3 |
| Charge | Charge | PomBase   | https://www.pombase.org/data/Protein_data/PeptideStats.tsv | col 4 |
| NumResidues | Number of amino acids | PomBase   | https://www.pombase.org/data/Protein_data/PeptideStats.tsv | col 5 |
| G | Glycine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| A | Alanine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| L | Leucine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| M | Methionine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| F | Phenylalanine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| W | Tryptophan | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| K | Lysine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| Q | Glutamine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| E | Glutamic acid | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| S | Serine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| P | Proline | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| V | Valine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| I | Isoleucine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| C | Cysteine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| Y | Tyrosine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| H | Histidine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| R | Arginine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| N | Asparagine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| D | Aspartic acid | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| T | Threonine | PomBase   | https://www.pombase.org/data/Protein_data/aa_composition.tsv | col 5 |
| ncont | Nitrogen content | NA   | NA | NA |
| scont | Sulphur content | NA   | NA | NA |
| FoldIndex | Fold Index | NA   | NA | NA |
| NumberIntrons | Number of introns | NA   | NA | NA |
| AvergaeIntLength | Average intron length | NA   | NA | NA |
| FirstIntLength | Length of first intron | NA   | NA | NA |
| GCcontent | GC contents of first intron | NA   | NA | NA |
| IntronContaining | Intron-containing genes | NA   | NA | NA |
| Intronless | Intron-less genes | PomBase   | NA | NA |
| rRNA | rRNA | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| protein_coding | protein_coding | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| ncRNA | ncRNA | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| snoRNA | snoRNA | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3| col 5 |
| tRNA | tRNA | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| pseudogene | pseudogene | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| snRNA | snRNA | PomBase   | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| Chromosome1 | Chromosome 1 | PomBase | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| Chromosome2 | Chromosome 2 | PomBase | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| Chromosome3 | Chromosome 3 | PomBase | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| Mitochondria | Mitochondria | PomBase | https://www.pombase.org/data/releases/latest/gff/Schizosaccharomyces_pombe_all_chromosomes.gff3 | col 5 |
| Abs_telomere | Abs. distance from telomere | NA   | NA | NA |
| Abs_centromere | Abs. distance from centromere | NA   | NA | NA |
| Rel_telomere | Relative distance from telomere | NA   | NA | NA |
| Rel_centromere | Relative distance from centromere | NA   | NA | NA |
| GO:XXXXX | Ordered GO terms | PomBase   | https://pombase.org/data/releases/latest/pombase-<DATE>.gaf.gz | col 5 |
| FYPO:XXXX | Ordered FYPO terms | PomBase | https://pombase.org/data/releases/latest/pombase-<DATE>.phaf.gz | NA |