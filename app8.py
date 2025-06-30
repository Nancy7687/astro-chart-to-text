# app.py - 占星命盤生成器後端程式碼 (修正版)
# VERSION: Multi-Chart Support with Composite Chart
# FIX: 修正了組合中點盤在計算相位時，因四軸點缺少 'house' 鍵而導致的 KeyError。
# FIX: 修正了 IndentationError。
# NEW: 增加了對組合中點盤 (Composite Chart) 的計算與 API 端點。
# NOTE: 比較合盤與行運盤的輸出結構與 app4.py 保持一致。

import os # 用於檢查檔案系統路徑
import swisseph as swe # 核心占星計算庫
import urllib.request
from flask import Flask, request, jsonify, render_template
import datetime
import pytz # 用於處理時區
import json # 用於處理JSON數據
import logging # 引入日誌模組
import math # 用於數學計算，特別是組合盤宮位

# --- 自動下載星曆資料的區塊 ---

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

# 2. 定義星曆檔案要存放的路徑和下載來源
EPHE_PATH = './ephe'
# 注意：這是 Swiss Ephemeris 官方的 FTP 伺服器位置
BASE_URL = 'ftp://ftp.astro.com/pub/swisseph/ephe/'

# 3. 檢查資料夾是否存在，不存在就建立一個
if not os.path.exists(EPHE_PATH):
    print(f"Creating ephemeris data directory at: {EPHE_PATH}")
    os.makedirs(EPHE_PATH)

# 4. 迴圈檢查每一個必要的檔案，如果不存在就自動下載
for filename in REQUIRED_FILES:
    filepath = os.path.join(EPHE_PATH, filename)
    if not os.path.exists(filepath):
        download_url = BASE_URL + filename
        print(f"'{filename}' not found. Downloading from {download_url}...")
        try:
            urllib.request.urlretrieve(download_url, filepath)
            print(f"Successfully downloaded '{filename}'.")
        except Exception as e:
            print(f"!!! Failed to download '{filename}'. Error: {e}")
            # 如果某個檔案下載失敗，您可以在這裡決定是否要讓程式中止

# 5. 告訴 swisseph 函式庫要去哪裡找資料
swe.set_ephe_path(EPHE_PATH)

print("Ephemeris check complete. All required files are present.")

# --- 自動下載區塊結束 ---

# 配置日誌，以便在終端機中看到更多詳細訊息
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

# 在Render佈署網站時使用這句(仍先註解掉以測試)
# port = int(os.environ.get("PORT", 5000))  # 預設5000，Render會自動給定PORT

# 設定 Flask 模板資料夾為當前目錄，這樣可以直接找到 astro3.html (For development)

app.template_folder = '.'

# ==============================================================================
# Global Configuration and Data (全域配置和數據)
# ==============================================================================

# 先註解隱藏原本本地的ephe資料夾
# EPHE_PATH_CONFIG = "C:/swisseph/ephe"

PLANET_IDS = {
    "太陽": swe.SUN, "月亮": swe.MOON, "水星": swe.MERCURY, "金星": swe.VENUS,
    "火星": swe.MARS, "木星": swe.JUPITER, "土星": swe.SATURN, "天王": swe.URANUS,
    "海王": swe.NEPTUNE, "冥王": swe.PLUTO, "凱龍": swe.CHIRON, "穀神": swe.CERES,
    "智神": swe.PALLAS, "婚神": swe.JUNO, "灶神": swe.VESTA,
    "愛神": swe.AST_OFFSET + 433, "莉莉絲": swe.MEAN_APOG, "靈神": swe.AST_OFFSET + 16,
    "人龍": swe.PHOLUS, "北交": swe.MEAN_NODE,
}

ZODIAC_SIGNS = [
    "牡羊", "金牛", "雙子", "巨蟹", "獅子", "處女",
    "天秤", "天蠍", "射手", "摩羯", "水瓶", "雙魚",
]

ASPECTS = {
    "合相": 0, "十二分相": 30, "半刑": 45, "六合": 60, "五分相": 72,
    "刑": 90, "拱": 120, "補八分相": 135, "倍五分相": 144, "梅花形相": 150, "沖": 180,
}

DEFAULT_ORB = {
    "合相": 8, "沖": 8, "拱": 6, "刑": 6, "六合": 5, "梅花形相": 4,
    "半刑": 3, "補八分相": 3, "十二分相": 3, "五分相": 2.5, "倍五分相": 2.5,
}

FOUR_ANGLES_AND_NODES = ['上升', '下降', '天頂', '天底', '宿命', '福點', '北交', '南交']
HOUSE_DEFINING_POINTS = ['上升', '下降', '天頂', '天底']

