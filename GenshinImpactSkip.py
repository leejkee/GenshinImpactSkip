import threading
import keyboard
import time, sys, ctypes
import pyautogui
import win32gui, win32con
from random import random
def setForground(handle):
    ctypes.windll.user32.ShowWindow(handle, win32con.SW_RESTORE)
    ctypes.windll.user32.SetForegroundWindow(handle)
    time.sleep(1)

class LoopThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.paused = True
        self.handle = win32gui.FindWindow(None, "原神")

    def run(self):
        if self.handle:
            print("Get successfully")
        window_rect = win32gui.GetWindowRect(self.handle)
        print("Window Rect:", window_rect)
        while True:
            # 默认开始运行，当按下n后程序终止
            if self.running:
                if not self.paused:
                    print("Clicking...")
                    window_rect = win32gui.GetWindowRect(self.handle)
                    print("Window Rect:", window_rect)
                    setForground(self.handle)
                    xx, yy = window_rect[0] + 1200, window_rect[1] + 700
                    print(f"xx = '{xx}', yy = '{yy}'")
                    pyautogui.click(xx, yy)
                    time.sleep(2 + 0.2 * random())
            else:
                break

    def start_loop(self):
        if self.paused:
            print("Click Started.")
            self.paused = False
        else:
            print("Click Paused.")
            self.paused = True

    def stop_loop(self):
        if self.running:
            print("Program Quit.")
            self.running = False


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