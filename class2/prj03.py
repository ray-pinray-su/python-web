#######################匯入模組#######################
from tkinter import *
import random as r


#######################定義函數########################
def say_hi():
    # 顯示"hi",並選擇一種顏色
    fg_color = "#" + "".join([r.choice("0123456789abcdef") for i in range(6)])
    """"
    比對展開寫法
    fg_color = "#"
    for i in range(6):
        fg_color += r.choice("0123456789abcdef")
    """
    bg_color = "#" + "".join([r.choice("0123456789abcdef") for i in range(6)])
    display.config(
        text="                                            hi                                                 ",
        fg=fg_color,
        bg=bg_color,
    )


#######################建立視窗########################
# 創建主視窗
window = Tk()
# 設定主視窗標題
window.title("my first GUI")
############################建立按鈕########################
# 創建按鈕，並指定按下按鈕後要執行say_hi函數
btn1 = Button(window, text="show screen", command=say_hi)
# 將按鈕放置在視窗中
btn1.pack()
#########################建立標籤########################
# 創建標籤，並指定要顯示"hello world",前景色為紅色，背景為黑色
# Label參數說明:(視窗名稱, text=文字內容, fg=前景顏色, bg=背景顏色)
display = Label(window, text="")
# 將標籤放置在視窗中
display.pack()
#######################運行應用程式########################
window.mainloop()
