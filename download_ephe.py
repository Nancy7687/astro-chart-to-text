# import os
# import swisseph as swe  # 核心占星計算庫
# import urllib.request
# import time  # 引入 time 模組用於延遲

# # 星曆檔案的 FTP 伺服器基礎 URL
# BASE_URL = "ftp://ftp.astro.com/pub/swisseph/ephe/"
# # 存放星曆資料的目錄名稱，相對於你的 Python 腳本
# EPHE_DIR_NAME = "ephe"

# # 需要下載的星曆檔案列表
# # 這是 swisseph 正常運行所需的一些基本檔案
# REQUIRED_FILES = [

# 'all_long.txt',
# 'all_short.txt',
# 'ast0/se00016s.se1',
# 'ast0/se00393s.se1',
# 'ast0/se00433s.se1',
# 'list_long.txt',
# 'list_short.txt',
# 'plmolist.txt',
# 'sat/plmolist.txt',
# 'sat/sepm9401.se1',
# 'sat/sepm9402.se1',
# 'sat/sepm9501.se1',
# 'sat/sepm9502.se1',
# 'sat/sepm9503.se1',
# 'sat/sepm9504.se1',
# 'sat/sepm9599.se1',
# 'sat/sepm9601.se1',
# 'sat/sepm9602.se1',
# 'sat/sepm9603.se1',
# 'sat/sepm9604.se1',
# 'sat/sepm9605.se1',
# 'sat/sepm9606.se1',
# 'sat/sepm9607.se1',
# 'sat/sepm9608.se1',
# 'sat/sepm9699.se1',
# 'sat/sepm9701.se1',
# 'sat/sepm9702.se1',
# 'sat/sepm9703.se1',
# 'sat/sepm9704.se1',
# 'sat/sepm9705.se1',
# 'sat/sepm9799.se1',
# 'sat/sepm9801.se1',
# 'sat/sepm9802.se1',
# 'sat/sepm9808.se1',
# 'sat/sepm9899.se1',
# 'sat/sepm9901.se1',
# 'sat/sepm9902.se1',
# 'sat/sepm9903.se1',
# 'sat/sepm9904.se1',
# 'sat/sepm9905.se1',
# 'sat/sepm9999.se1',
# 'se00016s.se1',
# 'se00393s.se1',
# 'se00433s.se1',
# 'seasm06.se1',
# 'seasm102.se1',
# 'seasm108.se1',
# 'seasm114.se1',
# 'seasm12.se1',
# 'seasm120.se1',
# 'seasm126.se1',
# 'seasm132.se1',
# 'seasm18.se1',
# 'seasm24.se1',
# 'seasm30.se1',
# 'seasm36.se1',
# 'seasm42.se1',
# 'seasm48.se1',
# 'seasm54.se1',
# 'seasm60.se1',
# 'seasm66.se1',
# 'seasm72.se1',
# 'seasm78.se1',
# 'seasm84.se1',
# 'seasm90.se1',
# 'seasm96.se1',
# 'seasnam.txt',
# 'seas_00.se1',
# 'seas_06.se1',
# 'seas_102.se1',
# 'seas_108.se1',
# 'seas_114.se1',
# 'seas_12.se1',
# 'seas_120.se1',
# 'seas_126.se1',
# 'seas_132.se1',
# 'seas_138.se1',
# 'seas_144.se1',
# 'seas_150.se1',
# 'seas_156.se1',
# 'seas_162.se1',
# 'seas_18.se1',
# 'seas_24.se1',
# 'seas_30.se1',
# 'seas_36.se1',
# 'seas_42.se1',
# 'seas_48.se1',
# 'seas_54.se1',
# 'seas_60.se1',
# 'seas_66.se1',
# 'seas_72.se1',
# 'seas_78.se1',
# 'seas_84.se1',
# 'seas_90.se1',
# 'seas_96.se1',
# 'sefstars.txt',
# 'semom06.se1',
# 'semom102.se1',
# 'semom108.se1',
# 'semom114.se1',
# 'semom12.se1',
# 'semom120.se1',
# 'semom126.se1',
# 'semom132.se1',
# 'semom18.se1',
# 'semom24.se1',
# 'semom30.se1',
# 'semom36.se1',
# 'semom42.se1',
# 'semom48.se1',
# 'semom54.se1',
# 'semom60.se1',
# 'semom66.se1',
# 'semom72.se1',
# 'semom78.se1',
# 'semom84.se1',
# 'semom90.se1',
# 'semom96.se1',
# 'semo_00.se1',
# 'semo_06.se1',
# 'semo_102.se1',
# 'semo_108.se1',
# 'semo_114.se1',
# 'semo_12.se1',
# 'semo_120.se1',
# 'semo_126.se1',
# 'semo_132.se1',
# 'semo_138.se1',
# 'semo_144.se1',
# 'semo_150.se1',
# 'semo_156.se1',
# 'semo_162.se1',
# 'semo_18.se1',
# 'semo_24.se1',
# 'semo_30.se1',
# 'semo_36.se1',
# 'semo_42.se1',
# 'semo_48.se1',
# 'semo_54.se1',
# 'semo_60.se1',
# 'semo_66.se1',
# 'semo_72.se1',
# 'semo_78.se1',
# 'semo_84.se1',
# 'semo_90.se1',
# 'semo_96.se1',
# 'seorbel.txt',
# 'seplm06.se1',
# 'seplm102.se1',
# 'seplm108.se1',
# 'seplm114.se1',
# 'seplm12.se1',
# 'seplm120.se1',
# 'seplm126.se1',
# 'seplm132.se1',
# 'seplm18.se1',
# 'seplm24.se1',
# 'seplm30.se1',
# 'seplm36.se1',
# 'seplm42.se1',
# 'seplm48.se1',
# 'seplm54.se1',
# 'seplm60.se1',
# 'seplm66.se1',
# 'seplm72.se1',
# 'seplm78.se1',
# 'seplm84.se1',
# 'seplm90.se1',
# 'seplm96.se1',
# 'sepl_00.se1',
# 'sepl_06.se1',
# 'sepl_102.se1',
# 'sepl_108.se1',
# 'sepl_114.se1',
# 'sepl_12.se1',
# 'sepl_120.se1',
# 'sepl_126.se1',
# 'sepl_132.se1',
# 'sepl_138.se1',
# 'sepl_144.se1',
# 'sepl_150.se1',
# 'sepl_156.se1',
# 'sepl_162.se1',
# 'sepl_18.se1',
# 'sepl_24.se1',
# 'sepl_30.se1',
# 'sepl_36.se1',
# 'sepl_42.se1',
# 'sepl_48.se1',
# 'sepl_54.se1',
# 'sepl_60.se1',
# 'sepl_66.se1',
# 'sepl_72.se1',
# 'sepl_78.se1',
# 'sepl_84.se1',
# 'sepl_90.se1',
# 'sepl_96.se1',
# 'sepm9401.se1',
# 'sepm9402.se1',
# 'sepm9501.se1',
# 'sepm9502.se1',
# 'sepm9503.se1',
# 'sepm9504.se1',
# 'sepm9599.se1',
# 'sepm9601.se1',
# 'sepm9602.se1',
# 'sepm9603.se1',
# 'sepm9604.se1',
# 'sepm9605.se1',
# 'sepm9606.se1',
# 'sepm9607.se1',
# 'sepm9608.se1',
# 'sepm9699.se1',
# 'sepm9701.se1',
# 'sepm9702.se1',
# 'sepm9703.se1',
# 'sepm9704.se1',
# 'sepm9705.se1',
# 'sepm9799.se1',
# 'sepm9801.se1',
# 'sepm9802.se1',
# 'sepm9808.se1',
# 'sepm9899.se1',
# 'sepm9901.se1',
# 'sepm9902.se1',
# 'sepm9903.se1',
# 'sepm9904.se1',
# 'sepm9905.se1',
# 'sepm9999.se1',

