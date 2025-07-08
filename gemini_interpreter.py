# gemini_interpreter.py
import os
import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv
import google.api_core.exceptions
import argparse

# 從 .env 檔案載入環境變數
load_dotenv()


# ==============================================================================
# --- 組態設定 (Configuration) ---
# ==============================================================================

# 當您要呼叫部署在 Render 上的服務時，請將此 URL 換成您的 Render 服務網址。
# 您的 Render 網址格式通常是： https://your-app-name.onrender.com
# 請將 'astro-chart-to-text' 換成您在 Render 上的真實服務名稱
# 修正：指向正確的 AI API 端點
ASTRO_API_URL = "https://astro-chart-to-text.onrender.com/api/v1/chart/single"

# 從環境變數讀取您的金鑰 (現在會由 .env 檔案提供)
ASTRO_API_KEY = os.getenv("ASTRO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not ASTRO_API_KEY:
    raise ValueError("錯誤：請在 .env 檔案中設定 ASTRO_API_KEY。")

if not GEMINI_API_KEY:
    raise ValueError("錯誤：請在 .env 檔案中設定 GEMINI_API_KEY。")

# 設定 Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================================
# --- 核心函式 (Core Functions) ---
# ==============================================================================

def get_chart_data_from_api(payload):
    """呼叫您的星盤 API 並回傳 JSON 數據"""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ASTRO_API_KEY
    }
    # 根據 URL 動態判斷是本地還是雲端，讓日誌更清晰
    api_location = "雲端" if "onrender.com" in ASTRO_API_URL else "本地"
    print(f"1. 正在向您的{api_location}星盤 API ({ASTRO_API_URL}) 發送請求...")
    response = requests.post(ASTRO_API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status() # 確保請求成功
    print("   ✅ 成功獲取星盤數據！")
    return response.json()



def get_interpretation_from_gemini(chart_data, custom_question=None):
    """將星盤數據發送給 Gemini 並獲取解讀"""
    
    # --- 動態提示工程 (Dynamic Prompt Engineering) ---
    if custom_question:
        # 如果使用者提供了特定問題，使用這個更直接的提示
        prompt = f"""
        你是一位專業的占星師。請根據以下提供的 JSON 格式的星盤數據，用清晰、易懂的方式回答使用者的問題。

        使用者的問題: "{custom_question}"

        ---
        星盤數據:
        ```json
        {json.dumps(chart_data, indent=2, ensure_ascii=False)}
        ```
        ---
        """
    else:
        # 如果沒有特定問題，則使用一個更開放、更鼓勵深入分析的提示
        prompt = f"""
        你是一位智慧、溫暖且富有洞察力的占星大師。你的任務是根據以下提供的 JSON 格式的個人星盤數據，為使用者提供一份全面、深入且整合的個性分析。

        請不要只是條列式地解釋單一配置。請將星盤視為一個整體，自由地探索其中最顯著的模式、天賦潛能、以及內在的挑戰與成長課題。你可以從核心的「三巨頭」（太陽、月亮、上升）出發，但更重要的是，請將它們與其他行星、宮位和關鍵相位（特別是容許度小的相位）聯繫起來，編織成一個連貫、深刻的生命故事。

        請用充滿人文關懷且啟發人心的語氣，以流暢、自然的散文形式呈現你的分析。


        ---
        星盤數據:
        ```json
        {json.dumps(chart_data, indent=2, ensure_ascii=False)}
        ```
        ---
        """
    
    print("\n2. 正在將星盤數據和提示發送給 Gemini API...")
    model = genai.GenerativeModel('gemini-1.5-flash') # 您也可以試試 'gemini-1.5-pro'
    response = model.generate_content(prompt)
    # 新增：檢查 Gemini 是否有回傳內容
    if not response.parts:
        print("   ⚠️ Gemini API 回應為空，可能是因為內容安全設定。")
        if response.prompt_feedback:
            print(f"   提示回饋: {response.prompt_feedback}")
        return "無法從 Gemini 獲取有效的解讀。"
    print("   ✅ 成功從 Gemini 獲取分析結果！")

    return response.text

def parse_arguments():
    """使用 argparse 解析命令列參數"""
    parser = argparse.ArgumentParser(
        description="從您的占星 API 獲取數據並由 Gemini 進行解讀。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # 顯示預設值
    )
    
    parser.add_argument("--year", type=int, default=1990, help="出生年份 (YYYY)")
    parser.add_argument("--month", type=int, default=1, help="出生月份 (1-12)")
    parser.add_argument("--day", type=int, default=1, help="出生日期 (1-31)")
    parser.add_argument("--hour", type=int, default=12, help="出生小時 (0-23)")
    parser.add_argument("--minute", type=int, default=30, help="出生分鐘 (0-59)")
    parser.add_argument("--lat", type=float, default=25.09, help="緯度 (+N / -S)")
    parser.add_argument("--lon", type=float, default=121.52, help="經度 (+E / -W)")
    parser.add_argument("--tz", type=str, default="Asia/Taipei", help="時區 (例如: 'Asia/Taipei')")
    parser.add_argument("--planets", nargs='*', default=["凱龍", "莉莉絲", "福點"], help="要計算的額外星體列表 (例如: --planets 凱龍 穀神)")
    parser.add_argument("-q", "--question", type=str, help="向 Gemini 提出一個關於此星盤的特定問題。")

    return parser.parse_args()

# ==============================================================================
# --- 主執行區塊 (Main Execution) ---
# ==============================================================================

if __name__ == "__main__":
    args = parse_arguments()

    # 從解析的參數建立 payload
    chart_payload = {
        "year": args.year, "month": args.month, "day": args.day,
        "hour": args.hour, "minute": args.minute,
        "latitude": args.lat, "longitude": args.lon,
        "timezone": args.tz, "optional_planets": args.planets
    }

    try:
        # 步驟 1: 從您的 API 獲取星盤數據
        astro_data = get_chart_data_from_api(chart_payload)
        
        # 步驟 2: 將數據和您的問題（如果有的話）交給 Gemini 進行解讀
        interpretation = get_interpretation_from_gemini(astro_data, custom_question=args.question)
        
        # 步驟 3: 印出最終結果
        print("\n" + "="*60)
        if args.question:
            print(f"✨ 對於問題「{args.question}」的分析結果 ✨")
        else:
            print("✨ Gemini 占星大師的分析結果 ✨")
        print("="*60)
        print(interpretation)

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ 您的星盤 API 回應錯誤: {e.response.status_code}")
        print(f"   回應內容: {e.response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 錯誤：無法連接到您的本地星盤 API。請確認 app.py 正在運行。")
        print(f"   詳細資訊: {e}")
    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"\n❌ Gemini API 呼叫失敗: {e}")
    except ValueError as e:
        # 捕捉我們自己拋出的 ValueError，例如找不到 API 金鑰
        print(f"\n❌ 設定錯誤: {e}")
    except Exception as e:
        print(f"\n❌ 發生未知錯誤: {e}")