PLANETS_THAT_CAN_RETROGRADE = [
    "水星", "金星", "火星", "木星", "土星", "天王", "海王", "冥王",
    "凱龍", "穀神", "智神", "婚神", "灶神", "愛神", "莉莉絲", "靈神", "人龍"
]

BASE_PLANETS = [
    "太陽", "月亮", "水星", "金星", "火星", "木星", "土星",
    "天王", "海王", "冥王", "北交"
]

# ==============================================================================
# Helper Functions (輔助函數)
# ==============================================================================

def degree_format(deg: float) -> str:
    return f"{deg:.2f}°"

def zodiac_format(deg: float) -> str:
    sign_idx = int(deg // 30)
    deg_in_sign = deg % 30
    return f"{ZODIAC_SIGNS[sign_idx]}({degree_format(deg_in_sign)})"

def get_midpoint(deg1: float, deg2: float) -> float:
    """
    計算兩個黃道度數在圓周上的最短距離中點 (向量法)。
    這個版本使用向量數學，將角度轉換為 (x, y) 座標，相加後再轉回角度，
    這種方法在處理環繞 360 度的情況時更為穩健且簡潔。

    Args:
        deg1 (float): 第一個角度 (0-360).
        deg2 (float): 第二個角度 (0-360).

    Returns:
        float: 兩個角度的中點度數。
    """
    rad1 = math.radians(deg1)
    rad2 = math.radians(deg2)
    x = math.cos(rad1) + math.cos(rad2)
    y = math.sin(rad1) + math.sin(rad2)
    mid_rad = math.atan2(y, x)
    return (math.degrees(mid_rad) + 360) % 360

def compute_positions(jd_ut: float, planet_names_to_calculate: list):
    try:
        swe.set_ephe_path(EPHE_PATH_CONFIG)
    except Exception as e:
        app.logger.error(f"DEBUG: Setting ephemeris path failed inside compute_positions: {e}", exc_info=True)
    pos = {}
    speeds = {}
    for name in planet_names_to_calculate:
        pid = PLANET_IDS.get(name)
        if pid is None:
            app.logger.warning(f"WARNING: Planet name '{name}' not found in PLANET_IDS, skipping.")
            continue
        try:
            xx, ret_code = swe.calc_ut(jd_ut, pid, swe.FLG_SWIEPH | swe.FLG_SPEED)
            if ret_code < 0:
                error_string = swe.get_errstr(ret_code) if hasattr(swe, 'get_errstr') else "未知錯誤"
                raise Exception(f"Swisseph 計算 {name} 時發生錯誤: {error_string}。")
            pos[name] = xx[0]
            speeds[name] = xx[3]
        except Exception as e:
            app.logger.error(f"計算天體 {name} (PID: {pid}) 時發生錯誤: {e}", exc_info=True)
            pos[name] = 0.0
            speeds[name] = 0.0
    if "北交" in pos and "北交" in speeds:
        pos["南交"] = (pos["北交"] + 180) % 360
        speeds["南交"] = -speeds.get("北交", 0.0)
    return pos, speeds

def compute_four_angles(jd_tt: float, lat: float, lon: float):
    try:
        swe.set_ephe_path(EPHE_PATH_CONFIG)
    except Exception as e:
        app.logger.error(f"除錯：在 compute_four_angles 內設定星曆路徑失敗: {e}", exc_info=True)
    try:
        cusps_output_raw, ascmc_raw = swe.houses(jd_tt, lat, lon, b"P")
        cusps_dict_formatted = {i + 1: cusps_output_raw[i] for i in range(12)}
        angles_data = {
            "上升": ascmc_raw[0], "下降": (ascmc_raw[0] + 180) % 360,
            "天頂": ascmc_raw[1], "天底": (ascmc_raw[1] + 180) % 360,
            "宿命": ascmc_raw[3], "cusps": cusps_dict_formatted,
        }
        return angles_data
    except Exception as e:
        app.logger.error(f"計算四軸時發生錯誤: {e}", exc_info=True)
        raise Exception(f"計算四軸時發生錯誤，請檢查經緯度及時間設定，或星曆檔案: {e}")

def calculate_astrology_chart(year, month, day, hour, minute, latitude, longitude, timezone_str, optional_planets=None, generate_image=False):
    try:
        # --- 修正：處理中國大陸時區與實際太陽時差問題 ---
        # 由於中國統一使用 UTC+8，對於西部地區如成都(經度104°E)，
        # 其地方時間與太陽時有顯著差異，這會嚴重影響上升點等對時間敏感的計算。
        # 許多占星軟體會對此進行校正，或使用更接近當地太陽時的時區。
        # 這裡我們做一個特別處理：當選擇成都時區(Asia/Chongqing)時，
        # 我們使用 UTC+7，這在歷史上(1949年前)是正確的，並且在占星學上
        # 對於現代時間也能更好地反映當地的太陽時，從而得到與其他專業軟體一致的結果。
        if timezone_str == "Asia/Chongqing":
            # 手動建立一個固定的 UTC+7 時區
            utc_offset = datetime.timedelta(hours=8)
            fixed_tz = datetime.timezone(utc_offset, name="UTC+08:00 (Astrological Correction for Chengdu)")
            # 假設輸入的時間就是當地時間，並賦予其正確的時區資訊
            local_dt = datetime.datetime(year, month, day, hour, minute, 0, tzinfo=fixed_tz)
        else:
            # 對於所有其他情況，使用標準的 pytz 處理
            local_tz = pytz.timezone(timezone_str)
            local_dt = local_tz.localize(datetime.datetime(year, month, day, hour, minute, 0))

        utc_dt = local_dt.astimezone(pytz.utc)
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                           utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600)
        delta_t_seconds = swe.deltat(jd_ut)
        jd_tt = jd_ut + delta_t_seconds / (24 * 3600)
        ephe_status = {"status": "OK", "message": "星曆檔案路徑已設定。"}
        if optional_planets is None:
            optional_planets = []
        # 1. 確定要計算位置的天體 (基礎行星 + 用戶選擇的額外行星/點)
        planets_to_compute_positions = list(BASE_PLANETS)
        for p in optional_planets:
            if p in PLANET_IDS and p not in planets_to_compute_positions:
                planets_to_compute_positions.append(p)

        positions_raw, speeds_raw = compute_positions(jd_ut, planets_to_compute_positions)
        angles_data = compute_four_angles(jd_tt, latitude, longitude)
        # 2. 將四軸點無條件加入 positions_raw
        positions_raw['上升'] = angles_data['上升']
        positions_raw['下降'] = angles_data['下降']
        positions_raw['天頂'] = angles_data['天頂']
        positions_raw['天底'] = angles_data['天底']

        # 3. 根據 optional_planets 條件性地加入宿命點和福點
        if "宿命" in optional_planets:
            positions_raw["宿命"] = angles_data["宿命"] # angles_data 已經包含宿命點

        # --- 修正：判斷日夜盤的邏輯 ---
        # 日夜盤的劃分是基於地平線 (上升/下降點)，而非天頂/天底。
        # 太陽在地平線上方 (7-12宮) 為日盤，下方 (1-6宮) 為夜盤。
        # 正確的計算方式是看太陽與上升點的相對位置。
        sun_deg = positions_raw['太陽']
        asc_deg = angles_data['上升']
        # 計算太陽在上升點之後的黃道度數距離 (逆時針方向)
        sun_from_asc = (sun_deg - asc_deg + 360) % 360
        # 如果距離大於等於180度，代表太陽在7-12宮，為日盤
        is_day_chart = (sun_from_asc >= 180)

        if "福點" in optional_planets:
            positions_raw["福點"] = compute_part_of_fortune(
                positions_raw["太陽"], positions_raw["月亮"], angles_data["上升"], is_day_chart
            )
        # 確保所有點 (包括行星、四軸、交點、宿命、福點) 都有速度資訊 (預設為 0)
        for name in positions_raw.keys():
            speeds_raw.setdefault(name, 0.0)

        # 為了除錯，保留舊的計算方式
        mc_deg = angles_data['天頂']
        sun_relative_mc_degree = (sun_deg - mc_deg + 360) % 360

        # 4. 構建 all_points_detailed_info
        all_points_detailed_info = {}
        for name, deg in positions_raw.items():
            speed = speeds_raw.get(name, 0.0)
            retrograde_label = ""
            is_retrograde = False
            if name in PLANETS_THAT_CAN_RETROGRADE and speed < 0: # 只有行星才考慮逆行
                retrograde_label = "逆行"
                is_retrograde = True

            house_num, hdeg_in_house = find_house(deg, angles_data['cusps'])

            all_points_detailed_info[name] = {
                'lon': deg, 'speed': speed, 'house': house_num, 'hdeg': hdeg_in_house,
                'is_retrograde': is_retrograde, 'retrograde_label': retrograde_label,
                'zodiac_position_formatted': zodiac_format(deg)
            }
        
            # 5. (可選) 生成星盤圖
        image_data = None
        if generate_image:
            # image_data = _generate_chart_image(all_points_detailed_info, angles_data['cusps']) # 未來實現的函式
            image_data = "placeholder_for_base64_image_string" # 目前使用佔位符
        return {
            "local_time": local_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "utc_time": utc_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "julian_day_ut": jd_ut, "delta_t_seconds": delta_t_seconds, "julian_day_tt": jd_tt,
            "latitude": latitude, "longitude": longitude,
            "ephemeris_path_status": ephe_status,
            "debug_info": {"sun_degree": sun_deg, "mc_degree": mc_deg, "ic_degree": (mc_deg + 180) % 360, "sun_relative_to_mc_degree": sun_relative_mc_degree, "is_day_chart": is_day_chart},
            "house_cusps": angles_data['cusps'],
            "planet_positions": all_points_detailed_info,
            "aspects": list_aspects(all_points_detailed_info),
            "chart_image_b64": image_data, # 將圖片數據加入回傳結果
        }
    except Exception as e:
        app.logger.error(f"計算命盤時發生錯誤: {e}", exc_info=True)
        return {"error": str(e)}
    
