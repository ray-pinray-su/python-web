#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os

#######################定義函數########################
#########################建立視窗########################
# 創建主視窗
Window = Tk()  # 創建視窗
Window.title("Checkbutton")  # 設定視窗標題
####################### 設定字體########################
font_size = 20  # 設定字體大小
Window.option_add(
    "*Font", ("Helvetica", font_size)
)  # 設定預設字型,這裡設定為Helvetica,字體大小為20
#####################設定主題#####################
style = Style(theme="minty")  # 設定主題為minty
# 設定按鈕與Checkbutton的字型樣式
style.configure("my.TButton", font=("Helvetica", font_size))  # 設定按鈕字型
style.configure("my.TCheckbutton", font=("Helvetica", font_size))  # 設定Checkbutton字型

#######################運行應用程式########################
