
def find_shine_dalgarno(sequence, shine_dalgarno="AGGAGG"):
    """Find the Shine-Dalgarno sequence in the given DNA sequence."""
    index = sequence.find(shine_dalgarno)
    if index != -1:
        return index
    else:
        return None



def cut_sequence(sequence, shine_dalgarno="AGGAGG"):
    """Cut the DNA sequence based on the Shine-Dalgarno sequence."""
    sections = []
    start_index = find_shine_dalgarno(sequence, shine_dalgarno)
    if start_index is not None:
        start_index += len(shine_dalgarno)
        while True:
            index = find_shine_dalgarno(sequence[start_index:], shine_dalgarno)
            if index is not None:
                sections.append(sequence[start_index:start_index + index])
                start_index += index + len(shine_dalgarno)
            else:
                sections.append(sequence[start_index:])
                break
    return sections



def translate_to_uppercase(sequence):
    """Translate the DNA sequence to uppercase."""
    return sequence.upper()




def filter_dna_sequence(sequence):
    """Filter out characters that are not 'A', 'T', 'C', or 'G'."""
    return ''.join(filter(lambda x: x in 'ATCG', sequence.upper()))




def read_dna_sequence(file_path):
    """Extract DNA sequence from fasta document"""
    with open(file_path, 'r') as file:
        sequence_lines = []

        for line in file:
            line = line.strip()
            if not line.startswith('>'):
                sequence_lines.append(line)
        sequence = ''.join(sequence_lines)
    return sequence


def ReadShineDalgarnoFromFasta(filename: str):
    """Read DNA sequence from the document and process it."""
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string")
    
    
    dna_sequence = read_dna_sequence(filename)
    
    
    dna_sequence = filter_dna_sequence(dna_sequence)
    sections = cut_sequence(dna_sequence)
    
    # Write resulting sections to a file
    with open("output.txt", "w") as file:
        for i, section in enumerate(sections):
            file.write(section + "\n")
            if i < len(sections) - 1:
                file.write("//\n") 
        file.write("//\n")
    
    print("Sections written to output.txt")
    sections = separate_sections("output.txt")
    return sections


if __name__ == "__main__":
    ReadShineDalgarnoFromFasta(filename)


def separate_sections(filename):
    """Read the file and separate sections of DNA into strings."""
    sections = []
    current_section = ""
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line == "//":
                sections.append(current_section)
                current_section = ""
            else:
                current_section += line
    return sections





def read_genetic_code(filename):
    """Reads the genetic code from a file."""
    genetic_code = {}
    with open(filename, 'r') as file:
        for line in file:
            codon, amino_acid = line.strip().split()
            genetic_code[codon] = amino_acid
    return genetic_code




def transcribe_dna_to_rna(dna_sequence):
    """ Transcribes a DNA sequence into an RNA sequence."""
    return dna_sequence.replace('T', 'U')
    



def find_start_codons_rna(rna_sequence):
    """ Finds start codons (AUG) in an RNA sequence."""
    start_codons = []
    for i in range(len(rna_sequence)):
        if rna_sequence[i:i+3] == "AUG":
            start_codons.append(i)
    if not start_codons:  # If start_codons is empty
        return -1
    return start_codons



def translate_rna_to_protein(rna_sequence):
    """Translates an RNA sequence into a protein sequence using a genetic code."""
    genetic_code = read_genetic_code("genetic_code.txt")
    start_index = find_start_codons_rna(rna_sequence)
    if start_index == -1:  # No start codon found
        return "Start codon not found"
    rna_sequence = rna_sequence[start_index[0]:]  # Use the first start index
    protein_sequence = ""
    for i in range(0, len(rna_sequence) - 2, 3):
        codon = rna_sequence[i:i+3]
        if codon in genetic_code:
            amino_acid = genetic_code[codon]
            if amino_acid == "*":
                break
            protein_sequence += amino_acid
        else:
            protein_sequence += "X"
    return protein_sequence




def complementary_sequences(dna_sequence):
    """Generates the complementary DNA sequence."""
    complementary_dna = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    comp_dna_sequence = ''.join(complementary_dna[base] for base in dna_sequence)
    return comp_dna_sequence





def flip_rna_sequence(rna_sequence):
    """ Reverses the RNA sequence."""
    return rna_sequence[::-1]





def translate_rna_to_proteins_all_frames(rna_sequence):
    """Translates RNA sequences into protein sequences in all reading frames."""
    proteins = []
    for start_index in find_start_codons_rna(rna_sequence):
        protein_sequence = translate_rna_to_protein(rna_sequence[start_index:])
        proteins.append(protein_sequence)
    return proteins





