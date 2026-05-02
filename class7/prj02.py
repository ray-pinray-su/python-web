#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk

os.chdir(sys.path[0])  # 設定工作目錄


#######################定義函數########################
def on_switch_change():
    # 當Checkbutton的狀態改變時,呼叫此函數更新check_label的文字為check_type的值
    check_label.config(text=str(check_type.get()))


#########################建立視窗########################
# 創建主視窗
window = Tk()  # 創建視窗
window.title("Checkbutton")  # 設定視窗標題
####################### 設定字體########################
# 設定全域預設字形
font_size = 20  # 設定字體大小
window.option_add(
    "*Font", ("Helvetica", font_size)
)  # 設定預設字型,這裡設定為Helvetica,字體大小為20
#####################設定主題#####################
style = Style(theme="darkly")  # 設定主題為darkly
# 設定按鈕與Checkbutton的字型樣式
style.configure("my.TButton", font=("Helvetica", font_size))  # 設定按鈕字型
style.configure("my.TCheckbutton", font=("Helvetica", font_size))  # 設定Checkbutton字型
#########################建立變數########################
# BooleanVar()是tkinter/ttk提供的一種特殊變數類型,用於存儲布林值(True或False)
check_type = BooleanVar()
check_type.set(True)  # 設定預設值為True
############################建立標籤########################
# 建立標籤,用於顯示Checkbutton的狀態
check_label = Label(window, text="True")  # 建立標籤
#######################運行應用程式########################
# 將標籤放到視窗中的指定位置
check_label.grid(row=1, column=2, padx=10, pady=10)  # 放置標籤
# 新增image label
image = Image.open("weather.png")  # 使用PIL載入圖片
img = ImageTk.PhotoImage(image)  # 將PIL Image物件轉換為Tkinter可用的PhotoImage物件
img_label = Label(window, image=img)  # 建立顯示圖片的Label
img_label.grid(row=2, column=1, columnspan=2, padx=10, pady=10)  # 放置圖片Label
img_label.image = img  # 防止圖片被垃圾回收機制回收
#########################建立Checkbutton#########################
# Checkbutton會和Check_type綁在一起
# 當Checkbutton被點擊時,check_type的值會自動更新為True或False並在狀態改變時呼叫on_switch_change函數
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)  # 建立Checkbutton
check.grid(row=1, column=1, padx=10, pady=10)  # 放置Checkbutton
############################運行應用程式########################
window.mainloop()  # 啟動視窗
