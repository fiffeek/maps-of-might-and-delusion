import subprocess
import time
from typing import Optional
from logger import logger

from vcmi import VCMI
import os


class GUIController:
    def __init__(self, vcmi: VCMI):
        self.vcmi = vcmi
        self.process: Optional[subprocess.Popen] = None
        os.environ.pop("WAYLAND_DISPLAY", None)
        os.environ["GDK_BACKEND"] = "x11"
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        os.environ["SDL_VIDEODRIVER"] = "x11"
        display = f"127.0.0.1:{self.vcmi.local_display}.0"
        os.environ["DISPLAY"] = display
        os.environ["XAUTHORITY"] = self.vcmi.xauth_file
        logger.debug(f"Set display to {display}")

    def screenshot(self, filename: Optional[str] = None) -> str:
        """Take a screenshot of the current display"""
        logger.debug("Trying to make a screenshot")
        import pyautogui

        if not filename:
            filename = f"vcmi_screenshot_{int(time.time())}.png"

        logger.info(f"Saving a screenshot as {filename}")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        logger.info(f"Screenshot saved as {filename}")
        return filename

    def __enter__(self):
        self.vcmi.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.vcmi.stop()
