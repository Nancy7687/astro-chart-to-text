# swiss_ephe_downloader.py
import os
import requests
from tqdm import tqdm
import logging

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 配置 ---
# Render 平台上用於儲存星曆檔案的建議路徑
# os.path.dirname(__file__) 會取得目前檔案所在的目錄
# '..' 往上一層, '.data/ephe' 是我們在 Render 上掛載的磁碟路徑
# 為了本地測試和部署的兼容性，我們這樣設定
# 當在本地運行時，它會在 astrology-app/.data/ephe/
# 當在 Render 運行時，它會正確地指向掛載的磁碟
EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.data', 'ephe')

# Swiss Ephemeris FTP 站點的 HTTP URL
BASE_URL = "http://www.astro.com/ftp/swisseph/ephe/"

# 需要下載的星曆檔案列表 (基礎版，可根據需要擴充)
# sepl_18.se1: 行星 (1800-2400 AD)
# semo_18.se1: 月亮 (1800-2400 AD)
# seas_18.se1: 主要小行星 (1800-2400 AD)
# sefstars.txt: 恆星資料
# fixstars.cat: 恆星目錄
REQUIRED_FILES = [

'all_long.txt',
'all_short.txt',
'ast0/se00016s.se1',
'ast0/se00393s.se1',
'ast0/se00433s.se1',
'list_long.txt',
'list_short.txt',
'plmolist.txt',
'sat/plmolist.txt',
'sat/sepm9401.se1',
'sat/sepm9402.se1',
'sat/sepm9501.se1',
'sat/sepm9502.se1',
'sat/sepm9503.se1',
'sat/sepm9504.se1',
'sat/sepm9599.se1',
'sat/sepm9601.se1',
'sat/sepm9602.se1',
'sat/sepm9603.se1',
'sat/sepm9604.se1',
'sat/sepm9605.se1',
'sat/sepm9606.se1',
'sat/sepm9607.se1',
'sat/sepm9608.se1',
'sat/sepm9699.se1',
'sat/sepm9701.se1',
'sat/sepm9702.se1',
'sat/sepm9703.se1',
'sat/sepm9704.se1',
'sat/sepm9705.se1',
'sat/sepm9799.se1',
'sat/sepm9801.se1',
'sat/sepm9802.se1',
'sat/sepm9808.se1',
'sat/sepm9899.se1',
'sat/sepm9901.se1',
'sat/sepm9902.se1',
'sat/sepm9903.se1',
'sat/sepm9904.se1',
'sat/sepm9905.se1',
'sat/sepm9999.se1',
'se00016s.se1',
'se00393s.se1',
'se00433s.se1',
'seasm06.se1',
'seasm102.se1',
'seasm108.se1',
'seasm114.se1',
'seasm12.se1',
'seasm120.se1',
'seasm126.se1',
'seasm132.se1',
'seasm18.se1',
'seasm24.se1',
'seasm30.se1',
'seasm36.se1',
'seasm42.se1',
'seasm48.se1',
'seasm54.se1',
'seasm60.se1',
'seasm66.se1',
'seasm72.se1',
'seasm78.se1',
'seasm84.se1',
'seasm90.se1',
'seasm96.se1',
'seasnam.txt',
'seas_00.se1',
'seas_06.se1',
'seas_102.se1',
'seas_108.se1',
'seas_114.se1',
'seas_12.se1',
'seas_120.se1',
'seas_126.se1',
'seas_132.se1',
'seas_138.se1',
'seas_144.se1',
'seas_150.se1',
'seas_156.se1',
'seas_162.se1',
'seas_18.se1',
'seas_24.se1',
'seas_30.se1',
'seas_36.se1',
'seas_42.se1',
'seas_48.se1',
'seas_54.se1',
'seas_60.se1',
'seas_66.se1',
'seas_72.se1',
'seas_78.se1',
'seas_84.se1',
'seas_90.se1',
'seas_96.se1',
'sefstars.txt',
'semom06.se1',
'semom102.se1',
'semom108.se1',
'semom114.se1',
'semom12.se1',
'semom120.se1',
'semom126.se1',
'semom132.se1',
'semom18.se1',
'semom24.se1',
'semom30.se1',
'semom36.se1',
'semom42.se1',
'semom48.se1',
'semom54.se1',
'semom60.se1',
'semom66.se1',
'semom72.se1',
'semom78.se1',
'semom84.se1',
'semom90.se1',
'semom96.se1',
'semo_00.se1',
'semo_06.se1',
'semo_102.se1',
'semo_108.se1',
'semo_114.se1',
'semo_12.se1',
'semo_120.se1',
'semo_126.se1',
'semo_132.se1',
'semo_138.se1',
'semo_144.se1',
'semo_150.se1',
'semo_156.se1',
'semo_162.se1',
'semo_18.se1',
'semo_24.se1',
'semo_30.se1',
'semo_36.se1',
'semo_42.se1',
'semo_48.se1',
'semo_54.se1',
'semo_60.se1',
'semo_66.se1',
'semo_72.se1',
'semo_78.se1',
'semo_84.se1',
'semo_90.se1',
'semo_96.se1',
'seorbel.txt',
'seplm06.se1',
'seplm102.se1',
'seplm108.se1',
'seplm114.se1',
'seplm12.se1',
'seplm120.se1',
'seplm126.se1',
'seplm132.se1',
'seplm18.se1',
'seplm24.se1',
'seplm30.se1',
'seplm36.se1',
'seplm42.se1',
'seplm48.se1',
'seplm54.se1',
'seplm60.se1',
'seplm66.se1',
'seplm72.se1',
'seplm78.se1',
'seplm84.se1',
'seplm90.se1',
'seplm96.se1',
'sepl_00.se1',
'sepl_06.se1',
'sepl_102.se1',
'sepl_108.se1',
'sepl_114.se1',
'sepl_12.se1',
'sepl_120.se1',
'sepl_126.se1',
'sepl_132.se1',
'sepl_138.se1',
'sepl_144.se1',
'sepl_150.se1',
'sepl_156.se1',
'sepl_162.se1',
'sepl_18.se1',
'sepl_24.se1',
'sepl_30.se1',
'sepl_36.se1',
'sepl_42.se1',
'sepl_48.se1',
'sepl_54.se1',
'sepl_60.se1',
'sepl_66.se1',
'sepl_72.se1',
'sepl_78.se1',
'sepl_84.se1',
'sepl_90.se1',
'sepl_96.se1',
'sepm9401.se1',
'sepm9402.se1',
'sepm9501.se1',
'sepm9502.se1',
'sepm9503.se1',
'sepm9504.se1',
'sepm9599.se1',
'sepm9601.se1',
'sepm9602.se1',
'sepm9603.se1',
'sepm9604.se1',
'sepm9605.se1',
'sepm9606.se1',
'sepm9607.se1',
'sepm9608.se1',
'sepm9699.se1',
'sepm9701.se1',
'sepm9702.se1',
'sepm9703.se1',
'sepm9704.se1',
'sepm9705.se1',
'sepm9799.se1',
'sepm9801.se1',
'sepm9802.se1',
'sepm9808.se1',
'sepm9899.se1',
'sepm9901.se1',
'sepm9902.se1',
'sepm9903.se1',
'sepm9904.se1',
'sepm9905.se1',
'sepm9999.se1',

    # --- 請在這裡繼續加入您需要的其他檔案名，例如凱龍星 'sech_18.se1' ---

]

