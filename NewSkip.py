import threading
import keyboard
import time, sys, ctypes
import win32gui, win32con
from random import random

GAME_NAME = "原神"
DELAY_SECONDS = 2 + 0.3 * random()
# 1600x900 resolution
X_OFFSET = 1200
Y_OFFSET = 700


class LoopThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__running = True
        self.__paused = True
        self.__handle = self.get_handle()

    def run(self):
        while True:
            if not self.__running:
                break
            if not self.__paused:
                print("Clicking...")
                self.set_foreground()
                self.click_pos()
        return

    def get_handle(self):
        window_handle = win32gui.FindWindow(None, GAME_NAME)
        return window_handle
    
    def check_handle(self):
        if not self.__handle:
            self.__handle = self.get_handle()

    def get_rect(self):
        window_rect = win32gui.GetWindowRect(self.__handle)
        xx, yy = window_rect[0] + X_OFFSET, window_rect[1] + Y_OFFSET
        return xx, yy
    
    def click_pos(self):
        xx, yy = self.get_rect()
        print(f"xx = '{xx}', yy = '{yy}'")
        ctypes.windll.user32.SetCursorPos(xx, yy)
        ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xx, yy, 0, 0)
        ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTUP, xx, yy, 0, 0)
        time.sleep(DELAY_SECONDS)

    def set_foreground(self):
        ctypes.windll.user32.ShowWindow(self.__handle, win32con.SW_RESTORE)
        ctypes.windll.user32.SetForegroundWindow(self.__handle)
        time.sleep(1)

    def start_loop(self):
        if self.__paused:
            print("Click Started.")
            self.__paused = False
        else:
            print("Click Paused.")
            self.__paused = True

    def stop_loop(self):
        if self.__running:
            print("Program Quit.")
            self.__running = False

def stop_click():
    loop_thread.stop_loop()
    loop_thread.join()

def start_click():
    loop_thread.start_loop()

keyboard.add_hotkey('n', stop_click)
keyboard.add_hotkey('k', start_click)

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('Admin, running...')
        loop_thread = LoopThread()
        loop_thread.start()
        keyboard.wait('n')
    else:
        print('Not Admin, restart')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)