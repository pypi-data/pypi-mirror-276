import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DNAPROT_package')))

from DNAPROT_analysis import *

# test find_shine_dalgarno_function

def test_find_shine_dalgarno():
    sequences = [
        ("ATGAGGAGGTAG", 3),
        ("ATGCCCTAG", None),
        ("AGGAGGATG", 0),
        ("ATGAGGAGG", 3),
        ("GGAGGAGG", 2),
    ]
    
    for sequence, expected in sequences:
        result = find_shine_dalgarno(sequence)
        assert result == expected, f"Test failed: did not understand {sequence}, expected {expected}, got {result}"

# test cut_sequence function

def test_cut_sequence():
    sequences = [
        ("ATGAGGAGGTAG", ["TAG"]),
        ("ATGCCCTAG", []),
        ("AGGAGGATG", ["ATG"]),
        ("ATGAGGAGG", [""]),
        ("GGAGGAGGA", ["A"]),
        ("AGGAGGAGGAGGAGGAGG", ["", "", ""])]
    
    for sequence, expected_sections in sequences:
        result = cut_sequence(sequence)
        assert result == expected_sections, f"Test failed: did not understand {sequence}, expected {expected_sections}, got {result}"

# test translate_to_uppercase function

def test_translate_to_uppercase():
    test_cases = [
        ("atgc", "ATGC"),
        ("ATGC-", "ATGC-"),
        ("aTgC3", "ATGC3"),
        ("", "")]
    
    for sequence, expected in test_cases:
        result = translate_to_uppercase(sequence)
        assert result == expected, f"Test failed: did not understand {sequence}, expected {expected}, got {result}"

def test_filter_dna_sequence():
    test_cases = [
        ("ATGC", "ATGC"),
        ("ATGCK", "ATGC"),
        ("atgc", "ATGC"),
        ("atgcn", "ATGC"),
        ("", "")]
    
    for sequence, expected in test_cases:
        result = filter_dna_sequence(sequence)
        assert result == expected, f"Test failed: did not understand {sequence}, expected {expected}, got {result}"

# test for read_dna_sequence

def test_read_dna_sequence():
    test_files = [("test_file_1.txt", "AGGAGGATGAGGTCTGAT"), ("test_file_2.txt", "AGGGTCCCTAGATGGGCTAAAAGCGTTCGCTAAGT")]

    for file_name, expected_sequence in test_files:
        file_path = os.path.join("tests", file_name)
        result = read_dna_sequence(file_path)
        
        assert result == expected_sequence, f"Test failed: did not understand {file_name}, expected {expected_sequence}, got {result}"

# test for ReadShineDalgarnoFromFasta

def test_ReadShineDalgarnoFromFasta():
    test_files = [
        ("test_file_3.txt", 
         ["ATGCATGCATGCATGC", "CGTACGTACGTACGTA", "TGTGTGTGTGTGTGTG"])]

    # Iterate through test cases
    for file_name, expected_sequence in test_files:
        file_path = os.path.join("tests", file_name)
        result = ReadShineDalgarnoFromFasta(file_path)

        assert result == expected_sequence, f"Test failed: did not understand {file_name}, expected {expected_sequence}, got {result}"

# test read_genetic_code

def test_read_genetic_code():
    file_path = os.path.join('genetic_code.txt')

    expected_output = {
        'UUU': 'F',
        'UUC': 'F',
        'UUA': 'L',
        'UUG': 'L',
        'UCU': 'S',
        'UCC': 'S',
        'UCA': 'S',
        'UCG': 'S',
        'UAU': 'Y',
        'UAC': 'Y',
        'UAA': '*',
        'UAG': '*',
        'UGU': 'C',
        'UGC': 'C',
        'UGA': '*',
        'UGG': 'W',
        'CUU': 'L',
        'CUC': 'L',
        'CUA': 'L',
        'CUG': 'L',
        'CCU': 'P',
        'CCC': 'P',
        'CCA': 'P',
        'CCG': 'P',
        'CAU': 'H',
        'CAC': 'H',
        'CAA': 'Q',
        'CAG': 'Q',
        'CGU': 'R',
        'CGC': 'R',
        'CGA': 'R',
        'CGG': 'R',
        'AUU': 'I',
        'AUC': 'I',
        'AUA': 'I',
        'AUG': 'M',
        'ACU': 'T',
        'ACC': 'T',
        'ACA': 'T',
        'ACG': 'T',
        'AAU': 'N',
        'AAC': 'N',
        'AAA': 'K',
        'AAG': 'K',
        'AGU': 'S',
        'AGC': 'S',
        'AGA': 'R',
        'AGG': 'R',
        'GUU': 'V',
        'GUC': 'V',
        'GUA': 'V',
        'GUG': 'V',
        'GCU': 'A',
        'GCC': 'A',
        'GCA': 'A',
        'GCG': 'A',
        'GAU': 'D',
        'GAC': 'D',
        'GAA': 'E',
        'GAG': 'E',
        'GGU': 'G',
        'GGC': 'G',
        'GGA': 'G',
        'GGG': 'G'
    }

    result = read_genetic_code(file_path)

    assert result == expected_output

# test for transcribe_dna_to_rna

def test_transcribe_dna_to_rna():
    assert transcribe_dna_to_rna("ATCG") == "AUCG"
    assert transcribe_dna_to_rna("ATTGC") == "AUUGC"
    assert transcribe_dna_to_rna("GCTA") == "GCUA"

# test for find_start_codons_rna function

