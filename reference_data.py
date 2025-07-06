
class ReferenceData:
    ROW_1 = [
        "Short name", "Mass", "pI", "Charge", "NumResidues", "G", "A", "L", "M", "F",
        "W", "K", "Q", "E", "S", "P", "V", "I", "C", "Y", "H", "R", "N", "D", "T",
        "ncont", "scont", "FoldIndex", "NumberIntrons", "AvergaeIntLength",
        "FirstIntLength", "GCcontent", "IntronContaining", "Intronless", "rRNA",
        "protein_coding", "ncRNA", "snoRNA", "tRNA", "pseudogene", "snRNA",
        "Chromosome1", "Chromosome2", "Chromosome3", "Mitochondria", "Abs_telomere",
        "Abs_centromere", "Rel_telomere", "Rel_centromere"
    ]

    ROW_2 = ["Long name","Molecular weight (kDa)","Isoelectric point (predicted pH)","Charge","Number of amino acids","Glycine","Alanine",
            "Leucine","Methionine","Phenylalanine","Tryptophan","Lysine","Glutamine","Glutamic acid","Serine","Proline","Valine","Isoleucine",
            "Cysteine","Tyrosine","Histidine","Arginine","Asparagine","Aspartic acid","Threonine","Nitrogen content","Sulphur content",
            "Fold Index","Number of introns","Average intron length","Length of first intron","GC contents of first intron","Intron-containing genes",
            "Intron-less genes","rRNA","protein_coding","ncRNA","snoRNA","tRNA","pseudogene","snRNA","Chromosome 1","Chromosome 2","Chromosome 3",
            "Mitochondria","Abs. distance from telomere","Abs. distance from centromere","Relative distance from telomere","Relative distance from centromere"]


    ROW_3 = ["Scale of measurement","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric",
            "Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric","Metric",
            "Metric","Metric","Metric","Binary","Binary","Binary","Binary","Binary","Binary","Binary","Binary","Binary","Binary","Binary","Binary",
            "Binary","Metric","Metric","Metric","Metric"]

    ROW_4 = ["Group","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features",
            "Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features",
            "Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features",
            "Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Protein Features","Gene Features",
            "Gene Features","Gene Features","Gene Features","Gene Features","Gene Features","Transcript Features","Transcript Features","Transcript Features",
            "Transcript Features","Transcript Features","Transcript Features","Transcript Features","Gene Features","Gene Features","Gene Features",
            "Gene Features","Gene Features","Gene Features","Gene Features","Gene Features"]

    ROW_5 = ["Source","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase",
            "Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase",
            "Prilusky J, Felder CE, Zeev-Ben-Mordehai T, Rydberg EH, Man O, Beckmann JS, Silman I, Sussman JL. 2005. FoldIndex: a simple tool to predict whether a given protein sequence is intrinsically unfolded. Bioinformatics 21(16): 3435-3438",
            "Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase",
            "Pombase","Pombase","Pombase","Pombase","Pombase","Pombase","Pombase"]

    ROW_6 = ["Author","DB","DB","DB","DB","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP",
            "DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB/VP","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB","DB",
            "DB","DB","DB","DB","DB","DB"]


    ROW_8 = ["Link","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org",
            "http://www.pombase.org","http://www.pombase.org","http://www.pombase.org","http://www.pombase.org"]


def main():
    """
    Run this to validate that the length of the rows is the same.
    NOTE: Row 7 is intentionally omitted as it is the current date
    """
    if len(ReferenceData.ROW_1) != len(ReferenceData.ROW_2):
        print("The lengths of ROW_1 and ROW_2 do not match.")
    else:
        print("The lengths of ROW_1 and ROW_2 match.")

    if len(ReferenceData.ROW_1) != len(ReferenceData.ROW_3):
        print("The lengths of ROW_1 and ROW_3 do not match.")
    else:
        print("The lengths of ROW_1 and ROW_3 match.")

    if len(ReferenceData.ROW_1) != len(ReferenceData.ROW_4):
        print("The lengths of ROW_1 and ROW_4 do not match.")
    else:
        print("The lengths of ROW_1 and ROW_4 match.")

    if len(ReferenceData.ROW_1) != len(ReferenceData.ROW_5):
        print("The lengths of ROW_1 and ROW_5 do not match.")
    else:
        print("The lengths of ROW_1 and ROW_5 match.")

    if len(ReferenceData.ROW_1) != len(ReferenceData.ROW_6):
        print("The lengths of ROW_1 and ROW_6 do not match.")
    else:
        print("The lengths of ROW_1 and ROW_6 match.")

    if len(ReferenceData.ROW_1) != len(ReferenceData.ROW_8):
        print(f"The lengths of ROW_1 {len(ReferenceData.ROW_1)} and ROW_8 {len(ReferenceData.ROW_8)} do not match.")
    else:
        print("The lengths of ROW_1 and ROW_8 match.")

# Example usage
if __name__ == "__main__":
    main()