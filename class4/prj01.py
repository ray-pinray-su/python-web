#######################匯入模組#######################
from tkinter import *
from PIL import Image, ImageTk
import os
import sys

#########################設定工作目錄########################
# 設定工作目錄
os.chdir(sys.path[0])


#######################定義函數###########################
# 定義一個函數,用來處理按下按鍵時要做的事情
def move_circle(event):
    # 取得按下的鍵
    key = event.keysym
    print(key)  # 印出按下的鍵
    if key == "Up":  # 如果按下的是上鍵
        canvas.move(circle, 0, -10)  # 將圓形往上移動10像素
    if key == "Down":  # 如果按下的是下鍵
        canvas.move(circle, 0, 10)  # 將圓形往下移動10像素
    if key == "Left":  # 如果按下的是左鍵
        canvas.move(circle, -10, 0)  # 將圓形往左移動10像素
    if key == "Right":  # 如果按下的是右鍵
        canvas.move(circle, 10, 0)  # 將圓形往右移動10像素
    if key == "w":  # 如果按下的是w鍵
        canvas.move(reck, 0, -10)  # 將矩形往上移動10像素
    if key == "s":  # 如果按下的是s鍵
        canvas.move(reck, 0, 10)  # 將矩形往下移動10像素
    if key == "a":  # 如果按下的是a鍵
        canvas.move(reck, -10, 0)  # 將矩形往左移動10像素
    if key == "d":  # 如果按下的是d鍵
        canvas.move(reck, 10, 0)  # 將矩形往右移動10像素


#######################建立視窗########################
# 創建主視窗
window = Tk()
# 設定主視窗標題
window.title("my first GUI")
######################創建畫布#########################
# 創建畫布，並指定畫布的寬度為600像素，高度為600像素，背景色為白色
canvas = Canvas(window, width=600, height=600, bg="#FFFFFF")
# 將畫布放置在視窗中
canvas.pack()
########################設定視窗圖片#########################
# 設定視窗圖片
window.iconbitmap("cat.jpg")
####################載入圖片#########################
# 原始方法tkinter內建PhotoImage,只支援PNG,GIF,PGM,PPM格式(不支援JPG,BMP等格式)
# tkinter內建PhotoImage,只支援PNG,GIF,PGM,PPM格式(不支援JPG,BMP等格式)
# img = PhotoImage(file="crocodile2.png")
# Pillow方式 使用Image.open()載入圖片
# 好處:
# 1.支援幾乎所有圖片格式(如JPG,BMP等)
# 2.提供更多圖片處理功能(如調整大小、旋轉等)
image = Image.open("cat.jpg")
# 將PIL Image物件轉換為Tkinter可用的PhotoImage物件
img = ImageTk.PhotoImage(image)
#####################顯示圖片#########################
# 在畫布上顯示圖片，並指定圖片的中心點座標為(300,300)
my_img = canvas.create_image(300, 300, image=img)
######################畫圖形########################
# 在畫布上畫一個圓形,起始位置為(250,150),結束位置為(300,200),填充顏色為紅色
circle = canvas.create_oval(250, 150, 300, 200, fill="red")
# 在畫布上畫一個矩形,起始位置為(220,400),結束位置為(340,430),填充顏色為藍色
reck = canvas.create_rectangle(220, 290, 340, 320, fill="blue")
# 在畫布上顯示一段文字,位置為(300,100),文字為cat,顏色為黑色,字型為Arial,大小為30
msg = canvas.create_text(300, 100, text="cat", fill="black", font=("Arial", 30))
#####################綁定按鍵事件
# 將按鍵事件綁定到畫布,當按下指定的按鍵時,移動對應的物件
canvas.bind_all("<Key>", move_circle)

#######################運行應用程式############################
window.mainloop()
