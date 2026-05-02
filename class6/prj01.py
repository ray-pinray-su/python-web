#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os

######################設定工作目錄########################
os.chdir(sys.path[0])  # 設定工作目錄


#######################定義函數########################
def show_result():
    entry_text = entry.get()  # 取得Entry物件中的文字
    try:
        result = eval(entry_text)  # 計算文字中的數學表達式
    except:
        result = "錯誤"  # 如果計算失敗,顯示錯誤訊息
    label.config(text=str(result))  # 顯示計算結果


#######################建立視窗########################
# 創建主視窗
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
#######################運行應用程式########################
#######################建立標籤########################
label = Label(Window, text="計算結果")  # 建立標籤
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)  # 放置標籤
########################建立按鈕#########################
# 顯示計算結果
button = Button(
    Window, text="顯示計算結果", command=show_result, style="my.TButton"
)  # 建立按鈕
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)  # 放置按鈕
##########################建立Entry物件#######################
# Entry物件
entry = Entry(Window, width=30)  # 建立Entry物件
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # 放置Entry物件
# padx,pady為元件與元件之間的間距
Window.mainloop()  # 啟動視窗