def ensure_ephe_files_exist():
    """
    檢查星曆檔案是否存在，如果不存在則下載。
    這個函數是冪等的 (idempotent)，重複執行不會造成問題。
    """
    logging.info(f"檢查星曆檔案是否存在於: {EPHE_DIR}")
    
    # 1. 確保目標資料夾存在
    os.makedirs(EPHE_DIR, exist_ok=True)
    logging.info(f"目標資料夾 '{EPHE_DIR}' 已確認存在。")

    # 2. 遍歷檔案列表，檢查並下載
    for filename in FILES_TO_DOWNLOAD:
        file_path = os.path.join(EPHE_DIR, filename)
        
        if os.path.exists(file_path):
            logging.info(f"檔案 '{filename}' 已存在，跳過下載。")
            continue
        
        # 檔案不存在，開始下載
        url = BASE_URL + filename
        logging.info(f"檔案 '{filename}' 不存在，開始從 {url} 下載...")
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()  # 如果 HTTP 狀態碼是 4xx/5xx，則引發異常

            total_size = int(response.headers.get('content-length', 0))
            
            with open(file_path, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)
            
            logging.info(f"檔案 '{filename}' 下載成功。")

        except requests.exceptions.RequestException as e:
            logging.error(f"下載檔案 '{filename}' 時發生錯誤: {e}")
            # 如果下載失敗，最好刪除不完整的檔案
            if os.path.exists(file_path):
                os.remove(file_path)
            # 拋出異常，讓主程式知道啟動失敗
            raise RuntimeError(f"無法下載必要的星曆檔案 {filename}，應用程式無法啟動。") from e

if __name__ == '__main__':
    # 如果直接運行此腳本，則執行下載檢查
    print("開始檢查並下載 Swiss Ephemeris 星曆檔案...")
    ensure_ephe_files_exist()
    print(f"\n所有必要的星曆檔案都已存在於 '{EPHE_DIR}'。")