#     # --- 請在這裡繼續加入您需要的其他檔案名，例如凱龍星 'sech_18.se1' ---

# ]

# def ensure_ephemeris_data_and_set_path():
#     """
#     檢查星曆資料目錄是否存在並確保所需檔案已被下載。
#     同時設定 swisseph 的星曆路徑。
#     """
#     print("DEBUG: download_ephe.py - Starting ensure_ephemeris_data_and_set_path()...")

#     # 獲取當前腳本的絕對路徑
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     # 構建星曆資料的絕對路徑
#     EPHE_PATH_ABS = os.path.join(script_dir, EPHE_DIR_NAME)

#     # 檢查並創建星曆資料目錄
#     if not os.path.exists(EPHE_PATH_ABS):
#         print(f"DEBUG: Creating ephemeris data directory at: {EPHE_PATH_ABS}")
#         os.makedirs(EPHE_PATH_ABS)
#     else:
#         print(f"DEBUG: Ephemeris data directory already exists at: {EPHE_PATH_ABS}")

#     # 遍歷所需檔案，檢查並下載
#     for relative_path in REQUIRED_FILES:
#         local_filepath = os.path.join(EPHE_PATH_ABS, relative_path)
#         local_dir = os.path.dirname(local_filepath)

#         # 確保本地子目錄存在 (如果檔案在子目錄中)
#         if not os.path.exists(local_dir):
#             os.makedirs(local_dir, exist_ok=True)

#         if not os.path.exists(local_filepath):
#             # 將相對路徑中的系統分隔符轉換為 URL 中的斜槓
#             url_path = relative_path.replace(os.path.sep, '/')
#             download_url = BASE_URL + url_path

#             print(f"DEBUG: Downloading '{relative_path}' from {download_url}...")
#             try:
#                 # 使用 urllib.request 進行下載
#                 urllib.request.urlretrieve(download_url, local_filepath)
#                 print(f"DEBUG: Successfully downloaded '{relative_path}'.")
#             except Exception as e:
#                 print(f"ERROR: Failed to download '{relative_path}'. Error: {e}")
#                 # 在生產環境中，如果關鍵檔案下載失敗，你可能希望這裡拋出異常或終止應用程式
#                 # raise  # 如果要強制停止，可以取消註解這行
#                 time.sleep(1) # 短暫延遲，避免連續失敗導致過度請求
#         else:
#             # print(f"DEBUG: File '{relative_path}' already exists, skipping download.")
#             pass # 為了保持日誌簡潔，已存在檔案時不打印

#     print("DEBUG: --- Ephemeris File Download & Check Complete ---")

#     # 設定 swisseph 的星曆路徑環境變數
#     os.environ['SE_PATH'] = EPHE_PATH_ABS

#     print(f"DEBUG: Swisseph path set to: {os.environ['SE_PATH']}")

#     # 驗證 swisseph 是否能找到路徑
#     try:
#         # swisseph.get_ephe_path() 函式返回 swisseph 當前正在尋找星曆檔案的路徑
#         print(f"DEBUG: Swisseph is actually looking in: {swe.get_ephe_path()}")
#     except Exception as e:
#         print(f"WARNING: Could not retrieve Swisseph's effective path after setting: {e}")


# if __name__ == '__main__':
#     # 這個區塊只在 download_ephe.py 被直接執行時運行
#     # 在導入時不會執行，這有助於在開發時獨立測試這個腳本
#     print("Running download_ephe.py directly for testing...")
#     ensure_ephemeris_data_and_set_path()
#     print("Direct execution of ephemeris setup complete.")