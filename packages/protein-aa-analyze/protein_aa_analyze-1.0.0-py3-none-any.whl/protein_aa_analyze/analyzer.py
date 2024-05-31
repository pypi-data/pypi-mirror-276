import argparse
import json
import matplotlib.pyplot as plt

# Predefined weights and hydrophobicity scales
AMINO_ACID_WEIGHTS = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2, 'E': 147.1,
    'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2, 'L': 131.2, 'K': 146.2,
    'M': 149.2, 'F': 165.2, 'P': 115.1, 'S': 105.1, 'T': 119.1, 'W': 204.2,
    'Y': 181.2, 'V': 117.1
}

AMINO_ACID_HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5, 'E': -3.5,
    'Q': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9,
    'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8, 'T': -0.7, 'W': -0.9,
    'Y': -1.3, 'V': 4.2
}

class ProteinAnalyzer:
    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self.amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        self.composition = {aa: 0 for aa in self.amino_acids}
        self.proportions = {aa: 0 for aa in self.amino_acids}

    def calculate_amino_acid_composition(self):
        for aa in self.sequence:
            if aa in self.composition:
                self.composition[aa] += 1
        return self.composition
    
    def calculate_amino_acid_proportions(self):
        total_count = len(self.sequence)
        if total_count == 0:
            return self.proportions

        for aa in self.sequence:
            if aa in self.proportions:
                self.proportions[aa] += 1

        for aa in self.proportions:
            self.proportions[aa] /= total_count
            self.proportions[aa] = round(self.proportions[aa], 3)
        return self.proportions

    def calculate_molecular_weight(self):
        weight = 0
        for aa in self.sequence:
            if aa in AMINO_ACID_WEIGHTS:
                weight += AMINO_ACID_WEIGHTS[aa]
        return round(weight, 2)

    def calculate_isoelectric_point(self):
        # Simplified method for estimating isoelectric point
        acidic = ['D', 'E']
        basic = ['K', 'R', 'H']
        pI = 0.0
        count_acidic = sum([self.sequence.count(aa) for aa in acidic])
        count_basic = sum([self.sequence.count(aa) for aa in basic])
        if count_acidic + count_basic > 0:
            pI = 7.0 + 0.1 * (count_basic - count_acidic)
        return round(pI, 2)

    def calculate_hydrophobicity(self):
        hydrophobicity = 0
        for aa in self.sequence:
            if aa in AMINO_ACID_HYDROPHOBICITY:
                hydrophobicity += AMINO_ACID_HYDROPHOBICITY[aa]
        return round(hydrophobicity, 2)

    def calculate_residues_info(self):
        residues = []
        for index, aa in enumerate(self.sequence):
            if aa in AMINO_ACID_WEIGHTS:
                residue_info = {
                    "position": index + 1,
                    "index": index,
                    "amino_acid": aa,
                    "molecular_weight": round(AMINO_ACID_WEIGHTS[aa], 2),
                    "isoelectric_point": round(self.calculate_isoelectric_point() / len(self.sequence), 4),  # Simplified, should be specific per residue
                    "hydrophobicity": round(AMINO_ACID_HYDROPHOBICITY[aa], 4)
                }
                residues.append(residue_info)
        return residues

    def plot_amino_acid_composition(self, output_file):
        labels = list(self.composition.keys())
        counts = list(self.composition.values())

        plt.figure(figsize=(10, 5))
        plt.bar(labels, counts, color='blue')
        plt.xlabel('Amino Acids')
        plt.ylabel('Counts')
        plt.title('Amino Acid Composition')
        plt.savefig(output_file)
        plt.close()

def main():
    parser = argparse.ArgumentParser(description="Analyze a protein sequence.")
    parser.add_argument('sequence', type=str, help='Protein sequence string')
    parser.add_argument('output', type=str, help='Output JSON file')
    parser.add_argument('--plot', type=str, help='Output plot file (optional)')

    args = parser.parse_args()

    analyzer = ProteinAnalyzer(args.sequence)
    proportions = analyzer.calculate_amino_acid_proportions()
    composition = analyzer.calculate_amino_acid_composition()
    molecular_weight = analyzer.calculate_molecular_weight()
    isoelectric_point = analyzer.calculate_isoelectric_point()
    hydrophobicity = analyzer.calculate_hydrophobicity()
    residues_info = analyzer.calculate_residues_info()

    results = {
        "sequence": args.sequence,
        "protein_molecular_weight": {
            "value": molecular_weight,
            "unit": "Daltons",
            "reference": "https://www.sigmaaldrich.com/BE/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart"
        },
        "protein_isoelectric_point": {
            "value": isoelectric_point,
            "unit": "pH",
            "reference": "https://www.sigmaaldrich.com/BE/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart"
        },
        "protein_hydrophobicity": {
            "value": hydrophobicity,
            "unit": "Arbitrary units with The Kyte-Doolittle scale",
            "reference": "https://resources.qiagenbioinformatics.com/manuals/clcgenomicsworkbench/650/Hydrophobicity_scales.html#:~:text=The%20Kyte%2DDoolittle%20scale%20is,on%20the%20window%20size%20used."
        },
        "amino_acid_composition": composition,
        "amino_acid_proportions": proportions,
        "residues": residues_info
    }

    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)

    if args.plot:
        analyzer.plot_amino_acid_composition(args.plot)

    print(f"Results successfully written to {args.output}")
    if args.plot:
        print(f"Plot successfully saved to {args.plot}")

if __name__ == "__main__":
    main()