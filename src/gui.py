import subprocess
import time
from typing import Optional
from file import ROOT_DIR
from logger import logger

from models import MapSize
from vcmi import VCMI
import os
from enum import Enum


class ButtonType(str, Enum):
    FILE_TOP_LEFT = "file"


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

    def prepare(self):
        # give some time to warm up
        time.sleep(10)
        self.vcmi.maximize()
        self.locate_buttons()

    def locate_buttons(self):
        self.button_map = {
            ButtonType.FILE_TOP_LEFT: self.locate_on_screen(ButtonType.FILE_TOP_LEFT)
        }

    def locate_screenshots_file(self, path: str) -> str:
        return f"{ROOT_DIR}/src/locators/screenshots/{path}.png"

    def locate_on_screen(self, button_type: ButtonType):
        import pyautogui

        logger.debug(f"Attempting to find: {self.locate_screenshots_file(button_type)}")
        found = pyautogui.locateOnScreen(
            image=self.locate_screenshots_file(button_type), confidence=0.5
        )
        logger.debug(f"Found {self.locate_screenshots_file(button_type)} at {found}")
        return found

    def __enter__(self):
        self.vcmi.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.vcmi.stop()

    def click(self, button_type: ButtonType):
        import pyautogui

        button_box = self.button_map[button_type]
        if button_box is None:
            raise RuntimeError(f"cant click {button_type}")
        point = pyautogui.center(
            (button_box.left, button_box.top, button_box.width, button_box.height)
        )
        pyautogui.click(point.x, point.y)

    def new_map(self, size: MapSize):
        self.click(ButtonType.FILE_TOP_LEFT)
        self.screenshot()
