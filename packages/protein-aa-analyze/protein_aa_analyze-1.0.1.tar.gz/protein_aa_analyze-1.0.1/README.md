# Protein Amino Acids Analyzer

## Overview

The Protein Amino Acids Analyzer is a command-line application that takes a protein sequence in string format as input and returns a JSON object containing various insights about the sequence.

## Features

- Amino Acid Composition: Counts the number of each type of amino acid.
- Proportions: Calculates the proportion of each amino acid in the sequence.
- Molecular Weight: Calculates the total molecular weight of the protein.
- Isoelectric Point (pI): Estimates the isoelectric point of the protein.
- Hydrophobicity: Provides a measure of the overall hydrophobicity of the sequence.
- Detailed Residue Information: Provides molecular weight, isoelectric point, and hydrophobicity for each amino acid residue in the sequence.
- Amino Acid Composition Plot: Generates a plot of the amino acid composition.

## Implementation Steps

1. Input Handling: Accepts a protein sequence as input from the command line.
2. Amino Acid Composition Calculation: Uses a dictionary to count occurrences of each amino acid.
3. Proportions Calculation: Calculates the proportion of each amino acid in the sequence.
4. Molecular Weight Calculation: Sums the weights of individual amino acids using a predefined weight table.
5. Isoelectric Point Calculation: Uses an algorithm to estimate the pI based on the amino acid composition.
6. Hydrophobicity Calculation: Sums the hydrophobicity values of individual amino acids using a predefined scale (e.g., Kyte-Doolittle scale).
7. Residue Information Calculation: Calculates detailed information for each residue, including molecular weight, isoelectric point, and hydrophobicity.
8. Plot Generation: Generates a bar plot for the amino acid composition.

## Usage

### Prerequisites

Make sure you have Python 3.x installed on your machine.

### Installation

Clone this repository or download the `protein_aa_analyze.py` file directly.

Install the required dependencies:
pip install matplotlib

### Execution

To run the script, use the following command:
python protein_aa_analyze.py "PROTEIN_SEQUENCE" OUTPUT_FILE.json [--plot OUTPUT_PLOT.png]

- `PROTEIN_SEQUENCE`: The protein sequence to analyze (e.g., "ACDEFGHIKLMNPQRSTVWY").
- `OUTPUT_FILE.json`: The name of the JSON file where the results will be saved.
- `--plot OUTPUT_PLOT.png`: (Optional) The name of the plot file where the amino acid composition will be saved.

### Example
```
protein_aa_analyze.py "ACDEFGHIKLMNPQRSTVWY" output.json --plot composition_plot.png
```
This will analyze the sequence "ACDEFGHIKLMNPQRSTVWY", save the insights in a file named `output.json`, and save the amino acid composition plot in `composition_plot.png`.

## Output Format

The JSON output will have the following structure
```
{
  "sequence": "ACDEFGHIKLMNPQRSTVWY",
  "protein_molecular_weight": {
    "value": 2373.4,
    "unit": "Daltons",
    "reference": "https://www.sigmaaldrich.com/BE/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart"
  },
  "protein_isoelectric_point": {
    "value": 6.8,
    "unit": "pH",
    "reference": "https://www.sigmaaldrich.com/BE/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart"
  },
  "protein_hydrophobicity": {
    "value": -5.7,
    "unit": "Arbitrary units with The Kyte-Doolittle scale",
    "reference": "https://resources.qiagenbioinformatics.com/manuals/clcgenomicsworkbench/650/Hydrophobicity_scales.html#:~:text=The%20Kyte%2DDoolittle%20scale%20is,on%20the%20window%20size%20used."
  },
  "amino_acid_composition": {
    "A": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "H": 1, "I": 1, "K": 1, "L": 1,
    "M": 1, "N": 1, "P": 1, "Q": 1, "R": 1, "S": 1, "T": 1, "V": 1, "W": 1, "Y": 1
  },
  "amino_acid_proportions": {
    "A": 0.05, "C": 0.05, "D": 0.05, "E": 0.05, "F": 0.05, "G": 0.05, "H": 0.05, "I": 0.05,
    "K": 0.05, "L": 0.05, "M": 0.05, "N": 0.05, "P": 0.05, "Q": 0.05, "R": 0.05, "S": 0.05,
    "T": 0.05, "V": 0.05, "W": 0.05, "Y": 0.05
  },
  "residues": [
    {
      "position": 1,
      "index": 0,
      "amino_acid": "A",
      "molecular_weight": 89.1,
      "isoelectric_point": 0.345,
      "hydrophobicity": 1.8
    },
    {
      "position": 2,
      "index": 1,
      "amino_acid": "C",
      "molecular_weight": 121.2,
      "isoelectric_point": 0.345,
      "hydrophobicity": 2.5
    },
    ...
  ]
}
```

## Code Explanation

### ProteinAnalyzer Class

#### `__init__(self, sequence)`

- Initializes the protein sequence.
- Defines the amino acids to analyze.
- Initializes a counter for each amino acid to 0.
- Initializes a proportions dictionary for each amino acid to 0.

#### `calculate_amino_acid_composition(self)`

- Calculates the number of each type of amino acid in the sequence.

#### `calculate_amino_acid_proportions(self)`

- Calculates the proportion of each type of amino acid in the sequence and rounds it to 3 decimal places.