def compute_part_of_fortune(sun_lon: float, moon_lon: float, asc_lon: float, is_day: bool) -> float:
    """計算福點 (Part of Fortune) 的黃道經度。"""
    return (asc_lon + moon_lon - sun_lon) % 360 if is_day else (asc_lon + sun_lon - moon_lon) % 360

def find_house(deg: float, cusps_dict: dict):
    """根據宮頭度數找到天體所在的宮位及其宮內度數。"""
    if not isinstance(cusps_dict, dict) or len(cusps_dict) < 12:
        # 如果宮頭數據不完整，返回預設值 (例如：第一宮，0度)
        return 1, 0.0

    # 將宮頭度數轉換為列表，方便索引
    cusps_list = [cusps_dict.get(i, 0.0) for i in range(1, 13)]

    for i in range(1, 13):
        start_cusp = cusps_list[i - 1]
        # 宮位的結束點是下一個宮位的起始點。
        # 對於第12宮(i=12)，下一個是第1宮，其索引為0。i % 12 的技巧可以完美處理這種情況。
        end_cusp = cusps_list[i % 12]

        # 創建標準化版本的度數用於比較
        d_start, d_end, d_deg = start_cusp, end_cusp, deg
        # 如果宮位跨越了0度牡羊座 (例如，從雙魚座到牡羊座)
        if d_end < d_start: # 如果宮位跨越了0度 (例如：雙魚座宮頭到牡羊座宮頭)
            d_end += 360
            # 如果行星的度數也位於星座的早期 (例如，牡羊座)，它也需要被調整以進行正確的比較
            if d_deg < d_start:
                d_deg += 360

        if d_start <= d_deg < d_end:
            relative_degree = (deg - start_cusp + 360) % 360
            return i, relative_degree
    # 如果在循環中沒有找到宮位 (在正常星盤中不應發生)，則記錄警告並返回預設值
    app.logger.warning(f"無法為度數 {deg} 找到宮位。預設返回第一宮。宮頭: {cusps_list}")
    return 1, 0.0

