# 預備下載星曆相關

import os
import swisseph as swe # 確保這裡有導入 swisseph
import urllib.request

print("--- Starting Ephemeris File Download Script ---")

# 1. 定義所有您需要的星曆檔案名稱列表
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

# 2. 定義星曆檔案將存放的目錄名稱和下載來源
EPHE_DIR_NAME = 'ephe' # 你的資料目錄名稱
BASE_URL = 'ftp://ftp.astro.com/pub/swisseph/ephe/'

def ensure_ephemeris_data_and_set_path():
    """
    確保所有必要的 Swisseph 星曆檔案都被下載，並設定 Swisseph 的查找路徑。
    """
    # 取得當前腳本 (download_ephe.py) 所在目錄的絕對路徑
    # 這能確保無論主應用程式在哪裡執行，都能正確找到 './ephe' 資料夾
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 建構星曆資料目錄的絕對路徑
    EPHE_PATH_ABS = os.path.join(script_dir, EPHE_DIR_NAME)

    # 3. 檢查星曆資料目錄是否存在；如果不存在，則建立它
    if not os.path.exists(EPHE_PATH_ABS):
        print(f"正在建立星曆資料目錄於: {EPHE_PATH_ABS}")
        os.makedirs(EPHE_PATH_ABS)
    else:
        print(f"星曆資料目錄已存在於: {EPHE_PATH_ABS}")

    # 4. 遍歷每個必要的檔案，如果不存在就下載它
    for relative_path in REQUIRED_FILES:
        local_filepath = os.path.join(EPHE_PATH_ABS, relative_path)
        
        # 確保子目錄也存在 (例如 ast0/)
        local_dir = os.path.dirname(local_filepath)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True) # exist_ok=True 是個好習慣

        if not os.path.exists(local_filepath):
            # 轉換路徑分隔符號以用於 URL (例如：'ast0\se00016s.se1' -> 'ast0/se00016s.se1')
            url_path = relative_path.replace(os.path.sep, '/')
            download_url = BASE_URL + url_path
            
            print(f"正在從 {download_url} 下載 '{relative_path}'...")
            try:
                urllib.request.urlretrieve(download_url, local_filepath)
                print(f"成功下載 '{relative_path}'。")
            except Exception as e:
                print(f"!!! 無法下載 '{relative_path}'。錯誤: {e}")
        # else: # 如果你希望顯示已存在檔案的訊息，可以解除這行的註解
        #     print(f"檔案 '{relative_path}' 已存在，跳過下載。")

    print("--- 星曆檔案下載與檢查完成 ---")

    # --- 關鍵步驟：設定 Swisseph 的路徑 ---
    # 這會告訴 swisseph 函式庫去哪裡找到你下載的檔案。
    os.environ['SE_PATH'] = EPHE_PATH_ABS
    
    # 如果你更喜歡，也可以使用 swisseph 函式庫自己的函數：
    # swe.set_ephe_path(EPHE_PATH_ABS)

    print(f"Swisseph 路徑已設定為: {os.environ['SE_PATH']}")

    # 可選：透過詢問 Swisseph 正在使用的路徑來驗證設定是否成功
    try:
        print(f"Swisseph 實際查找的路徑: {swe.get_ephe_path()}")
    except Exception as e:
        print(f"警告: 設定路徑後，無法正確獲取 Swisseph 的有效路徑: {e}")

# 這是關鍵的 Python 慣用語法，它確保當 download_ephe.py 被導入 (import) 時，
# ensure_ephemeris_data_and_set_path() 函數會自動執行，
# 但當它直接被執行 (例如透過命令列) 時，則不會自動執行。
if __name__ != '__main__':
    ensure_ephemeris_data_and_set_path()

# 這個區塊允許你直接執行 download_ephe.py 來執行下載動作
if __name__ == '__main__':
    print("直接運行 download_ephe.py 以確保資料存在並設定路徑。")
    ensure_ephemeris_data_and_set_path()
    print("直接下載和路徑設定已完成。")