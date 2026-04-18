########################匯入模組############################
from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk
from tkinter import filedialog


###################定義函式########################
def open_file():
    global file_path
    # 選擇檔案,initialdir參數設定初始目錄,這裡設定為程式所在目錄
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])
    label2.config(text=file_path)  # 顯示檔名


def show_image():
    global file_path
    image = Image.open(file_path)  # 使用PIL載入圖片
    # 為了讓它適合畫布,要調整大小
    # Image.LANCZOS是用來縮放圖片,它會使用高品質的重採樣濾鏡來保持圖片的清晰度和細節
    image = image.resize(
        (canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS
    )  # 調整圖片大小
    # 將PIL Image物件轉換為Tkinter可用的PhotoImage物件
    photo = ImageTk.PhotoImage(image)
    # 在畫布上顯示圖片,並指定圖片對齊左上角
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.image = photo  # 防止圖片被垃圾回收


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
label = Label(Window, text="選擇檔案:")  # 建立標籤
label.grid(row=0, column=0, sticky="E")  # sticky="E"靠右對齊

label2 = Label(Window, text="無")  # 建立標籤
label2.grid(row=0, column=1, sticky="E")  # sticky="E"靠右對齊
###########################建立按鈕###########################
button = Button(Window, text="瀏覽", command=open_file, style="my.TButton")  # 建立按鈕
button.grid(row=0, column=2, sticky="W")  # 放置按鈕
button2 = Button(
    Window, text="顯示", command=show_image, style="my.TButton"
)  # 建立按鈕
button2.grid(row=1, column=0, columnspan=3, sticky="EW")  # 放置按鈕

###########################建立畫布###########################
canvas = Canvas(Window, width=600, height=600, bg="#FFFFFF")  # 建立畫布
canvas.grid(row=2, column=0, columnspan=3)  # 放置畫布
#################################################
Window.mainloop()  # 啟動視窗
