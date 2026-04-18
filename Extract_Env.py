import os
import csv
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

#1. Configuration

root_dir = "."
output_file = 'pdb_metadata_ext.csv'

def safe_get(mmcif_dict, tags):
	"""Searches through list of tags and returns first non-empty value."""
	if isinstance(tags, str):
		 tags = [tags]
	for tag in tags:
		val = mmcif_dict.get(tag)

		# MMCIF2Dict values are lists; filter out placeholders like '?' or '.'
		if val and isinstance(val, list):
			results = [str(v).strip() for v in val if v not in ['?','.','None']]
			if results:
				return ";". join(results)
	return"N/A"

fieldnames = ["Folder", "File", "PDB_ID", "Sequence", "Ligand_Name","Ligand_ID","Number_molec","Crystal_cond","pH","Growth_Temp","Diff_Temp"]

# Main Extraction and write code

count = 0 

with open(output_file,'w',newline='')as f:
	writer = csv.DictWriter(f, fieldnames = fieldnames)
	writer.writeheader()

	for root,_, files in os.walk(root_dir):
		for filename in files:
			if filename.lower().endswith(".cif"):
				path = os.path.join(root, filename)
				try:
					mmcif_dict = MMCIF2Dict(path)
					row = {
						'Folder': os.path.basename(root),
						'File': filename,	
						'PDB_ID':safe_get(mmcif_dict,'_entry.id'),
						'Sequence':safe_get(mmcif_dict,'_entity_poly.pdbx_seq_one_letter_code_can').replace("\n",""),
						'Ligand_Name':safe_get(mmcif_dict,'_pdbx_entity_nonpoly.name'),
						'Ligand_ID':safe_get(mmcif_dict,'_pdbx_entity_nonpoly.comp_id'),
						'Number_molec':safe_get(mmcif_dict,'_entity.pdbx_number_of_molecules'),
						'Crystal_cond':safe_get(mmcif_dict,'exptl_crystal_grow.pdbx_details'),
						'pH':safe_get(mmcif_dict,'_exptl_crystal_grow.pH'),
						'Growth_Temp':safe_get(mmcif_dict,'_exptl_crystal_grow.temp'),
						'Diff_Temp':safe_get(mmcif_dict,'_diffrn.ambient_temp')
						}
					writer.writerow(row)
					count += 1
					print(f"[{count}] Successfully Processed: {filename}")

				except Exception as e:
					print(f"Error processing {filename}:{e}")
print(f"\nResults saved to {output_file}")


