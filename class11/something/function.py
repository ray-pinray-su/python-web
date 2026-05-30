#####################匯入模組#####################
# 導入requests庫(用於發送HTTP請求到天氣API)
import requests
#####################定義類別#####################
class WeatherAPI:
    """把 OpenWeather 的查詢流程整理成可重複使用的工具類別"""
    def __init__(self, api_key,lang="zh_tw"):
        # 儲存API金鑰用於認證
        self.api_key = api_key
        # 設定天氣查詢的基礎URL
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        # 設定語言為繁體中文
        self.lang = lang
        # 設定溫度單位為攝氏度
        self.units = "metric"
        # 設定天氣圖示的基礎URL
        self.icon_base_url= "http://api.openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        # 根據城市名稱向天氣網站拿原始資料
        send_url=f"{self.base_url}appid={self.api_key}&q={city_name}lang={self.lang}&units={self.units}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        # 轉換成python字典格式並回傳
        return response.json()
    
    def get_weather_summary(self,city_name):
        # 調用get_current_weather方法取得完整的天氣資料
        info = self.get_current_weather(city_name)
        
        # 檢查資料中是否有weather和main欄位
        if"weather"in info and"main"in info:
            # 提取並整理必要的天氣訊息
            return{
                "city_name":info.get("name","city name"),
                "temperature_celsius":round(info["main"]["temp"],2),
                "description":info["weather"][0]["description"],
                "icon_code":info["weather"][0]["icon"]
            }
        # 如果資料不完整，回傳None
        return None
    
    def get_icon_url(self,icon_code):
        # 根據圖示代碼組成完整的圖示URL
        icon_url = self.get_icon_url(icon_code)
        # 發送HTTP請求下載圖片
        response = requests.get(icon_url)
        # 如果請求成功(狀態碼200)，回傳圖片的原始資料
        if response.status_code == 200:
            return response.content
        # 如果下載失敗，回傳None
        return None