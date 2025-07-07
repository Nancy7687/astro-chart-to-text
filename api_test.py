# api_test.py
import requests
import json
import os
from dotenv import load_dotenv

# 從 .env 檔案載入環境變數
load_dotenv()

# --- 設定 ---
# 如果您是在本機測試，URL 就是 http://127.0.0.1:5000
# 如果您已經部署到雲端，請換成您的雲端 URL
API_URL = "http://127.0.0.1:5000/api/v1/chart/single"

# 從環境變數讀取金鑰
YOUR_API_KEY = os.getenv("ASTRO_API_KEY")
if not YOUR_API_KEY:
    raise ValueError("錯誤：請在 .env 檔案中設定 ASTRO_API_KEY。")

# 要計算的星盤資料
chart_payload = {
    "year": 1990,
    "month": 1,
    "day": 1,
    "hour": 12,
    "minute": 30,
    "latitude": 25.09,
    "longitude": 121.52,
    "timezone": "Asia/Taipei",
    "optional_planets": ["凱龍", "莉莉絲", "福點"]
}

# 設定請求標頭 (Headers)
headers = {
    "Content-Type": "application/json",
    "X-API-Key": YOUR_API_KEY  # 這是您用來驗證的 API 金鑰
}

# --- 執行請求 ---
try:
    print(f"正在向 {API_URL} 發送請求...")
    response = requests.post(API_URL, headers=headers, data=json.dumps(chart_payload))

    # 檢查回應狀態碼
    response.raise_for_status()  # 如果狀態碼不是 2xx，這會引發一個錯誤

    # 解析並印出回應的 JSON 數據
    chart_data = response.json()
    print("\n✅ 成功從您的 API 獲取星盤數據！")
    print("="*50)
    # 使用 json.dumps 進行美化輸出
    print(json.dumps(chart_data, indent=2, ensure_ascii=False))
    print("="*50)

except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP 錯誤: {http_err}")
    print(f"狀態碼: {http_err.response.status_code}")
    print(f"回應內容: {http_err.response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"❌ 請求錯誤: {req_err}")
except Exception as e:
    print(f"❌ 發生未知錯誤: {e}")