def translate_one_letter_to_three_letter_list(one_letter_sequences):
    """Converts one-letter amino acid sequences to three-letter codes."""
    three_letter_code = {
        "A": "Ala", "C": "Cys", "D": "Asp", "E": "Glu",
        "F": "Phe", "G": "Gly", "H": "His", "I": "Ile",
        "K": "Lys", "L": "Leu", "M": "Met", "N": "Asn",
        "P": "Pro", "Q": "Gln", "R": "Arg", "S": "Ser",
        "T": "Thr", "V": "Val", "W": "Trp", "Y": "Tyr",
        "*": "Stop"
    }
    three_letter_sequences = []
    for one_letter_sequence in one_letter_sequences:
        three_letter_sequence = [three_letter_code.get(aa, "Unknown") for aa in one_letter_sequence]
        three_letter_sequences.append("-".join(three_letter_sequence))
    return three_letter_sequences










def calculate_hydrophobicity(protein: str) -> float:
    """Calculates the hydrophobicity score of a protein sequence."""
    hydrophobicity_scale = {
        'A': 1.800,  # Alanine
        'R': -4.500, # Arginine
        'N': -3.500, # Asparagine
        'D': -3.500, # Aspartic Acid
        'C': 2.500,  # Cysteine
        'Q': -3.500, # Glutamine
        'E': -3.500, # Glutamic Acid
        'G': -0.400, # Glycine
        'H': -3.200, # Histidine
        'I': 4.500,  # Isoleucine
        'L': 3.800,  # Leucine
        'K': -3.900, # Lysine
        'M': 1.900,  # Methionine
        'F': 2.800,  # Phenylalanine
        'P': -1.600, # Proline
        'S': -0.800, # Serine
        'T': -0.700, # Threonine
        'W': -0.900, # Tryptophan
        'Y': -1.300, # Tyrosine
        'V': 4.200   # Valine
    }
    
    total_score = 0.0
    for amino_acid in protein:
        if amino_acid in hydrophobicity_scale:
            total_score += hydrophobicity_scale[amino_acid]
        else:
            raise ValueError(f"Invalid amino acid: {amino_acid}")
    
    return total_score






def calculate_molecular_weight(protein: str) -> float:
    """Calculates the molecular weight of a protein sequence."""
    molecular_weights = {
        'A': 89.000,  # Alanine
        'R': 174.000, # Arginine
        'N': 132.000, # Asparagine
        'D': 133.000, # Aspartic Acid
        'C': 121.000, # Cysteine
        'Q': 146.000, # Glutamine
        'E': 147.000, # Glutamic Acid
        'G': 75.000,  # Glycine
        'H': 155.000, # Histidine
        'I': 131.000, # Isoleucine
        'L': 131.000, # Leucine
        'K': 146.000, # Lysine
        'M': 149.000, # Methionine
        'F': 165.000, # Phenylalanine
        'P': 115.000, # Proline
        'S': 105.000, # Serine
        'T': 119.000, # Threonine
        'W': 204.000, # Tryptophan
        'Y': 181.000, # Tyrosine
        'V': 117.000  # Valine
    }
    
    total_weight = 0.0
    for amino_acid in protein:
        if amino_acid in molecular_weights:
            total_weight += molecular_weights[amino_acid]
        else:
            raise ValueError(f"Invalid amino acid: {amino_acid}")
    
    return total_weight




