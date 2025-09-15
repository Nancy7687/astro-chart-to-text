# app.py (Final Verified Version)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime
import pytz
import swisseph as swe
import json
import os
import logging
import math
from functools import wraps
from dotenv import load_dotenv

load_dotenv() # 在應用程式啟動時從 .env 載入變數

# --- Import our downloader script ---
import swiss_ephe_downloader


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Standard Flask App Initialization ---
app = Flask(__name__, template_folder='templates')
CORS(app)

# ==============================================================================
# --- API Security Configuration ---
# ==============================================================================
API_KEY = os.getenv("ASTRO_API_KEY")
if not API_KEY:
    logging.warning("警告：在 .env 檔案中找不到 ASTRO_API_KEY。API 端點將無法訪問。")





# 取得所有 IANA 時區名稱
all_timezones = pytz.all_timezones

# 可以選擇性地過濾掉一些比較不常用的或內部使用的時區，
# 但對於自動完成來說，全部提供通常也沒問題
# 例如：過濾掉 POSIX 時區，或只留下常見的時區
# filtered_timezones = [tz for tz in all_timezones if not tz.startswith('Etc/') and not tz.startswith('SystemV/')]

# 將列表轉換成 JSON 格式傳給前端
# print(json.dumps(list(all_timezones)))

# ==============================================================================
# --- Run the downloader and set the ephemeris path at startup ---
# ==============================================================================
# Use the path defined in the downloader to ensure consistency
# EPHE_PATH_CONFIG = swiss_ephe_downloader.EPHE_DIR
EPHE_PATH_CONFIG = os.path.abspath(swiss_ephe_downloader.EPHE_DIR) # 確保是絕對路徑
print(f"DEBUG: EPHE_PATH_CONFIG is set to: {EPHE_PATH_CONFIG}")
try:
    # This will trigger downloads on the server if files are missing
    swiss_ephe_downloader.ensure_ephe_files_exist()
    # Then, tell the swisseph engine where to find them
    swe.set_ephe_path(EPHE_PATH_CONFIG)
    logging.info(f"Successfully set Swisseph ephemeris path to: {EPHE_PATH_CONFIG}")
except Exception as e:
    logging.critical(f"FATAL ERROR: Could not set up or download ephemeris files. App cannot run. Error: {e}", exc_info=True)
# ==============================================================================



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
def dms_format(deg: float) -> str:
    """將十進制度數轉換為度、分的 60 進制格式 (含四捨五入與進位處理)"""
    
    # 你之前遇到的 NoneType 錯誤，如果這個函數在其他地方也可能接收 None，建議保留這行
    # 例如：
    # if deg is None:
    #     return "N/A" # 或者 "00°00'"

    d = int(deg)  # 取整數度數
    minutes_decimal = (deg - d) * 60  # 將小數部分轉換為分鐘（含小數）
    m = round(minutes_decimal)  # **關鍵：在這裡對分鐘進行四捨五入**

    # 處理分鐘的進位（如果四捨五入後分鐘達到 60）
    if m >= 60:
        d += 1
        m = 0
    
    # 不再計算和處理秒數

    # 格式化為 XX°YY' (只顯示度數和分鐘)
    # 使用 zfill 確保兩位數格式（例如 5 變成 05）
    return f"{str(d).zfill(2)}°{str(m).zfill(2)}'"

def degree_format(deg: float) -> str:
    # OLD: return f"{deg:.2f}°"
    # NEW: Use the new DMS formatter
    return dms_format(deg)