#### `calculate_molecular_weight(self)`

- Calculates the total molecular weight of the protein based on a predefined weight table and rounds it to 2 decimal places.

#### `calculate_isoelectric_point(self)`

- Estimates the isoelectric point (pI) of the protein using an algorithm based on the amino acid composition.

#### `calculate_hydrophobicity(self)`

- Provides a measure of the overall hydrophobicity of the sequence using a predefined scale (e.g., Kyte-Doolittle scale) and rounds it to 2 decimal places.

#### `calculate_residues_info(self)`

- Calculates detailed information for each residue, including molecular weight, isoelectric point, and hydrophobicity.

#### `plot_amino_acid_composition(self, output_file)`

- Generates a bar plot for the amino acid composition.

### `main()` Function

1. ArgumentParser: Uses `argparse` to handle command-line arguments.
   - `sequence`: The protein sequence to analyze.
   - `output`: The name of the JSON output file.
   - `--plot`: (Optional) The name of the plot file where the amino acid composition will be saved.

2. Sequence Analysis: Displays the received sequence and output file. Instantiates the `ProteinAnalyzer` class and calculates the insights. Displays the calculated insights.

3. Saving Results: Saves the insights in a JSON file. Displays a confirmation or error message. If the `--plot` argument is provided, generates and saves the plot.

## Example Output

If you run the script with the sequence "ACDEFGHIKLMNPQRSTVWY" and the file name `output.json`, the contents of the `output.json` file might look like this:
```
{
  "sequence": "ACDEFGHIKLMNPQRSTVWY",
  "protein_molecular_weight": {
    "value": 2373.4,
    "unit": "Daltons",
    "reference": "https://www.sigmaaldrich.com/BE/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart"
  },
  "protein_isoelectric_point": {
    "value": 6.8,
    "unit": "pH",
    "reference": "https://www.sigmaaldrich.com/BE/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart"
  },
  "protein_hydrophobicity": {
    "value": -5.7,
    "unit": "Arbitrary units with The Kyte-Doolittle scale",
    "reference": "https://resources.qiagenbioinformatics.com/manuals/clcgenomicsworkbench/650/Hydrophobicity_scales.html#:~:text=The%20Kyte%2DDoolittle%20scale%20is,on%20the%20window%20size%20used."
  },
  "amino_acid_composition": {
    "A": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "H": 1, "I": 1, "K": 1, "L": 1,
    "M": 1, "N": 1, "P": 1, "Q": 1, "R": 1, "S": 1, "T": 1, "V": 1, "W": 1, "Y": 1
  },
  "amino_acid_proportions": {
    "A": 0.05, "C": 0.05, "D": 0.05, "E": 0.05, "F": 0.05, "G": 0.05, "H": 0.05, "I": 0.05,
    "K": 0.05, "L": 0.05, "M": 0.05, "N": 0.05, "P": 0.05, "Q": 0.05, "R": 0.05, "S": 0.05,
    "T": 0.05, "V": 0.05, "W": 0.05, "Y": 0.05
  },
  "residues": [
    {
      "position": 1,
      "index": 0,
      "amino_acid": "A",
      "molecular_weight": 89.1,
      "isoelectric_point": 0.345,
      "hydrophobicity": 1.8
    },
    {
      "position": 2,
      "index": 1,
      "amino_acid": "C",
      "molecular_weight": 121.2,
      "isoelectric_point": 0.345,
      "hydrophobicity": 2.5
    },
    ...
  ]
}
```
## Code Explanation

### ProteinAnalyzer Class

#### `__init__(self, sequence)`

- Initializes the protein sequence.
- Defines the amino acids to analyze.
- Initializes a counter for each amino acid to 0.
- Initializes a proportions dictionary for each amino acid to 0.

#### `calculate_amino_acid_composition(self)`

- Calculates the number of each type of amino acid in the sequence.

#### `calculate_amino_acid_proportions(self)`

- Calculates the proportion of each type of amino acid in the sequence and rounds it to 3 decimal places.

#### `calculate_molecular_weight(self)`

- Calculates the total molecular weight of the protein based on a predefined weight table and rounds it to 2 decimal places.

#### `calculate_isoelectric_point(self)`

- Estimates the isoelectric point (pI) of the protein using an algorithm based on the amino acid composition.

#### `calculate_hydrophobicity(self)`

- Provides a measure of the overall hydrophobicity of the sequence using a predefined scale (e.g., Kyte-Doolittle scale) and rounds it to 2 decimal places.

#### `calculate_residues_info(self)`

- Calculates detailed information for each residue, including molecular weight, isoelectric point, and hydrophobicity.

#### `plot_amino_acid_composition(self, output_file)`

- Generates a bar plot for the amino acid composition.

### `main()` Function

1. ArgumentParser: Uses `argparse` to handle command-line arguments.
   - `sequence`: The protein sequence to analyze.
   - `output`: The name of the JSON output file.
   - `--plot`: (Optional) The name of the plot file where the amino acid composition will be saved.

2. Sequence Analysis: Displays the received sequence and output file. Instantiates the `ProteinAnalyzer` class and calculates the insights. Displays the calculated insights.

3. Saving Results: Saves the insights in a JSON file. Displays a confirmation or error message. If the `--plot` argument is provided, generates and saves the plot.

## Authors

This script was created by Iman Jouiad.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.