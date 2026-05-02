##########################匯入模組###################################
import requests  # 匯入requests套件(用於發送請求)內建json模組

############################定義常數###################################
API_KEY = "892da2f13edf3c7f382637760e72d224"  # API金鑰
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"  # API基礎URL
UNITS = "metric"  # 單位(公制)
LANG = "zh_tw"  # 語言(繁體中文)
############################主程式###################################
city_name = input("請輸入城市名稱:")  # 從使用者輸入城市名稱
# 建立完整的API URL
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"

print(f"發送的URL: {send_url}")  # 印出完整的API URL
response = requests.get(send_url)  # 發送請求到API URL
info = response.json()  # 將API回傳的JSON資料轉換為Python字典格式
# 處理和顯示天氣資訊
if info["cod"] != "404":  # 如果API回傳的狀態碼不是404(表示城市存在)
    temperature = info["main"]["temp"]  # 取得主要天氣資訊
    weather = info["weather"][0]["description"]  # 取得天氣描述(列表中的第一個元素)
    print(f"城市: {city_name}")  # 印出城市名稱
    print(f"溫度:{ temperature}°C")  # 印出溫度
    print(f"天氣描述: {weather}")  # 印出天氣描述