def calculate_configuration_likelihoods(protein: str):
    """Calculates the likelihood of different structural configurations for a protein."""
    beta_sheet = {
        'A': 0.830, 'R': 0.930, 'N': 0.890, 'D': 0.540, 'C': 1.190, 'Q': 1.100, 'E': 0.370,
        'G': 0.750, 'H': 0.870, 'I': 1.600, 'L': 1.300, 'K': 0.740, 'M': 1.050, 'F': 1.380,
        'P': 0.550, 'S': 0.750, 'T': 1.190, 'W': 1.370, 'Y': 1.470, 'V': 1.700
    }

    alpha_helix = {
        'A': 1.420, 'R': 0.980, 'N': 0.670, 'D': 1.010, 'C': 0.700, 'Q': 1.110, 'E': 1.510,
        'G': 0.570, 'H': 1.000, 'I': 1.080, 'L': 1.210, 'K': 1.160, 'M': 1.450, 'F': 1.130,
        'P': 0.570, 'S': 0.770, 'T': 0.830, 'W': 1.080, 'Y': 0.690, 'V': 1.060
    }

    beta_turn = {
        'A': 0.660, 'R': 0.950, 'N': 1.560, 'D': 1.460, 'C': 1.190, 'Q': 0.980, 'E': 0.740,
        'G': 1.560, 'H': 0.950, 'I': 0.470, 'L': 0.590, 'K': 1.010, 'M': 0.600, 'F': 0.600,
        'P': 1.520, 'S': 1.430, 'T': 0.960, 'W': 0.960, 'Y': 1.140, 'V': 0.500
    }

    def calculate_score(protein, score_dict):
        total_score = 0.0
        for amino_acid in protein:
            if amino_acid in score_dict:
                total_score += score_dict[amino_acid]
            else:
                raise ValueError(f"Invalid amino acid: {amino_acid}")
        return total_score

    beta_sheet_score = calculate_score(protein, beta_sheet)
    alpha_helix_score = calculate_score(protein, alpha_helix)
    beta_turn_score = calculate_score(protein, beta_turn)

    scores = {
        'beta-sheet': beta_sheet_score,
        'alpha-helix': alpha_helix_score,
        'beta-turn': beta_turn_score
    }

    highest_likelihood = max(scores, key=scores.get)
    highest_score = scores[highest_likelihood]

    return highest_likelihood, highest_score, beta_sheet_score, alpha_helix_score, beta_turn_score






def calculate_retention_coefficient(protein: str) -> float:
    """Calculates the retention coefficient of a protein sequence."""
    retention_coefficients = {
        'A': 7.300,   # Alanine
        'R': -3.600,  # Arginine
        'N': -5.700,  # Asparagine
        'D': -2.900,  # Aspartic Acid
        'C': -9.200,  # Cysteine
        'Q': -0.300,  # Glutamine
        'E': -7.100,  # Glutamic Acid
        'G': -1.200,  # Glycine
        'H': -2.100,  # Histidine
        'I': 6.600,   # Isoleucine
        'L': 20.000,  # Leucine
        'K': -3.700,  # Lysine
        'M': 5.600,   # Methionine
        'F': 19.200,  # Phenylalanine
        'P': 5.100,   # Proline
        'S': -4.100,  # Serine
        'T': 0.800,   # Threonine
        'W': 16.300,  # Tryptophan
        'Y': 5.900,   # Tyrosine
        'V': 3.500    # Valine
    }
    
    total_retention = 0.0
    for amino_acid in protein:
        if amino_acid in retention_coefficients:
            total_retention += retention_coefficients[amino_acid]
        else:
            raise ValueError(f"Invalid amino acid: {amino_acid}")
    
    return total_retention





def calculate_polarity_score(protein: str) -> float:
    """Calculates the polarity score of a protein sequence."""
    polarity_scores = {
        'A': 0.000,   # Alanine
        'R': 52.000,  # Arginine
        'N': 3.380,   # Asparagine
        'D': 49.700,  # Aspartic Acid
        'C': 1.480,   # Cysteine
        'Q': 3.530,   # Glutamine
        'E': 49.900,  # Glutamic Acid
        'G': 0.000,   # Glycine
        'H': 51.600,  # Histidine
        'I': 0.130,   # Isoleucine
        'L': 0.130,   # Leucine
        'K': 49.500,  # Lysine
        'M': 1.430,   # Methionine
        'F': 0.350,   # Phenylalanine
        'P': 1.580,   # Proline
        'S': 1.670,   # Serine
        'T': 1.660,   # Threonine
        'W': 2.100,   # Tryptophan
        'Y': 1.610,   # Tyrosine
        'V': 0.130    # Valine
    }
    
    total_polarity = 0.0
    for amino_acid in protein:
        if amino_acid in polarity_scores:
            total_polarity += polarity_scores[amino_acid]
        else:
            raise ValueError(f"Invalid amino acid: {amino_acid}")
    
    return total_polarity






import os
import pandas as pd

def get_unique_folder_path(base_folder):
    """
    This function takes a base folder path and returns a unique folder path by adding a suffix if the folder already exists.
    """
    counter = 1
    unique_folder = base_folder
    while os.path.exists(unique_folder):
        unique_folder = f"{base_folder}({counter})"
        counter += 1
    return unique_folder

