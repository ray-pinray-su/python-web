########################匯入模組############################
from ttkbootstrap import *
import sys
import os


###################定義函式########################
def test():
    print("")


##################建立視窗###########################
Window = Tk()  # 創建視窗
Window.title("hi")  # 設定視窗標題
###################設定字體########################
font_size = 30  # 設定字體大小
Window.option_add("*Font", ("Helvetica", font_size))
# 設定預設字型,這裡設定為Helvetica,字體大小為30
#####################設定主題#####################
style = Style(theme="darkly")  # 設定主題為darkly
# "my.TButton"的命名邏輯:
# 就像幫東西貼標籤一樣,分成兩個部分,用[.]隔開
#   前半段"my"  ->自己取名子,可以換成任何名子,例如"big","red"等等
#   後半段"TButton" -> 固定寫法,代表[按鈕]這種元件
#                     T是Ttk(一種按鈕工具箱)的縮寫
#                     就像[T恤]的T一樣,是品牌名稱的開頭
# 常見元件的後半段寫法:
#   按鈕 -> TButton
#   標籤 -> TLabel
#   輸入框 -> TEntry
style.configure("my.TButton", font=("Helvetica", font_size))  # 設定按鈕字型
###########################建立標籤###########################
label = Label(Window, text="Hello World")  # 建立標籤
label.grid(row=0, column=0, sticky="E")  # sticky="E"靠右對齊
###########################建立按鈕###########################
button = Button(Window, text="Click Me", command=test, style="my.TButton")  # 建立按鈕
button.grid(row=0, column=1, sticky="W")  # 放置按鈕
button2 = Button(Window, text="lick me", command=test, style="my.TButton")  # 建立按鈕
button2.grid(row=1, column=0, columnspan=2, sticky="EW")  # 放置按鈕
#################################################
Window.mainloop()  # 啟動視窗
