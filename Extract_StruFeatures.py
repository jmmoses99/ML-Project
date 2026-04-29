import pandas as pd
import RNA
import itertools
from collections import Counter
import forgi.graph.bulge_graph as fgb  # For structural element counts

# Feature Calculation

#PDB Downloads by Category
def get_kmer_freqs(seq,k):
	bases = ['A','C','G','U']
	all_kmers = [''.join(p) for p in itertools.product(bases,repeat=k)]
	counts = Counter([seq[i:i+k] for i in range(len(seq)-k + 1)])
	total = max(sum(counts.values()), 1)
	return {f"{k}-mer_{kmer}": counts.get(kmer,0) / total for kmer in all_kmers}

def get_structural_counts(structure_dot_bracket):
	"""Counts structural elements using the forgi library."""

	try:
		bg = fgb.BulgeGraph.from_dotbracket(structure_dot_bracket)
		# forgi element types: 'h' = hairpin, 'i'=internal loop, 'm'=multiloop, 's'=stem,'f'=5
		counts = Counter(key[0] for key in bg.defines.keys())

		return {
		     'Hairpin_Count': counts.get('h',0),
		      'Bulge_Internal_Loop_Count': counts.get('i',0),
		      'Multiloop_Count': counts.get('m',0),
		      'Stem_Count': counts.get('s',0)
		}
	except:
		return {'Hairpin_Count': 0, 'Bulge_InternalLoop_Count': 0,'Multiloop_Count':0, 'Stem_Count': 0}

def analyze_row(row):

	seq = str(row['Sequence']).upper().replace('T','U')
	if not seq or seq == 'NAN' or seq== 'None':
		 return pd.Series(dtype='float64')

	# ViennaRNA Prediction

	fc = RNA.fold_compound(seq)
	ss, mfe = fc.mfe()

	# Sequence Features

	res = {

		'Length': len(seq),
		'GC_Content': round((seq.count('G') + seq.count('C')) / len (seq), 4),
		'MFE_kcal_mol': round(mfe,2),
		'Secondary_Structure': ss
	}

	# Structural Element Counts

	res.update(get_structural_counts(ss))

	# K-mer Frequencies (Dinucleotides and 3-mers)
	
	res.update(get_kmer_freqs(seq,2))
	res.update(get_kmer_freqs(seq,3))

	return pd.Series(res)

input_file ="pdb_metadata_ext.xlsx"
df = pd.read_excel(input_file, header = 1)
df.columns = df.columns.str.strip()
print(f"I found these columns: {df.columns.tolist()}")

print(f"Processing {len(df)} Sequence from {input_file}")

	# Process and  join to the right of existing columns

features_df = df.apply(analyze_row, axis=1)
final_df = pd.concat([df, features_df], axis = 1)

# Save

output_file = "riboswitch_PDBdata.xlsx"
final_df.to_excel(output_file, index=False)
print(f"Success! Features added to {output_file}")


