import os

# 1. Try different path variations
paths_to_test = [
    "./ML-Project",
    "ML-Project",
    ".",           # Checks the current folder
    ".."          # Checks one folder up
]

for p in paths_to_test:
    abs_p = os.path.abspath(p)
    exists = os.path.exists(abs_p)
    print(f"Testing: {p}")
    print(f"  Full path: {abs_p}")
    print(f"  Exists?    {exists}")
    
    if exists:
        # Check if there are any .cif files inside
        found_cifs = []
        for root, _, files in os.walk(abs_p):
            for f in files:
                if f.lower().endswith(".cif"):
                    found_cifs.append(f)
        
        print(f"  CIF files found: {len(found_cifs)}")
        if found_cifs:
            print(f"  Example file: {found_cifs[0]}")
    print("-" * 30)

