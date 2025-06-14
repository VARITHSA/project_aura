import os
import platform
import shutil
import subprocess

import pyautogui


class SystemBot:
    def __init__(self):
        self.os_type = platform.system().lower()

    def shutdown(self):
        try:
            if "windows" in self.os_type:
                os.system("shutdown /s /t 1")
            elif "linux" in self.os_type or "darwin" in self.os_type:
                os.system("shutdown now")
            print("🔌 Shutdown initiated.")
        except Exception as e:
            print(f"❌ Failed to shutdown: {e}")

    def restart(self):
        try:
            if "windows" in self.os_type:
                os.system("shutdown /r /t 1")
            elif "linux" in self.os_type or "darwin" in self.os_type:
                os.system("reboot")
            print("♻️ Restart initiated.")
        except Exception as e:
            print(f"❌ Failed to restart: {e}")

    def sleep(self):
        try:
            if "windows" in self.os_type:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif "darwin" in self.os_type:
                os.system("pmset sleepnow")
            elif "linux" in self.os_type:
                os.system("systemctl suspend")
            print("😴 Sleep initiated.")
        except Exception as e:
            print(f"❌ Failed to sleep: {e}")

    def volume_up(self):
        try:
            pyautogui.press("volumeup")
            print("🔊 Volume increased.")
        except Exception as e:
            print(f"❌ Failed to increase volume: {e}")

    def volume_down(self):
        try:
            pyautogui.press("volumedown")
            print("🔉 Volume decreased.")
        except Exception as e:
            print(f"❌ Failed to decrease volume: {e}")

    def mute(self):
        try:
            pyautogui.press("volumemute")
            print("🔇 Volume muted.")
        except Exception as e:
            print(f"❌ Failed to mute volume: {e}")

    def take_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            path = os.path.join(os.getcwd(), "screenshot.png")
            screenshot.save(path)
            print(f"🖼️ Screenshot saved at: {path}")
        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")

    def open_app(self, app_name):
        try:
            if shutil.which(app_name):
                subprocess.Popen([app_name])
                print(f"🚀 Launched {app_name}")
            else:
                print(f"❌ App not found in PATH: {app_name}")
        except Exception as e:
            print(f"❌ Failed to open app: {e}")