def zodiac_format(deg: float) -> str:
    sign_idx = int(deg // 30)
    deg_in_sign = deg % 30
    return f"{ZODIAC_SIGNS[sign_idx]}({degree_format(deg_in_sign)})"

def get_midpoint(deg1: float, deg2: float) -> float:
    rad1 = math.radians(deg1)
    rad2 = math.radians(deg2)
    x = math.cos(rad1) + math.cos(rad2)
    y = math.sin(rad1) + math.sin(rad2)
    mid_rad = math.atan2(y, x)
    return (math.degrees(mid_rad) + 360) % 360

def compute_positions(jd_ut: float, planet_names_to_calculate: list):
    # 注意：現在不再需要在每個函數內都呼叫 set_ephe_path
    # 因為我們已經在應用程式啟動時全域設定好了。
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

# ==============================================================================
# --- 請用此版本【完整取代】您 app.py 中的舊函式 ---
# ==============================================================================

def calculate_astrology_chart(year, month, day, hour, minute, latitude, longitude, timezone_str, optional_planets=None, generate_image=False):
    """
    核心計算函式。此版本已加入「智慧依賴處理」邏輯，
    例如當使用者勾選福點時，會自動在內部計算其依賴的太陽、月亮和上升。
    """
    try:
        swe.set_ephe_path(EPHE_PATH_CONFIG)
        
        # --- 1. 時間與儒略日計算 (此部分邏輯不變) ---
        if timezone_str == "Asia/Chongqing":
            utc_offset = datetime.timedelta(hours=8)
            fixed_tz = datetime.timezone(utc_offset, name="UTC+08:00 (Astrological Correction for Chengdu)")
            local_dt = datetime.datetime(year, month, day, hour, minute, 0, tzinfo=fixed_tz)
        else:
            try:
                local_tz = pytz.timezone(timezone_str)
                local_dt = local_tz.localize(datetime.datetime(year, month, day, hour, minute, 0))
            except pytz.UnknownTimeZoneError:
                app.logger.warning(f"無效的時區名稱: '{timezone_str}'")
                return {
                    "error": f"您手動輸入的時區 '{timezone_str}' 無效。請檢查拼寫，或從下拉選單中選擇。",
                    "error_type": "invalid_timezone"
                }
        utc_dt = local_dt.astimezone(pytz.utc)
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600)
        delta_t_seconds = swe.deltat(jd_ut)
        jd_tt = jd_ut + delta_t_seconds / (24 * 3600)

        # --- 2. 【核心修改】智慧依賴處理 ---
        # user_requested_planets 是使用者真正想看到的「菜單」
        user_requested_planets = set(optional_planets if optional_planets is not None else [])
        
        # planets_to_calculate 是廚師為了做菜需要準備的「備料單」
        planets_to_calculate = user_requested_planets.copy()
        
        # 如果菜單上有「福點」，備料單就必須加入「太陽、月亮、上升」
        if "福點" in user_requested_planets:
            planets_to_calculate.update({"太陽", "月亮", "上升"})
        
        # 如果菜單上有任何宮位相關的點，備料單就必須加入「上升」
        if any(p in user_requested_planets for p in ["上升", "下降", "天頂", "天底", "宿命"]):
            planets_to_calculate.add("上升")
        
        app.logger.info(f"使用者請求: {user_requested_planets}")
        app.logger.info(f"內部實際計算: {planets_to_calculate}")
        
        # --- 3. 使用「備料單」進行計算 ---
        planets_for_swisseph = [p for p in planets_to_calculate if p in PLANET_IDS]
        positions_raw, speeds_raw = compute_positions(jd_ut, planets_for_swisseph)
        
        # 無論如何都計算四軸和宮位，因為它們是基礎結構
        angles_data = compute_four_angles(jd_tt, latitude, longitude)
        
        # 4. 將所有計算出的點統一格式，存入一個內部字典，以防 'float' object is not subscriptable 錯誤
        internal_points = {}
        for name, lon in positions_raw.items():
            internal_points[name] = {'lon': lon, 'speed': speeds_raw.get(name, 0.0)}
        for name in ["上升", "下降", "天頂", "天底", "宿命"]:
            if angles_data.get(name) is not None:
                internal_points[name] = {'lon': angles_data[name], 'speed': 0.0}
        
        # 只有當所有備料都齊全時，才製作「福點」這道菜
        if "福點" in planets_to_calculate and all(k in internal_points for k in ["太陽", "月亮", "上升"]):
            sun_lon = internal_points["太陽"]["lon"]
            moon_lon = internal_points["月亮"]["lon"]
            asc_lon = internal_points["上升"]["lon"]
            is_day_chart = (sun_lon - asc_lon + 360) % 360 >= 180
            pof_lon = compute_part_of_fortune(sun_lon, moon_lon, asc_lon, is_day_chart)
            internal_points["福點"] = {'lon': pof_lon, 'speed': 0.0}
        else:
            is_day_chart = False # 預設值

        # 5. 【核心修改】過濾最終輸出結果
        # 準備上菜，只上客戶點的菜
        final_planet_positions = {}
        # 這裡我們遍歷的是客戶的「原始菜單」，而不是廚師的「備料單」
        for name in user_requested_planets:
            if name in internal_points:
                info = internal_points[name]
                house_num, hdeg = find_house(info['lon'], angles_data['cusps'])
                final_planet_positions[name] = {
                    'lon': info['lon'], 'speed': info.get('speed', 0.0), 'house': house_num, 'hdeg': hdeg,
                    'is_retrograde': bool(name in PLANETS_THAT_CAN_RETROGRADE and info.get('speed', 0.0) < 0),
                    'retrograde_label': "逆行" if (name in PLANETS_THAT_CAN_RETROGRADE and info.get('speed', 0.0) < 0) else "",
                    'zodiac_position_formatted': zodiac_format(info['lon'])
                }
        
        # 同樣，相位也只顯示客戶點的星體之間的相位
        all_aspects = list_aspects(internal_points)
        final_aspects = [asp for asp in all_aspects if asp['p1_name'] in user_requested_planets and asp['p2_name'] in user_requested_planets]

        # 6. 回傳結果 (使用與您原始碼完全相同的完整結構)
        return {
            "local_time": local_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "utc_time": utc_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "julian_day_ut": jd_ut, 
            "delta_t_seconds": delta_t_seconds, 
            "julian_day_tt": jd_tt,
            "latitude": latitude, 
            "longitude": longitude,
            "ephemeris_path_status": {"status": "OK", "message": f"星曆檔案路徑已從 {EPHE_PATH_CONFIG} 載入。"},
            "debug_info": {"is_day_chart": is_day_chart},
            "house_cusps": angles_data['cusps'],
            "planet_positions": final_planet_positions,  # 使用已過濾的、只包含使用者所選星體的結果
            "aspects": final_aspects,  # 使用已過濾的、只包含使用者所選星體之間相位的結果
            "chart_image_b64": "placeholder_for_base64_image_string" if generate_image else None,
        }
    except Exception as e:
        app.logger.error(f"計算命盤時發生錯誤: {e}", exc_info=True)
        return {"error": str(e)}
        
