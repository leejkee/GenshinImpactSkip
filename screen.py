# 像素坐标显示
import pyautogui
from PIL import ImageGrab
from tkinter import Tk, Canvas, Label, PhotoImage

def get_pixel_color(x, y):
    screenshot = ImageGrab.grab()
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color

def update_pixel_coordinates():
    x, y = pyautogui.position()
    pixel_color = get_pixel_color(x, y)
    pixel_coordinates_label.config(text=f"({x}, {y}) - Color: {pixel_color}")

    # 更新像素坐标显示
    root.after(100, update_pixel_coordinates)

# 创建GUI窗口
root = Tk()
root.title("实时显示鼠标像素坐标")

# 创建Canvas用于显示截图
canvas = Canvas(root, width=400, height=300)
canvas.pack()

# 创建Label用于显示像素坐标信息
pixel_coordinates_label = Label(root, text="", font=("Helvetica", 12))
pixel_coordinates_label.pack()

# 更新像素坐标
update_pixel_coordinates()

# 运行Tkinter主循环
root.mainloop()
