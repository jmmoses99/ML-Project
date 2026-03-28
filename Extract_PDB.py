#Code to download and organize the riboswitches files from PDB

import os

import requests

#PDB Downloads by Category

my_categories = {

	"PreQI_id" : ["3K1V", "3FU2","3GCA", "2L1V","3Q50", "3Q51", "6E1S", "6E1T", "6E1U",
	"6E1V", "6E1W","6VUH", "6VUI","7E9E","7E9I", "7REX"],



	"Adenine" : ["1Y26", "3IVN", "4TZY","4TZX","4LX5","4LX6","4XNR","5E54","5SWE","5SWD","5UZA","6VWV","6VWT"],


	"TPP_id" : ["2GDI","2CKY","2HOJ","2HOK","2HOL","2HOM","2HOO","2HOP", "3D2X","3D2V","3D2G","3K0J","4NYA","4NYD","4NYC","4NYB","4NYG","7TD7","7TDA","7TDB","7TDC","7TZR","7TZS","7TZT","7TZU","8F4O"],


	"FMN_id" : ["3F2Q","3F2T", "3F2W","3F2X","3F2Y","3F30","3F4E","3F4G","3F4H","2YIF","2YIE","5C45","5KX9","6BFB","6DN1","6DN2","6DN3","6WJR","6WJS"],


	"GlutamineI_id"  : ["5DDO","5DDP","5DDQ","5DDR"],

	"GlutamineII_id" : ["6QN3"],

	"THF_id" : ["3SUY","3SUX","3SUH","3SD3","4LVV","4LVZ","4LVW","4LVX","4LVY","4LW0","7KD1","6Q57"],


	"SAMI_id" : ["2GIS","3GX2","3GX3","3GX5","3GX6","3GX7","3IQN","3IQP","3IQR","4KQY","2YGH","2YDH","4AOB","4B5R","7EAF","7EAG"],

	"Fluoride_id" : ["3VRS","4EN5","4ENA","4ENC","5KH8"],

	"cdiGMPI_id" : ["3IRW","3IWN","3MUM","3MUR","3MUT","3MUV","3MXH","3UCU","3UCZ","3UD3","3UD4"]

}

# Loop through each category and its list of ids

for category, pdb_ids in my_categories.items():
	print(f"\n--Category:{category} ---")



# Create the folder if it does not exist

	os.makedirs(category,exist_ok = True)


# mmCIF download URL

	for pdb_id in pdb_ids:
		url = f"https://files.rcsb.org/download/{pdb_id.lower()}.cif"
		file_path = os.path.join(category,f"{pdb_id}.cif")

# Download the file

		try:
			r = requests.get(url)
			if r.status_code == 200:
				with open(file_path, "wb") as f:
					f.write(r.content)
				print(f"Successfully Downloaded {pdb_id}.cif to {category}/")
			else:
				print(f"FAILED {pdb_id}: Status {r.status_code}")

		except requests.exceptions.RequestException as e:

			print(f"Network error with {pdb_id}: {e}")


	print("Done! All files are organized in their folders")