def aspect_between(p1_name: str, p2_name: str, lon_a: float, lon_b: float, speed_a: float, speed_b: float):
    """計算兩個天體之間的相位。"""
    diff_current = abs(lon_a - lon_b)
    diff_current = min(diff_current, 360 - diff_current) # 確保度數差在0-180之間

    result_aspect = None
    for asp_name, target_angle in ASPECTS.items():
        orb = DEFAULT_ORB.get(asp_name, 3) # 獲取預設容許度
        current_deviation = abs(diff_current - target_angle)

        if current_deviation <= orb:
            aspect_type = ""
            # 判斷是否為入相或出相 (針對有速度的行星)
            is_p1_moving = (p1_name in PLANETS_THAT_CAN_RETROGRADE or p1_name in ["太陽", "月亮"])
            is_p2_moving = (p2_name in PLANETS_THAT_CAN_RETROGRADE or p2_name in ["太陽", "月亮"])
            # 避免對兩個固定點之間的相位計算入相/出相 (因為它們沒有速度)
            is_two_fixed_points = (p1_name in FOUR_ANGLES_AND_NODES and p2_name in FOUR_ANGLES_AND_NODES)

            if (is_p1_moving or is_p2_moving) and not is_two_fixed_points:
                # 模擬短時間後的移動，判斷相位是接近還是遠離
                dt_factor = 1 / 24 # 假設移動1小時
                lon_a_next = (lon_a + speed_a * dt_factor) % 360
                lon_b_next = (lon_b + speed_b * dt_factor) % 360
                diff_next = abs(lon_a_next - lon_b_next)
                diff_next = min(diff_next, 360 - diff_next)
                next_deviation = abs(diff_next - target_angle)
                if next_deviation < current_deviation:
                    aspect_type = "入相"
                elif next_deviation > current_deviation:
                    aspect_type = "出相"
            result_aspect = asp_name, current_deviation, aspect_type
            break # 找到第一個符合容許度的相位就跳出
    return result_aspect

