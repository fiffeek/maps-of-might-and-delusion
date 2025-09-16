from gui import GUIController
from models import GenerateMapResponse


class MapGenerator:
    def __init__(self) -> None:
        pass

    def generate(self, map: GenerateMapResponse, gui: GUIController):
        gui.screenshot()