def compute_part_of_fortune(sun_lon: float, moon_lon: float, asc_lon: float, is_day: bool) -> float:
    return (asc_lon + moon_lon - sun_lon) % 360 if is_day else (asc_lon + sun_lon - moon_lon) % 360

def find_house(deg: float, cusps_dict: dict):
    if not isinstance(cusps_dict, dict) or len(cusps_dict) < 12:
        return 1, 0.0

    cusps_list = [cusps_dict.get(i, 0.0) for i in range(1, 13)]

    for i in range(1, 13):
        start_cusp = cusps_list[i - 1]
        end_cusp = cusps_list[i % 12]

        d_start, d_end, d_deg = start_cusp, end_cusp, deg
        if d_end < d_start:
            d_end += 360
            if d_deg < d_start:
                d_deg += 360

        if d_start <= d_deg < d_end:
            relative_degree = (deg - start_cusp + 360) % 360
            return i, relative_degree
    app.logger.warning(f"無法為度數 {deg} 找到宮位。預設返回第一宮。宮頭: {cusps_list}")
    return 1, 0.0

def aspect_between(p1_name: str, p2_name: str, lon_a: float, lon_b: float, speed_a: float, speed_b: float):
    diff_current = abs(lon_a - lon_b)
    diff_current = min(diff_current, 360 - diff_current)

    result_aspect = None
    for asp_name, target_angle in ASPECTS.items():
        orb = DEFAULT_ORB.get(asp_name, 3)
        current_deviation = abs(diff_current - target_angle)

        if current_deviation <= orb:
            aspect_type = ""
            is_p1_moving = (p1_name in PLANETS_THAT_CAN_RETROGRADE or p1_name in ["太陽", "月亮"])
            is_p2_moving = (p2_name in PLANETS_THAT_CAN_RETROGRADE or p2_name in ["太陽", "月亮"])
            is_two_fixed_points = (p1_name in FOUR_ANGLES_AND_NODES and p2_name in FOUR_ANGLES_AND_NODES)

            if (is_p1_moving or is_p2_moving) and not is_two_fixed_points:
                dt_factor = 1 / 24
                lon_a_next = (lon_a + speed_a * dt_factor) % 360
                lon_b_next = (lon_b + speed_b * dt_factor) % 360
                diff_next = abs(lon_a_next - lon_b_next)
                diff_next = min(diff_next, 360 - diff_next)
                next_deviation = abs(diff_next - target_angle)
                if next_deviation < current_deviation - 1e-9:
                    aspect_type = "入相"
                elif next_deviation > current_deviation + 1e-9:
                    aspect_type = "出相"
                else:
                    aspect_type = "入相"
            result_aspect = asp_name, current_deviation, aspect_type
            break
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
    res = []
    keys = list(detailed_points_info.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            p1_name, p2_name = keys[i], keys[j]
            p1_info, p2_info = detailed_points_info.get(p1_name), detailed_points_info.get(p2_name)
            if not p1_info or not p2_info: continue

            definitional_oppositions = [
                {"上升", "下降"}, {"天頂", "天底"}, {"北交", "南交"},
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
    return sorted(res, key=lambda item: (ASPECTS.get(item["aspect_name"], 361), item["orb"]))

def list_interchart_aspects(chart1_points: dict, chart2_points: dict):
    res = []
    for p1_name, p1_info in chart1_points.items():
        for p2_name, p2_info in chart2_points.items():
            if not p1_info or 'lon' not in p1_info or not p2_info or 'lon' not in p2_info:
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
    return sorted(res, key=lambda item: (ASPECTS.get(item["aspect_name"], 361), item["orb"]))

def get_planet_overlays_in_houses(source_chart_points: dict, target_chart_cusps: dict):
    overlays = []
    for planet_name in source_chart_points.keys():
        planet_info = source_chart_points.get(planet_name)
        if not planet_info or 'lon' not in planet_info:
            continue
        house_in_target, deg_in_target_house = find_house(planet_info['lon'], target_chart_cusps)
        overlays.append({
            "planet_name": planet_name,
            "zodiac_position_formatted": zodiac_format(planet_info['lon']),
            "retrograde_label": planet_info.get('retrograde_label', ''),
            "house_in_target_chart": house_in_target,
            "degree_in_target_house": deg_in_target_house
        })
    return overlays

# ==============================================================================
# API Routes (API 路由)
# ==============================================================================

# --- API Key Decorator ---
def api_key_required(f):
    """
    一個裝飾器，用於驗證請求中是否包含有效的 API 金鑰。
    金鑰應該放在請求的 Header 中，例如：'X-API-Key: YOUR_SECRET_API_KEY_HERE'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 從請求標頭中獲取 API 金鑰
        provided_key = request.headers.get('X-API-Key')
        
        # 檢查金鑰是否存在且是否與我們設定的相符
        if not provided_key or provided_key != API_KEY:
            app.logger.warning(f"無效的 API 金鑰嘗試: {provided_key}")
            # 如果驗證失敗，返回 403 Forbidden 錯誤
            return jsonify({"error": "未經授權的訪問。請提供有效的 API 金鑰。"}), 403
        
        # 如果金鑰有效，則繼續執行原始的路由函式
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# --- End of API Security ---
# ==============================================================================

# 定義 API 接口 (這段程式碼放在應用程式初始化之後，運行之前)

@app.route('/api/timezones')
def get_timezones():
    """
    提供所有 IANA 時區名稱的 API 接口
    """
    # 將 all_timezones 列表轉換為 JSON 格式回傳
    return jsonify(list(all_timezones)) # 使用上面定義的 all_timezones

@app.route('/')
def index():
    # 這裡會渲染 templates/astro__.html
    return render_template('astro__格子版+指引簡化0905C.html')

# ... (這裡的所有 API 路由，從 /calculate_single_chart 到 /calculate_composite_chart，都保持不變) ...
# ... 我將省略貼上這部分相同的程式碼，請直接從您的 app13.py 複製過來 ...
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

# --- 請用這段新程式碼取代您現有的 calculate_comparison_chart_api 函式 ---
@app.route('/calculate_comparison_chart', methods=['POST'])
def calculate_comparison_chart_api():
    data = request.get_json(force=True)
    try:
        # 接收兩個獨立的星體選項列表
        chart1_optional_planets = data.get('chart1_optional_planets', [])
        chart2_optional_planets = data.get('chart2_optional_planets', [])

        c1_raw = calculate_astrology_chart(
            int(data['chart1_year']), int(data['chart1_month']), int(data['chart1_day']),
            int(data['chart1_hour']), int(data['chart1_minute']),
            float(data['chart1_latitude']), float(data['chart1_longitude']),
            data['chart1_timezone'], chart1_optional_planets) # <-- 傳入 chart1 的選項
        if "error" in c1_raw:
            c1_raw["error_source"] = "chart1"
            app.logger.error(f"比較盤計算錯誤 (命盤A): {c1_raw.get('error', 'N/A')}")
            return jsonify(c1_raw), 400
        
        c2_raw = calculate_astrology_chart(
            int(data['chart2_year']), int(data['chart2_month']), int(data['chart2_day']),
            int(data['chart2_hour']), int(data['chart2_minute']),
            float(data['chart2_latitude']), float(data['chart2_longitude']),
            data['chart2_timezone'], chart2_optional_planets) # <-- 傳入 chart2 的選項
        if "error" in c2_raw:
            c2_raw["error_source"] = "chart2"
            app.logger.error(f"比較盤計算錯誤 (命盤B): {c2_raw.get('error', 'N/A')}")
            return jsonify(c2_raw), 400

        # 因為最終的 inter_aspects 和疊宮數據需要雙方所有星體，
        # 所以這裡我們需要一個合併的列表來確保計算完整性。
        all_planets = list(set(chart1_optional_planets + chart2_optional_planets))
        c1_for_inter_aspects = calculate_astrology_chart(
            int(data['chart1_year']), int(data['chart1_month']), int(data['chart1_day']),
            int(data['chart1_hour']), int(data['chart1_minute']),
            float(data['chart1_latitude']), float(data['chart1_longitude']),
            data['chart1_timezone'], all_planets)

        c2_for_inter_aspects = calculate_astrology_chart(
            int(data['chart2_year']), int(data['chart2_month']), int(data['chart2_day']),
            int(data['chart2_hour']), int(data['chart2_minute']),
            float(data['chart2_latitude']), float(data['chart2_longitude']),
            data['chart2_timezone'], all_planets)

        response_data = {
            "chart_type": "comparison",
            "chart1_data": format_chart_data_for_display(c1_raw),
            "chart2_data": format_chart_data_for_display(c2_raw),
            # 使用包含所有星體的結果來計算跨盤相位和疊宮
            "inter_aspects": list_interchart_aspects(c1_for_inter_aspects['planet_positions'], c2_for_inter_aspects['planet_positions']),
            "chart1_planets_in_chart2_houses": get_planet_overlays_in_houses(c1_for_inter_aspects['planet_positions'], c2_for_inter_aspects['house_cusps']),
            "chart2_planets_in_chart1_houses": get_planet_overlays_in_houses(c2_for_inter_aspects['planet_positions'], c1_for_inter_aspects['house_cusps']),
        }
        return jsonify(response_data)
    except Exception as e:
        app.logger.error(f"後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500
      
# --- 請用這段新程式碼取代您現有的 calculate_transit_chart_api 函式 ---
@app.route('/calculate_transit_chart', methods=['POST'])
def calculate_transit_chart_api():
    data = request.get_json(force=True)
    try:
        # 接收兩個獨立的星體選項列表
        natal_optional_planets = data.get('natal_optional_planets', [])
        transit_optional_planets = data.get('transit_optional_planets', [])

        natal_raw = calculate_astrology_chart(
            int(data['natal_year']), int(data['natal_month']), int(data['natal_day']),
            int(data['natal_hour']), int(data['natal_minute']),
            float(data['natal_latitude']), float(data['natal_longitude']),
            data['natal_timezone'], natal_optional_planets) # <-- 傳入本命盤選項
        if "error" in natal_raw:
            natal_raw["error_source"] = "chart1"
            app.logger.error(f"行運盤計算錯誤 (本命盤): {natal_raw.get('error', 'N/A')}")
            return jsonify(natal_raw), 400
        
        transit_raw = calculate_astrology_chart(
            int(data['transit_year']), int(data['transit_month']), int(data['transit_day']),
            int(data['transit_hour']), int(data['transit_minute']),
            float(data['transit_latitude']), float(data['transit_longitude']),
            data['transit_timezone'], transit_optional_planets) # <-- 傳入行運盤選項
        if "error" in transit_raw:
            transit_raw["error_source"] = "chart2"
            app.logger.error(f"行運盤計算錯誤 (行運盤): {transit_raw.get('error', 'N/A')}")
            return jsonify(transit_raw), 400

        # 為了計算跨盤相位和疊宮，需要一個合併的列表
        all_planets = list(set(natal_optional_planets + transit_optional_planets))
        natal_for_inter_aspects = calculate_astrology_chart(
            int(data['natal_year']), int(data['natal_month']), int(data['natal_day']),
            int(data['natal_hour']), int(data['natal_minute']),
            float(data['natal_latitude']), float(data['natal_longitude']),
            data['natal_timezone'], all_planets)

        transit_for_inter_aspects = calculate_astrology_chart(
            int(data['transit_year']), int(data['transit_month']), int(data['transit_day']),
            int(data['transit_hour']), int(data['transit_minute']),
            float(data['transit_latitude']), float(data['transit_longitude']),
            data['transit_timezone'], all_planets)

        response_data = {
            "chart_type": "transit",
            "natal_chart_data": format_chart_data_for_display(natal_raw),
            "transit_chart_data": format_chart_data_for_display(transit_raw),
            # 使用包含所有星體的結果來計算跨盤相位和疊宮
            "inter_aspects": list_interchart_aspects(natal_for_inter_aspects['planet_positions'], transit_for_inter_aspects['planet_positions']),
            "natal_planets_in_transit_houses": get_planet_overlays_in_houses(natal_for_inter_aspects['planet_positions'], transit_for_inter_aspects['house_cusps']),
            "transit_planets_in_natal_houses": get_planet_overlays_in_houses(transit_for_inter_aspects['planet_positions'], natal_for_inter_aspects['house_cusps']),
        }
        return jsonify(response_data)
    except Exception as e:
        app.logger.error(f"後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500
    
# --- 請用這段新程式碼取代您現有的 calculate_composite_chart_api 函式 ---
@app.route('/calculate_composite_chart', methods=['POST'])
def calculate_composite_chart_api():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "請求中未提供 JSON 數據"}), 400
    try:
        # 接收兩個獨立的星體選項列表，並將其合併為一個
        chart1_optional_planets = data.get('chart1_optional_planets', [])
        chart2_optional_planets = data.get('chart2_optional_planets', [])
        user_requested_planets = list(set(chart1_optional_planets + chart2_optional_planets))

        # 建立一個為了計算基礎盤而必須有的星體列表
        planets_for_base_charts = set(user_requested_planets)
        # 強制性地加入組合盤計算所必需的「上升」和「天頂」
        planets_for_base_charts.update({"上升", "天頂"})
        
        app.logger.info(f"組合盤計算 - 使用者請求: {user_requested_planets}")
        app.logger.info(f"組合盤計算 - 內部基礎盤計算使用: {list(planets_for_base_charts)}")

        # 使用新的列表來計算兩個基礎盤
        c1_raw = calculate_astrology_chart(
            int(data['chart1_year']), int(data['chart1_month']), int(data['chart1_day']),
            int(data['chart1_hour']), int(data['chart1_minute']),
            float(data['chart1_latitude']), float(data['chart1_longitude']),
            data['chart1_timezone'], list(planets_for_base_charts))
        if "error" in c1_raw:
            c1_raw["error_source"] = "chart1"
            return jsonify(c1_raw), 400

        c2_raw = calculate_astrology_chart(
            int(data['chart2_year']), int(data['chart2_month']), int(data['chart2_day']),
            int(data['chart2_hour']), int(data['chart2_minute']),
            float(data['chart2_latitude']), float(data['chart2_longitude']),
            data['chart2_timezone'], list(planets_for_base_charts))
        if "error" in c2_raw:
            c2_raw["error_source"] = "chart2"
            return jsonify(c2_raw), 400
        
        # --- 後續的中點計算邏輯 (大部分不變) ---
        composite_positions_raw = {}
        for name in user_requested_planets:
            if name in c1_raw['planet_positions'] and name in c2_raw['planet_positions'] and name in PLANET_IDS:
                lon1 = c1_raw['planet_positions'][name]['lon']
                lon2 = c2_raw['planet_positions'][name]['lon']
                composite_positions_raw[name] = {'lon': get_midpoint(lon1, lon2), 'speed': 0}

        mc1 = c1_raw['planet_positions']['天頂']['lon']
        mc2 = c2_raw['planet_positions']['天頂']['lon']
        composite_mc_deg = get_midpoint(mc1, mc2)

        asc1 = c1_raw['planet_positions']['上升']['lon']
        asc2 = c2_raw['planet_positions']['上升']['lon']
        composite_asc_deg = get_midpoint(asc1, asc2)

        if '上升' in user_requested_planets:
            composite_positions_raw['上升'] = {'lon': composite_asc_deg, 'speed': 0}
        if '下降' in user_requested_planets:
            composite_positions_raw['下降'] = {'lon': (composite_asc_deg + 180) % 360, 'speed': 0}
        if '天頂' in user_requested_planets:
            composite_positions_raw['天頂'] = {'lon': composite_mc_deg, 'speed': 0}
        if '天底' in user_requested_planets:
            composite_positions_raw['天底'] = {'lon': (composite_mc_deg + 180) % 360, 'speed': 0}
        
        composite_cusps_dict = {i: get_midpoint(c1_raw['house_cusps'][i], c2_raw['house_cusps'][i]) for i in range(1, 13)}
        
        final_composite_positions = {}
        for name, info in composite_positions_raw.items():
            house_num, hdeg = find_house(info['lon'], composite_cusps_dict)
            final_composite_positions[name] = { 'lon': info['lon'], 'speed': 0, 'house': house_num, 'hdeg': hdeg, 'is_retrograde': False, 'retrograde_label': "", 'zodiac_position_formatted': zodiac_format(info['lon']) }

        composite_raw = {
            "local_time": "Composite Chart", "utc_time": "N/A",
            "latitude": (c1_raw['latitude'] + c2_raw['latitude']) / 2, 
            "longitude": get_midpoint(c1_raw['longitude'], c2_raw['longitude']),
            "house_cusps": composite_cusps_dict,
            "planet_positions": final_composite_positions,
            "aspects": list_aspects(final_composite_positions)
        }

        return jsonify({
            "chart_type": "composite",
            "composite_chart_data": format_chart_data_for_display(composite_raw),
            "natal_chart1_data": format_chart_data_for_display(c1_raw),
            "natal_chart2_data": format_chart_data_for_display(c2_raw),
        })
    except Exception as e:
        app.logger.error(f"組合盤後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500
    
# ==============================================================================
# --- NEW: API Endpoint for AI/Gemini Integration ---
# ==============================================================================
@app.route('/api/v1/chart/single', methods=['POST'])
@api_key_required # 使用我們上面定義的裝飾器來保護這個端點
def calculate_single_chart_for_ai():
    """
    這個端點專為 AI 整合設計。
    它直接回傳未經格式化的原始星盤數據 JSON，方便程式解析。
    """
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "請求中未提供 JSON 數據"}), 400
        
    try:
        # 直接呼叫核心計算函式
        raw_chart_data = calculate_astrology_chart(
            int(data['year']), int(data['month']), int(data['day']),
            int(data['hour']), int(data['minute']),
            float(data['latitude']), float(data['longitude']),
            data['timezone'], data.get('optional_planets', []))

        # 檢查計算過程中是否有錯誤，如果有的話直接回傳
        if "error" in raw_chart_data:
            app.logger.error(f"AI API - 單盤計算錯誤: {raw_chart_data['error']}")
            return jsonify(raw_chart_data), 400

        # 成功：直接回傳原始的、未經格式化的 JSON 數據
        return jsonify(raw_chart_data)

    except KeyError as e:
        app.logger.error(f"AI API - 請求中缺少必要欄位: {e}", exc_info=True)
        return jsonify({"error": f"請求的 JSON 中缺少必要欄位: {e}"}), 400
    except Exception as e:
        app.logger.error(f"AI API - 後端發生未知錯誤: {e}", exc_info=True)
        return jsonify({"error": f"伺服器內部錯誤: {e}"}), 500

# --- FIX: 更新主執行區塊 ---
# 這個區塊現在主要用於本地開發測試。
# 在 Render 上，Gunicorn 會直接執行 'app' 物件，不會執行這個區塊的內容。
if __name__ == '__main__':
    # 這裡的日誌主要用於在本地終端機上確認一切正常
    logging.info("應用程式以本地開發模式啟動...")
    # 再次確認星曆檔案路徑是否設定成功
    if EPHE_PATH_CONFIG:
        logging.info(f"確認星曆檔案路徑: {EPHE_PATH_CONFIG}")
        # 啟動 Flask 開發伺服器
        # debug=True 可以在修改程式碼後自動重載
        # host='0.0.0.0' 允許從網路上的其他裝置訪問
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        logging.critical("由於星曆路徑未設定，無法啟動開發伺服器。")