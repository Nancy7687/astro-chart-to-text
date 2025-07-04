# swiss_ephe_downloader.py (Bulletproof Version)
import os
import requests
from tqdm import tqdm
import logging

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 配置 ---
EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.data', 'ephe')

# ========================================================================
# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# BULLETPROOF FIX: Using a hardcoded, full URL for every single file
# This eliminates all variables related to path concatenation.
# ========================================================================
FILES_TO_DOWNLOAD_URLS = [
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/sepl_18.se1",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/semo_18.se1",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/seas_18.se1",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/sech_18.se1",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/sefo_18.se1",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/ast_433.eph",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/ast_016.eph",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/fixstars.cat",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/sefstars.txt",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/sweph.cat",
    "https://raw.githubusercontent.com/gemini-astro-data/swisseph-files-core/main/solarsys.cat"
]
# ========================================================================
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

def ensure_ephe_files_exist():
    """
    檢查星曆檔案是否存在，如果不存在則下載。
    """
    logging.info(f"檢查星曆檔案是否存在於: {EPHE_DIR}")
    os.makedirs(EPHE_DIR, exist_ok=True)
    logging.info(f"目標資料夾 '{EPHE_DIR}' 已確認存在。")

    for url in FILES_TO_DOWNLOAD_URLS:
        # 從完整的 URL 中提取檔案名
        filename = url.split('/')[-1]
        full_path = os.path.join(EPHE_DIR, filename)
        
        if os.path.exists(full_path):
            logging.info(f"檔案 '{filename}' 已存在，跳過下載。")
            continue
        
        logging.info(f"檔案 '{filename}' 不存在，開始從絕對路徑 {url} 下載...")
        
        try:
            # 增加 User-Agent 標頭，模擬瀏覽器，避免被阻擋
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
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
            
            logging.info(f"檔案 '{filename}' 下載成功。")

        except requests.exceptions.RequestException as e:
            logging.error(f"下載檔案 '{filename}' 時發生錯誤: {e}")
            if os.path.exists(full_path):
                os.remove(full_path)
            raise RuntimeError(f"無法下載必要的星曆檔案 {filename}，應用程式無法啟動。") from e

if __name__ == '__main__':
    print("開始檢查並下載 Swiss Ephemeris 星曆檔案...")
    ensure_ephe_files_exist()
    print(f"\n所有必要的星曆檔案都已存在於 '{EPHE_DIR}'。")