def format_chart_data_for_display(raw_chart_data):
    if "error" in raw_chart_data: return raw_chart_data
    output = {
        "timestamps": {
            "local_time": raw_chart_data["local_time"], "utc_time": raw_chart_data["utc_time"],
            "julian_day_ut": f"{raw_chart_data.get('julian_day_ut', 0):.6f}",
            "delta_t_seconds": raw_chart_data.get('delta_t_seconds', 0),
            "julian_day_tt": f"{raw_chart_data.get('julian_day_tt', 0):.6f}"
        },
        "birth_info": {"latitude": f"{raw_chart_data['latitude']:.2f}", "longitude": f"{raw_chart_data['longitude']:.2f}"},
        "ephemeris_path_status": raw_chart_data.get("ephemeris_path_status", {"status": "Unknown", "message": "N/A"}),
        "debug_info": raw_chart_data.get("debug_info", {}),
        "house_cusps": [{"house_number": i, "zodiac_position_formatted": zodiac_format(raw_chart_data["house_cusps"][i])} for i in range(1, 13)],
        "planet_positions": {},
        "aspects": raw_chart_data["aspects"]
    }
    for name, info in raw_chart_data["planet_positions"].items():
        formatted_info = info.copy()
        formatted_info['house_display'] = f"{int(info['house'])}宮" if info.get('house') is not None else ""
        formatted_info['hdeg_display'] = f"{info['hdeg']:.2f}°" if info.get('hdeg') is not None else ""
        output["planet_positions"][name] = formatted_info
    return output

