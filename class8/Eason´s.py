from ttkbootstrap import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

# OpenWeather API KEY
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANGU = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

# 目前溫度（攝氏）
current_temp_c = 0


# ===== 查詢天氣 =====
def get_weather():

    global current_temp_c

    city = city_entry.get()

    if city == "":
        temp_label.config(text="請輸入城市")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"

    data = requests.get(url).json()

    if data["cod"] == 200:

        # 攝氏溫度
        current_temp_c = data["main"]["temp"]

        # 描述
        desc = data["weather"][0]["description"]

        # 圖標代碼
        icon_code = data["weather"][0]["icon"]

        # 圖標網址
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

        # 下載圖片
        response = requests.get(icon_url)

        # 轉圖片
        image_data = Image.open(BytesIO(response.content))

        # tkinter圖片格式
        photo = ImageTk.PhotoImage(image_data)

        # 顯示圖片
        icon_label.config(image=photo)
        icon_label.image = photo

        # 顯示溫度
        update_temperature()

        # 顯示描述
        desc_label.config(text=f"描述: {desc}")

    else:
        temp_label.config(text="找不到城市")
        desc_label.config(text="")
        icon_label.config(image="")


# ===== 更新溫度 =====
def update_temperature():

    # 如果勾選 -> 華氏
    if temp_var.get():

        f = (current_temp_c * 9 / 5) + 32
        temp_label.config(text=f"溫度: {f:.1f}°F")

    # 否則 -> 攝氏
    else:

        temp_label.config(text=f"溫度: {current_temp_c:.1f}°C")


# ===== 建立視窗 =====
window = Window(themename="minty")
window.title("Weather App")
window.columnconfigure(1, weight=1)

style = window.style
style.configure("Weather.TLabel", font=("微軟正黑體", 24))
style.configure("Weather.TEntry", font=("微軟正黑體", 24))
style.configure("Weather.TButton", font=("微軟正黑體", 22))
style.configure("Weather.TCheckbutton", font=("微軟正黑體", 18))

city_label = Label(
    window,
    text="請輸入想搜尋的城市：",
    style="Weather.TLabel",
)
city_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="w")

city_entry = Entry(window, width=20, style="Weather.TEntry")
city_entry.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="ew")

search_button = Button(
    window,
    text="獲得天氣資訊",
    style="Weather.TButton",
    command=get_weather,
)
search_button.grid(row=0, column=2, padx=(10, 20), pady=(20, 10))

# 天氣圖片
icon_label = Label(window)
icon_label.grid(row=1, column=0, padx=20, pady=20)

# 溫度
temp_label = Label(
    window,
    text="溫度: ?°C",
    style="Weather.TLabel",
)
temp_label.grid(row=1, column=1, padx=20, pady=20)

# 描述
desc_label = Label(window, text="描述: ?", style="Weather.TLabel")
desc_label.grid(row=1, column=2, padx=20, pady=20)

# 勾選變數
temp_var = BooleanVar()

# 勾選框
check = Checkbutton(
    window,
    text="切換成華氏溫度 °F",
    variable=temp_var,
    style="Weather.TCheckbutton",
    command=update_temperature,
)
check.grid(row=2, column=0, columnspan=3, pady=(0, 20))

# 啟動
window.mainloop()