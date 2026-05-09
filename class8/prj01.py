##########################匯入模組###################################
import requests  # 匯入requests套件(用於發送請求)內建json模組
from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk
#############################定義常數###################################
API_KEY = "892da2f13edf3c7f382637760e72d224"  # API金鑰
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"  # API基礎URL
UNITS = "metric"  # 單位(公制)
LANG = "zh_tw"  # 語言(繁體中文)
ICON_BASE_URL = "http://openweathermap.org/img/wn/"  # 天氣圖示URL
temperature = 0
def btn ():
    entry_text = entry.get()  # 取得Entry物件中的文字
    global city_name
    city_name = entry_text  # 將Entry物件中的文字賦值給city_name變數
    ############################主程式###################################
    os.chdir(sys.path[0])  # 設定工作目錄
    # 建立完整的API URL
    send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    print(f"發送的URL: {send_url}")  # 印出完整的API URL
    response = requests.get(send_url)  # 發送請求到API URL
    global temperature
    temperature = response.json()["main"]["temp"]
    info = response.json()  # 將API回傳的JSON資料轉換為Python字典格式
    label3.config(text=f"溫度:{temperature}°C")  # 印出溫度
    label4.config(text=f"天氣描述: {info['weather'][0]['description']}")  # 印出天氣描述
    icon_code = info["weather"][0]["icon"]  # 取得天氣圖示代碼
    # 根據圖標代碼建立圖標下載網址
    icon_code = f"{ICON_BASE_URL}{icon_code}@2x.png"
    image = Image.open("weather.png")  # 使用PIL載入圖片
    img = ImageTk.PhotoImage(image)  # 將PIL Image物件轉換為Tkinter可用的PhotoImage物件
    label2.config(text="",image=img)  # 建立顯示圖片的Label
    label2.image = img  # 防止圖片被垃圾回收機制回收

def on_switch_change():
    ############################主程式###################################
    os.chdir(sys.path[0])  # 設定工作目錄
    # 建立完整的API URL
    send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    change=check_type.get()
    response = requests.get(send_url)  # 發送請求到API URL
    info = response.json()
    if change==True:
        check_label.config(text="(℃)")
        label3.config(text=f"溫度:{temperature}°C")  # 印出溫度
    else:
        check_label.config(text="(℉)")
        label3.config(text=f"溫度:{temperature*9/5+32}°F")  # 印出溫度
#######################建立視窗########################
# 創建主視窗
window = Tk()  # 創建視窗
window.title("hi")  # 設定視窗標題
###################設定字體########################
font_size = 20  # 設定字體大小
window.option_add("*Font", ("Helvetica", font_size))
# 設定預設字型,這裡設定為Helvetica,字體大小為30
label = Label(window, text="請輸入想搜尋的城市")  # 建立標籤
label.grid(row=0, column=0, padx=10, pady=10)  # 放置標籤
entry = Entry(window, width=30)  # 建立Entry物件
entry.grid(row=0, column=1, padx=10, pady=10)  # 放置Entry物件
btn=Button(window, text="獲得天氣資訊",command=btn)  # 建立標籤
btn.grid(row=0, column=2, padx=10, pady=10)  # 放置標籤
label2 = Label(window, text="天氣圖示")  # 建立標籤
label2.grid(row=1, column=0, padx=10, pady=10)  # 放置標籤
label3 = Label(window, text="溫度?℃")  # 建立標籤
label3.grid(row=1, column=1, padx=10, pady=10)  # 放置標籤
label4 = Label(window, text="天氣描述?")  # 建立標籤
label4.grid(row=1, column=2, padx=10, pady=10)  # 放置標籤
check_label = Label(window, text="(℃/℉)")  # 建立標籤
check_label.grid(row=2, column=1, padx=10, pady=10)  # 放置標籤
check_type = BooleanVar()
check_type.set(True)  # 設定預設值為True
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)  # 建立Checkbutton
check.grid(row=2, column=0,columnspan=2, padx=10, pady=10)  # 放置Checkbutton
window.mainloop()  # 啟動視窗