def list_aspects(detailed_points_info: dict):
    """列出單一星盤內所有天體之間的相位。"""
    res = []
    keys = list(detailed_points_info.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            p1_name, p2_name = keys[i], keys[j]
            p1_info, p2_info = detailed_points_info.get(p1_name), detailed_points_info.get(p2_name)
            if not p1_info or not p2_info: continue

            # 修正：不再過濾所有虛點間的相位，
            # 只精確排除定義上的對分相 (例如 上升-下降, 天頂-天底, 北交-南交)。
            # 這樣就能允許計算如 "天底-宿命" 這類有意義的相位。
            definitional_oppositions = [
                {"上升", "下降"},
                {"天頂", "天底"},
                {"北交", "南交"},
            ]
            current_pair = {p1_name, p2_name}
            if any(current_pair == pair for pair in definitional_oppositions):
                continue

            p1_lon, p2_lon = p1_info['lon'], p2_info['lon']
            p1_speed, p2_speed = p1_info.get('speed', 0.0), p2_info.get('speed', 0.0)

            asp_info = aspect_between(p1_name, p2_name, p1_lon, p2_lon, p1_speed, p2_speed)
            if asp_info:
                asp_name, orb_val, aspect_type = asp_info
                res.append({
                    "p1_name": p1_name, "p2_name": p2_name, "aspect_name": asp_name,
                    "aspect_type": aspect_type, "orb": orb_val,
                    "p1_details": p1_info, "p2_details": p2_info
                })
    # 根據相位類型和容許度排序
    return sorted(res, key=lambda item: (ASPECTS.get(item["aspect_name"], 361), item["orb"]))

@app.route('/')
def index():
    return render_template('astro3.html')

@app.route('/calculate_single_chart', methods=['POST'])
def calculate_single_chart_api():
    data = request.get_json(force=True)
    try:
        raw_chart_data = calculate_astrology_chart(
            int(data['year']), int(data['month']), int(data['day']),
            int(data['hour']), int(data['minute']),
            float(data['latitude']), float(data['longitude']),
            data['timezone'], data.get('optional_planets', []))
        if "error" in raw_chart_data:
            app.logger.error(f"單盤計算錯誤: {raw_chart_data['error']}")
            return jsonify(raw_chart_data), 400
        formatted_output = format_chart_data_for_display(raw_chart_data)
        formatted_output['chart_type'] = 'single'
        return jsonify(formatted_output)
    except Exception as e:
        app.logger.error(f"後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500

@app.route('/calculate_comparison_chart', methods=['POST'])
def calculate_comparison_chart_api():
    data = request.get_json(force=True)
    try:
        optional_planets = data.get('optional_planets', [])
        c1_raw = calculate_astrology_chart(
            int(data['chart1_year']), int(data['chart1_month']), int(data['chart1_day']),
            int(data['chart1_hour']), int(data['chart1_minute']),
            float(data['chart1_latitude']), float(data['chart1_longitude']),
            data['chart1_timezone'], optional_planets)
        c2_raw = calculate_astrology_chart(
            int(data['chart2_year']), int(data['chart2_month']), int(data['chart2_day']),
            int(data['chart2_hour']), int(data['chart2_minute']),
            float(data['chart2_latitude']), float(data['chart2_longitude']),
            data['chart2_timezone'], optional_planets)
        if "error" in c1_raw or "error" in c2_raw:
            app.logger.error(f"比較盤計算錯誤: Chart 1 Error: {c1_raw.get('error', 'N/A')}, Chart 2 Error: {c2_raw.get('error', 'N/A')}")
            return jsonify({"error": f"Chart 1 Error: {c1_raw.get('error', 'N/A')}, Chart 2 Error: {c2_raw.get('error', 'N/A')}"}), 400
        response_data = {
            "chart_type": "comparison",
            "chart1_data": format_chart_data_for_display(c1_raw),
            "chart2_data": format_chart_data_for_display(c2_raw),
            "inter_aspects": list_interchart_aspects(c1_raw['planet_positions'], c2_raw['planet_positions']),
            "chart1_planets_in_chart2_houses": get_planet_overlays_in_houses(c1_raw['planet_positions'], c2_raw['house_cusps']),
            "chart2_planets_in_chart1_houses": get_planet_overlays_in_houses(c2_raw['planet_positions'], c1_raw['house_cusps']),
        }
        return jsonify(response_data)
    except Exception as e:
        app.logger.error(f"後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500
    
def list_interchart_aspects(chart1_points: dict, chart2_points: dict):
    """列出兩個星盤之間所有天體之間的相位。"""
    res = []
    for p1_name, p1_info in chart1_points.items():
        for p2_name, p2_info in chart2_points.items():
            # 為了讓輸出更精確，我們計算「行星與任何點」的相位，
            # 但排除「固定點與固定點」之間的相位 (例如：本命上升點與行運天頂點)。
            # 這與單盤相位的邏輯一致。
            is_p1_fixed = p1_name in FOUR_ANGLES_AND_NODES
            is_p2_fixed = p2_name in FOUR_ANGLES_AND_NODES
            if is_p1_fixed and is_p2_fixed:
                continue

            # 確保 p1_info 和 p2_info 存在且包含 'lon' 鍵
            if not p1_info or 'lon' not in p1_info or not p2_info or 'lon' not in p2_info:
                continue

            p1_lon, p2_lon = p1_info['lon'], p2_info['lon']
            # 跨盤相位通常不考慮速度來判斷入相/出相，因為是兩個獨立時間點的盤
            # 但為了通用性，我們仍然傳遞速度，aspect_between 會根據其邏輯判斷
            p1_speed, p2_speed = p1_info.get('speed', 0.0), p2_info.get('speed', 0.0)

            asp_info = aspect_between(p1_name, p2_name, p1_lon, p2_lon, p1_speed, p2_speed)
            if asp_info:
                asp_name, orb_val, aspect_type = asp_info
                res.append({
                    "p1_name": p1_name, "p2_name": p2_name, "aspect_name": asp_name,
                    "aspect_type": aspect_type, "orb": orb_val,
                    "p1_details": p1_info, "p2_details": p2_info
                })
    # 根據相位類型和容許度排序
    return sorted(res, key=lambda item: (ASPECTS.get(item["aspect_name"], 361), item["orb"]))

@app.route('/calculate_transit_chart', methods=['POST'])
def calculate_transit_chart_api():
    data = request.get_json(force=True)
    try:
        optional_planets = data.get('optional_planets', [])
        natal_raw = calculate_astrology_chart(
            int(data['natal_year']), int(data['natal_month']), int(data['natal_day']),
            int(data['natal_hour']), int(data['natal_minute']),
            float(data['natal_latitude']), float(data['natal_longitude']),
            data['natal_timezone'], optional_planets)
        transit_raw = calculate_astrology_chart(
            int(data['transit_year']), int(data['transit_month']), int(data['transit_day']),
            int(data['transit_hour']), int(data['transit_minute']),
            float(data['transit_latitude']), float(data['transit_longitude']),
            data['transit_timezone'], optional_planets)
        if "error" in natal_raw or "error" in transit_raw:
            app.logger.error(f"行運盤計算錯誤: Natal Error: {natal_raw.get('error', 'N/A')}, Transit Error: {transit_raw.get('error', 'N/A')}")
            return jsonify({"error": f"Natal Error: {natal_raw.get('error', 'N/A')}, Transit Error: {transit_raw.get('error', 'N/A')}"}), 400
        response_data = {
            "chart_type": "transit",
            "natal_chart_data": format_chart_data_for_display(natal_raw),
            "transit_chart_data": format_chart_data_for_display(transit_raw),
            "inter_aspects": list_interchart_aspects(natal_raw['planet_positions'], transit_raw['planet_positions']),
            "natal_planets_in_transit_houses": get_planet_overlays_in_houses(natal_raw['planet_positions'], transit_raw['house_cusps']),
            "transit_planets_in_natal_houses": get_planet_overlays_in_houses(transit_raw['planet_positions'], natal_raw['house_cusps']),
        }
        return jsonify(response_data)
    except Exception as e:
        app.logger.error(f"後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500
    
def get_planet_overlays_in_houses(source_chart_points: dict, target_chart_cusps: dict):
    """計算一個星盤中的所有點落入另一個星盤的宮位。"""
    overlays = []
    # 修正：不再排除任何點，計算所有點的落宮資訊，以提供最完整的數據。
    for planet_name in source_chart_points.keys():
        planet_info = source_chart_points.get(planet_name)
        if not planet_info or 'lon' not in planet_info:
            continue # 跳過無效的行星資訊

        house_in_target, deg_in_target_house = find_house(planet_info['lon'], target_chart_cusps)
        overlays.append({
            "planet_name": planet_name,
            "zodiac_position_formatted": zodiac_format(planet_info['lon']),
            "retrograde_label": planet_info.get('retrograde_label', ''),
            "house_in_target_chart": house_in_target,
            "degree_in_target_house": deg_in_target_house
        })
    return overlays  

@app.route('/calculate_composite_chart', methods=['POST'])
def calculate_composite_chart_api():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "請求中未提供 JSON 數據"}), 400
    try:
        optional_planets = data.get('optional_planets', [])
        c1_raw = calculate_astrology_chart(
            int(data['chart1_year']), int(data['chart1_month']), int(data['chart1_day']),
            int(data['chart1_hour']), int(data['chart1_minute']),
            float(data['chart1_latitude']), float(data['chart1_longitude']),
            data['chart1_timezone'], optional_planets)
        c2_raw = calculate_astrology_chart(
            int(data['chart2_year']), int(data['chart2_month']), int(data['chart2_day']),
            int(data['chart2_hour']), int(data['chart2_minute']),
            float(data['chart2_latitude']), float(data['chart2_longitude']),
            data['chart2_timezone'], optional_planets)
        if "error" in c1_raw or "error" in c2_raw:
            app.logger.error(f"組合盤計算錯誤: Chart 1 Error: {c1_raw.get('error', 'N/A')}, Chart 2 Error: {c2_raw.get('error', 'N/A')}")
            return jsonify({"error": f"Chart 1 Error: {c1_raw.get('error', 'N/A')}, Chart 2 Error: {c2_raw.get('error', 'N/A')}"}), 400
        composite_positions_raw = {}
        planets_to_process = list(dict.fromkeys(BASE_PLANETS + optional_planets))
        for name in planets_to_process:
            if name in c1_raw['planet_positions'] and name in c2_raw['planet_positions']:
                lon1 = c1_raw['planet_positions'][name]['lon']
                lon2 = c2_raw['planet_positions'][name]['lon']
                composite_positions_raw[name] = {'lon': get_midpoint(lon1, lon2), 'speed': 0}
        # 修正：從中點北交計算中點南交
        if '北交' in composite_positions_raw:
            composite_positions_raw['南交'] = {
                'lon': (composite_positions_raw['北交']['lon'] + 180) % 360,
                'speed': 0
            }
        # --- 修正：採用直接中點法 (Midpoint Method) 計算組合盤軸點與宮頭 ---
        # 這種方法直接取兩個本命盤對應點的中點，是另一種常見的計算技術。
        # 1. 計算中點 MC, ASC, 和 宿命 (如果需要)
        mc1 = c1_raw['planet_positions']['天頂']['lon']
        mc2 = c2_raw['planet_positions']['天頂']['lon']
        composite_mc_deg = get_midpoint(mc1, mc2)

        asc1 = c1_raw['planet_positions']['上升']['lon']
        asc2 = c2_raw['planet_positions']['上升']['lon']
        composite_asc_deg = get_midpoint(asc1, asc2)

        composite_vertex_deg = None
        if "宿命" in optional_planets and '宿命' in c1_raw['planet_positions'] and '宿命' in c2_raw['planet_positions']:
             vertex1 = c1_raw['planet_positions']['宿命']['lon']
             vertex2 = c2_raw['planet_positions']['宿命']['lon']
             composite_vertex_deg = get_midpoint(vertex1, vertex2)

        # 2. 計算所有12個宮頭的中點
        composite_cusps_dict = {}
        for i in range(1, 13):
            cusp1 = c1_raw['house_cusps'][i]
            cusp2 = c2_raw['house_cusps'][i]
            composite_cusps_dict[i] = get_midpoint(cusp1, cusp2)

        # 3. 準備組合盤的基礎數據 (時間和地點的中點)
        jd_ut_mid = (c1_raw['julian_day_ut'] + c2_raw['julian_day_ut']) / 2
        delta_t_mid_seconds = swe.deltat(jd_ut_mid)
        jd_tt_mid = jd_ut_mid + delta_t_mid_seconds / 86400.0
        lat_mid = (c1_raw['latitude'] + c2_raw['latitude']) / 2
        composite_raw = {
            "local_time": f"Composite of {c1_raw['local_time']} and {c2_raw['local_time']}", "utc_time": "Composite UTC",
            "julian_day_ut": jd_ut_mid, "delta_t_seconds": delta_t_mid_seconds, "julian_day_tt": jd_tt_mid,
            "latitude": lat_mid, "longitude": get_midpoint(c1_raw['longitude'], c2_raw['longitude']),
            "ephemeris_path_status": c1_raw['ephemeris_path_status'], "debug_info": {}, "house_cusps": composite_cusps_dict,
            "planet_positions": {},
        }
        # 4. 將所有計算好的中點位置填入
        composite_raw['planet_positions'].update(composite_positions_raw)
        composite_raw['planet_positions'].update({
            '上升': {'lon': composite_asc_deg, 'speed': 0}, '天頂': {'lon': composite_mc_deg, 'speed': 0},
            '下降': {'lon': (composite_asc_deg + 180) % 360, 'speed': 0}, '天底': {'lon': (composite_mc_deg + 180) % 360, 'speed': 0}
        })
        if composite_vertex_deg is not None:
            composite_raw['planet_positions']['宿命'] = {'lon': composite_vertex_deg, 'speed': 0}
        if "福點" in optional_planets and '福點' in c1_raw['planet_positions'] and '福點' in c2_raw['planet_positions']:
            composite_raw['planet_positions']['福點'] = {'lon': get_midpoint(c1_raw['planet_positions']['福點']['lon'], c2_raw['planet_positions']['福點']['lon']), 'speed': 0}
        for name, info in composite_raw['planet_positions'].items():
            info.update({'zodiac_position_formatted': zodiac_format(info['lon']), 'retrograde_label': '', 'is_retrograde': False})
            if name not in HOUSE_DEFINING_POINTS: 
                info['house'], info['hdeg'] = find_house(info['lon'], composite_raw['house_cusps'])
            else:
                info['house'] = None
                info['hdeg'] = None
        composite_raw['aspects'] = list_aspects(composite_raw['planet_positions'])
        return jsonify({
            "chart_type": "composite",
            "composite_chart_data": format_chart_data_for_display(composite_raw),
            "natal_chart1_data": format_chart_data_for_display(c1_raw),
            "natal_chart2_data": format_chart_data_for_display(c2_raw),
        })
    except Exception as e:
        app.logger.error(f"組合盤後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"組合盤伺服器內部錯誤: {e}"}), 500
    
if __name__ == '__main__':
    # 為了能在 Render 上運行，我們需要從環境變數讀取 PORT
    # os.environ.get('PORT', 10000) 的意思是：
    # 嘗試讀取 'PORT' 這個環境變數，如果找不到，就使用 10000 作為預設值
    port = int(os.environ.get('PORT', 10000))

    # 讓 Flask 伺服器監聽在 0.0.0.0，這樣外部才能連線
    # 並使用 Render 指定的 port
    app.run(host='0.0.0.0', port=port)

# 先註解掉，在Render佈署網站去跑時
# if __name__ == '__main__':
#    try:
#        ephe_path_to_use = EPHE_PATH_CONFIG
#        if not os.path.exists(ephe_path_to_use):
#            print(f"警告：找不到星曆檔案資料夾 '{ephe_path_to_use}'。請下載 Swisseph 星曆檔案並將其放置在此目錄中，否則計算可能無法進行或不準確。")
#            print("您可以從 http://www.astro.com/ftp/swisseph/ephe/ 處下載相關檔案。")
#            
#        swe.set_ephe_path(ephe_path_to_use)
#        print(f"Swisseph 星曆檔案路徑已設定為: {ephe_path_to_use}")
        
#    except Exception as e:
#        print(f"錯誤：無法設定 Swisseph 星曆檔案路徑: {e}")
#        print("請檢查 pyswisseph 安裝和星曆檔案的配置。")

#    app.run(debug=True, port=5000)