def test_find_start_codons_rna():
    assert find_start_codons_rna("AUGUUUAUG") == [0, 6]
    assert find_start_codons_rna("UUUAUGUUUGA") == [3]
    assert find_start_codons_rna("UAUGUUUA") == [1]

# test for translate_rna_to_protein

def test_translate_rna_to_protein():
    assert translate_rna_to_protein("UUUGAUGUCUCUAGUCGAUCGAUUGCUUU") == "MSLVDRLL"
    assert translate_rna_to_protein("UUUGAUGUCUCUAGCAGUCGAUCAUGUCCUGAUCCGU") == "MSLAVDHVLIR"

# Test for complementary_sequences function

def test_complementary_sequences():
    assert complementary_sequences("ATCG") == "TAGC"
    assert complementary_sequences("GCTA") == "CGAT"
    assert complementary_sequences("TTAAGC") == "AATTCG"

# Test for flip_rna_sequence function

def test_flip_rna_sequence():
    assert flip_rna_sequence("AUGUUUUAG") == "GAUUUUGUA"
    assert flip_rna_sequence("UUUGUUUGA") == "AGUUUGUUU"
    assert flip_rna_sequence("AUAGUUUA") == "AUUUGAUA"
    assert flip_rna_sequence("") == ""
    
# test for translate_rna_to_proteins_all_frames

def test_translate_rna_to_proteins_all_frames():
    assert translate_rna_to_proteins_all_frames("UGCUAGAUGUAGCGAAUGCUGAGUUUGC") == ['M', 'MLSL']
    assert translate_rna_to_proteins_all_frames("UUGAUGUUUUUGGGGCCCCAUGCCCGGGUAUUUGC") == ['MFLGPHARVF', 'MPGYL']

# test for translate_one_letter_to_three_letter_list

def test_translate_one_letter_to_three_letter_list():
    assert translate_one_letter_to_three_letter_list(["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) == ['Ala-Unknown-Cys-Asp-Glu-Phe-Gly-His-Ile-Unknown-Lys-Leu-Met-Asn-Unknown-Pro-Gln-Arg-Ser-Thr-Unknown-Val-Trp-Unknown-Tyr-Unknown']
    assert translate_one_letter_to_three_letter_list(["ACDEFGHIKLMNPQRSTVWY"]) == ['Ala-Cys-Asp-Glu-Phe-Gly-His-Ile-Lys-Leu-Met-Asn-Pro-Gln-Arg-Ser-Thr-Val-Trp-Tyr']
    assert translate_one_letter_to_three_letter_list(["CCCCCCCCC"]) == ['Cys-Cys-Cys-Cys-Cys-Cys-Cys-Cys-Cys']
    assert translate_one_letter_to_three_letter_list(["WWWWW"]) == ['Trp-Trp-Trp-Trp-Trp']

# test for calculate_hydrophobicity

def test_calculate_hydrophobicity():
    assert calculate_hydrophobicity("ACDEFGHIKLMNPQRSTVWY") == -9.8
    assert calculate_hydrophobicity("CCCCCCCCC") == 22.5
    assert calculate_hydrophobicity("WWWWW") == -4.5

# test for calculate_molecular_weight

def test_calculate_molecular_weight():
    assert calculate_molecular_weight("ACDEFGHIKLMNPQRSTVWY") == 2735.0
    assert calculate_molecular_weight("CCCCCCCCC") == 1089.0
    assert calculate_molecular_weight("WWWWW") == 1020.0

# test for calculate_configuration_likelihoods

def test_calculate_configuration_likelihoods():
    # Test case 1
    result1 = calculate_configuration_likelihoods("ACDEFGHIKLMNPQRSTVWY")
    expected_result1 = ('beta-sheet', 20.57, 20.57, 20.00, 19.83)
    rounded_result1 = (
        result1[0],
        round(result1[1], 2),
        round(result1[2], 2),
        round(result1[3], 2),
        round(result1[4], 2)
    )
    assert rounded_result1 == expected_result1

    # Test case 2
    result2 = calculate_configuration_likelihoods("CCCCCCCCC")
    expected_result2 = ('beta-sheet', 10.71, 10.71, 6.30, 10.71)
    rounded_result2 = (
        result2[0],
        round(result2[1], 2),
        round(result2[2], 2),
        round(result2[3], 2),
        round(result2[4], 2)
    )
    assert rounded_result2 == expected_result2

    # Test case 3
    result3 = calculate_configuration_likelihoods("WWWWW")
    expected_result3 = ('beta-sheet', 6.85, 6.85, 5.40, 4.80)
    rounded_result3 = (
        result3[0],
        round(result3[1], 2),
        round(result3[2], 2),
        round(result3[3], 2),
        round(result3[4], 2)
    )
    assert rounded_result3 == expected_result3

# test for calculate_retention_coefficient

def test_calculate_retention_coefficient():
    assert round(calculate_retention_coefficient("ACDEFGHIKLMNPQRSTVWY"), 2) == 50.4
    assert round(calculate_retention_coefficient("CCCCCCCCC"), 2) == -82.8
    assert round(calculate_retention_coefficient("WWWWW"), 2) == 81.5

# test for calculate_polarity_score

def test_calculate_polarity_score():
    assert round(calculate_polarity_score("ACDEFGHIKLMNPQRSTVWY"), 2) == 271.88
    assert round(calculate_polarity_score("CCCCCCCCC"), 2) == 13.32
    assert round(calculate_polarity_score("WWWWW"), 2) == 10.50

# for get_unique_folder_path and DNA_ToProtExcl_Analysis a test function cannot be made as it creates files and/or folders