def DNA_ToProtExcl_Analysis(sections, section_number=None, output_folder=None):
    """Performs DNA to protein transcription, translation and protein properties analysis. It then saves the results in Excel files."""
    if section_number is None:
        section_number = 1
    if output_folder is None:
        base_output_folder = os.path.join(os.getcwd(), "DNAtoPROT_results")
        output_folder = get_unique_folder_path(base_output_folder)
        os.makedirs(output_folder)

    # If sections is a list of DNA sequences
    if isinstance(sections, list):
        for i in range(len(sections)):
            dna_sequence = sections[i]
            DNA_ToProtExcl_Analysis(dna_sequence, i + 1, output_folder)
    else:
        dna_sequence = sections
        rna_sequence = transcribe_dna_to_rna(dna_sequence)

        # Translate RNA to protein with start codon "AUG" for 5'3'
        protein_sequence_rna53 = translate_rna_to_proteins_all_frames(rna_sequence)
        
        # Find the complementary of the DNA and RNA sequences
        dna_sequence35 = complementary_sequences(dna_sequence)
        rna_sequence35 = transcribe_dna_to_rna(dna_sequence35)
        rna_sequence35_inv = flip_rna_sequence(rna_sequence35)
        
        # Translate RNA to protein with start codon "AUG" for 5'3'
        protein_sequence_rna35 = translate_rna_to_proteins_all_frames(rna_sequence35_inv)
        
        # Translating one-letter symbol amino acid into three
        protein_sequence_3letters53 = translate_one_letter_to_three_letter_list(protein_sequence_rna53)
        protein_sequence_3letters35 = translate_one_letter_to_three_letter_list(protein_sequence_rna35)

        # Compute additional properties
        hydrophobicity_53 = [calculate_hydrophobicity(protein) for protein in protein_sequence_rna53]
        molecular_weight_53 = [calculate_molecular_weight(protein) for protein in protein_sequence_rna53]
        retention_coefficient_53 = [calculate_retention_coefficient(protein) for protein in protein_sequence_rna53]
        config_likelihoods_53 = [calculate_configuration_likelihoods(protein) for protein in protein_sequence_rna53]
        polarity_53 = [calculate_polarity_score(protein) for protein in protein_sequence_rna53]

        hydrophobicity_35 = [calculate_hydrophobicity(protein) for protein in protein_sequence_rna35]
        molecular_weight_35 = [calculate_molecular_weight(protein) for protein in protein_sequence_rna35]
        retention_coefficient_35 = [calculate_retention_coefficient(protein) for protein in protein_sequence_rna35]
        config_likelihoods_35 = [calculate_configuration_likelihoods(protein) for protein in protein_sequence_rna35]
        polarity_35 = [calculate_polarity_score(protein) for protein in protein_sequence_rna35]

        # Create DataFrames for displaying protein sequences
        df53 = pd.DataFrame({
            "Frame 1L (5'->3')": protein_sequence_rna53,
            "Frame 3L (5'->3')": protein_sequence_3letters53,
            "Hydrophobicity": hydrophobicity_53,
            "Molecular Weight": molecular_weight_53,
            "Retention Coefficient": retention_coefficient_53,
            "beta-sheet score": [beta_sheet for _, _, beta_sheet, _, _ in config_likelihoods_53],
            "alpha-helix score": [alpha_helix for _, _, _, alpha_helix, _ in config_likelihoods_53],
            "beta-turn score": [beta_turn for _, _, _, _, beta_turn in config_likelihoods_53],
            "Most probable configuration": [likelihood for likelihood, _, _, _, _ in config_likelihoods_53],
            "polarity": polarity_53
        })

        df35 = pd.DataFrame({
            "Frame 1L (3'->5')": protein_sequence_rna35,
            "Frame 3L (3'->5')": protein_sequence_3letters35,
            "Hydrophobicity": hydrophobicity_35,
            "Molecular Weight": molecular_weight_35,
            "Retention Coefficient": retention_coefficient_35,
            "beta-sheet score": [beta_sheet for _, _, beta_sheet, _, _ in config_likelihoods_35],
            "alpha-helix score": [alpha_helix for _, _, _, alpha_helix, _ in config_likelihoods_35],
            "beta-turn score": [beta_turn for _, _, _, _, beta_turn in config_likelihoods_35],
            "Most probable configuration": [likelihood for likelihood, _, _, _, _ in config_likelihoods_35],
            "polarity": polarity_35
        })

        # Create output file path
        output_file = os.path.join(output_folder, f"section_{section_number}.xlsx")
        
        with pd.ExcelWriter(output_file) as writer:
            df53.to_excel(writer, sheet_name="Frame (5'->3')")
            df35.to_excel(writer, sheet_name="Frame (3'->5')")

if __name__ == "__main__":
    DNA_ToProtExcl_Analysis(sections)