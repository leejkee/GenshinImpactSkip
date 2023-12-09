import threading
import keyboard
import time, sys, ctypes
# import pyautogui
import win32gui, win32con
from random import random

class LoopThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__running = True
        self.__paused = True
        self.__handle = self.get_handle()

    def run(self):
        while True:
            if self.__running:
                if not self.__paused:
                    print("Clicking...")
                    self.setForground()
                    xx, yy = self.get_rect()
                    print(f"xx = '{xx}', yy = '{yy}'")
                    # pyautogui.click(xx, yy)
                    ctypes.windll.user32.SetCursorPos(xx, yy)
                    ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, xx, yy, 0, 0)
                    ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTUP, xx, yy, 0, 0)
                    time.sleep(2 + 0.2 * random())
            else:
                break

    def get_handle(self):
        window_handle = win32gui.FindWindow(None, "原神")
        return window_handle
    
    def check_handle(self):
        if not self.__handle:
            self.__handle = self.get_handle()

    def get_rect(self):
        window_rect = win32gui.GetWindowRect(self.__handle)
        xx, yy = window_rect[0] + 1200, window_rect[1] + 700
        return xx, yy

    def setForground(self):
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


def on_key_event(dummy_arg=None):
    if keyboard.is_pressed('n'):
        loop_thread.stop_loop()
        loop_thread.join()
        sys.exit(0)

    if keyboard.is_pressed('k'):
        loop_thread.start_loop()

keyboard.add_hotkey('n', on_key_event)
keyboard.add_hotkey('k', on_key_event)

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() :
        print('Admin, running...')
        loop_thread = LoopThread()
        loop_thread.start()
        keyboard.wait()
    else:
        print('Not Admin, restart')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)