import pandas as pd
import requests
import time
from tqdm import tqdm

# --- SETTINGS ---
# This script reads and then overwrites the same file to keep your data in one place
FILE_NAME = "riboswitch_PDBdata.xlsx"

def fetch_graphql_batch(pdb_ids):
    """Fetches PDB metadata in batches using GraphQL to avoid connection blocks."""
    url = "https://rcsb.org"
    query = """
    query ($ids: [String!]!) {
      entries(entry_ids: $ids) {
        rcsb_id
        exptl_crystal_grow {
          pdbx_details
        }
      }
    }
    """
    variables = {"ids": pdb_ids}
    
    try:
        # Using a POST request with the GraphQL query
        r = requests.post(url, json={'query': query, 'variables': variables}, timeout=30)
        if r.status_code == 200:
            return r.json().get('data', {}).get('entries', [])
        return []
    except Exception:
        return []

def run_fetch():
    print(f"Loading {FILE_NAME} and preparing for batch fetch...")
    try:
        df = pd.read_excel(FILE_NAME, engine='openpyxl')
    except Exception as e:
        print(f"Error: Could not find or read {FILE_NAME}. {e}")
        return

    # Clean PDB IDs: Handles scientific notation and spaces correctly
    df['PDB_ID_Clean'] = df['PDB_ID'].astype(str).str.strip().str.upper().str[:4]
    
    # Identify unique, valid 4-character PDB IDs
    unique_ids = [id for id in df['PDB_ID_Clean'].unique() if len(id) == 4 and id.isalnum()]
    print(f"Found {len(unique_ids)} unique PDB IDs. Fetching details from RCSB...")

    details_map = {}
    chunk_size = 50 # Fetching 50 IDs at a time is the safest way to avoid 'Aborted' errors
    
    for i in range(0, len(unique_ids), chunk_size):
        chunk = unique_ids[i:i + chunk_size]
        print(f"Processing batch {i//chunk_size + 1}...")
        
        results = fetch_graphql_batch(chunk)
        
        if results:
            for entry in results:
                pdb_id = entry['rcsb_id']
                grow_data = entry.get('exptl_crystal_grow')
                
                # Safe extraction: pdbx_details can be nested or missing
                if isinstance(grow_data, list) and len(grow_data) > 0:
                    details = grow_data[0].get('pdbx_details', "Not Found")
                elif isinstance(grow_data, dict):
                    details = grow_data.get('pdbx_details', "Not Found")
                else:
                    details = "Not Found"
                    
                details_map[pdb_id] = details
        
        # Pause between batches to respect the server
        time.sleep(2)

    # Apply the new data back to the main dataframe
    df['Exp_Details'] = df['PDB_ID_Clean'].map(details_map).fillna("Fetch Failed")
    
    # Final save (Overwriting the original file as requested)
    df.to_excel(FILE_NAME, index=False, engine='openpyxl')
    print(f"\nSuccess! '{FILE_NAME}' has been updated with experimental details.")

# --- THE CALL (Required to make the script run) ---
if __name__ == "__main__":
    run_fetch()

