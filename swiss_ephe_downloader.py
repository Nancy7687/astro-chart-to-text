# swiss_ephe_downloader.py (Final Correct Version)
import os
import requests
from tqdm import tqdm
import logging

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 配置 ---
EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.data', 'ephe')
BASE_URL = "http://www.astro.com/ftp/swisseph/ephe/"

# ========================================================================
# FINAL & CORRECT FILE LIST
# ========================================================================
# 這是一個為標準占星盤（個人、行運等）精心挑選的列表。
# 它的大小適中，下載速度快，並且完整涵蓋您程式中定義的所有星體。
FILES_TO_DOWNLOAD = [
    # 主要行星 (太陽到冥王星) - 現代 (1800-2400 AD)
    "sepl_18.se1",
    
    # 月亮
    "semo_18.se1",
    
    # 主要小行星 (穀神, 智神, 婚神, 灶神)
    "seas_18.se1",
    
    # 凱龍星 (Chiron) - 現代占星常用
    "sech_18.se1",

    # 人龍 (Pholus) - 您定義的半人馬小行星
    "sefo_18.se1",
    
    # 您定義的特定小行星: 愛神 (433) 和 靈神 (16)
    "ast_433.eph",
    "ast_016.eph",
    
    # 核心系統檔案，提供恆星等數據
    "fixstars.cat",
    "sefstars.txt",
    "sweph.cat",
    "solarsys.cat"
]

def ensure_ephe_files_exist():
    """
    檢查星曆檔案是否存在，如果不存在則下載。
    """
    logging.info(f"檢查星曆檔案是否存在於: {EPHE_DIR}")
    os.makedirs(EPHE_DIR, exist_ok=True)
    logging.info(f"目標資料夾 '{EPHE_DIR}' 已確認存在。")

    for filename in FILES_TO_DOWNLOAD:
        # 處理包含子目錄的路徑，例如 'ast/file.se1'
        full_path = os.path.join(EPHE_DIR, filename)
        
        # 如果檔案路徑包含子目錄，請確保該子目錄存在
        if '/' in filename:
            sub_dir = os.path.dirname(full_path)
            os.makedirs(sub_dir, exist_ok=True)
            
        if os.path.exists(full_path):
            logging.info(f"檔案 '{filename}' 已存在，跳過下載。")
            continue
        
        url = BASE_URL + filename
        logging.info(f"檔案 '{filename}' 不存在，開始從 {url} 下載...")
        
        try:
            response = requests.get(url, stream=True, timeout=60) # 增加超時時間
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