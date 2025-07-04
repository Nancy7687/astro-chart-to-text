# swiss_ephe_downloader.py (Final Verified Version)
import os
import requests
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# This path points to the persistent disk on Render
EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.data', 'ephe')

# Use a dedicated and verified GitHub mirror for file downloads
BASE_URL = "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/"

# Core file list needed for the application
FILES_TO_DOWNLOAD = [
    "sepl_18.se1", "semo_18.se1", "seas_18.se1", "sech_18.se1", "sefo_18.se1",
    "ast_433.eph", "ast_016.eph", "fixstars.cat", "sefstars.txt", "sweph.cat",
    "solarsys.cat"
]

def ensure_ephe_files_exist():
    """Checks for ephemeris files and downloads them if they are missing."""
    logging.info(f"Checking for ephemeris files in: {EPHE_DIR}")
    os.makedirs(EPHE_DIR, exist_ok=True)
    logging.info(f"Target directory '{EPHE_DIR}' is ready.")

    for filename in FILES_TO_DOWNLOAD:
        full_path = os.path.join(EPHE_DIR, filename)
        
        if os.path.exists(full_path):
            logging.info(f"File '{filename}' already exists. Skipping download.")
            continue
        
        url = BASE_URL + filename
        logging.info(f"File '{filename}' not found. Downloading from {url}...")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            
            with open(full_path, 'wb') as f, tqdm(
                desc=filename, total=total_size, unit='iB',
                unit_scale=True, unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)
            
            logging.info(f"Successfully downloaded '{filename}'.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading '{filename}': {e}")
            if os.path.exists(full_path):
                os.remove(full_path)
            raise RuntimeError(f"Failed to download required file {filename}. Application cannot start.") from e