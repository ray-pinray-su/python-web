#######################匯入模組#######################
from tkinter import *


#######################定義函數########################
def say_hi():
    display.config(text="hi", fg="red", bg="black")


# 定義清除畫面函數,將標籤文字設為空字串，前景色和背景色都設為透明
def clear():
    display.config(text="", fg=window.cget("bg"), bg=window.cget("bg"))


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
btn2 = Button(window, text="clear screen", command=clear)
# 將按鈕放置在視窗中
btn2.pack()
#########################建立標籤########################
# 創建標籤，並指定要顯示"hello world",前景色為紅色，背景為黑色
# Label參數說明:(視窗名稱, text=文字內容, fg=前景顏色, bg=背景顏色)
display = Label(window, text="")
# 將標籤放置在視窗中
display.pack()
#######################運行應用程式########################
window.mainloop()
