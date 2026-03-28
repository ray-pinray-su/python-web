#######################匯入模組#######################
from tkinter import *
from PIL import Image, ImageTk
import os
import sys

#########################設定工作目錄########################
# 設定工作目錄
os.chdir(sys.path[0])
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
#######################運行應用程式############################
window.mainloop()
