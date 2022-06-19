from typing import List, Any

import raylibpy as ray


class GameWindow:
    def __init__(self, width: int = 800, height: int = 400, pages: int = 1):
        self.width = width
        self.height = height
        self.pages = pages
        self.shapes = []

    def add_rectangle(self, x_pos: int, y_pos: int, width: int, height: int):
        self.shapes.append(ray.Rectangle(x_pos, y_pos, width, height))


class MainMenuWindow(GameWindow):
    def __init__(self):
        super().__init__(width=200, height=600, pages=5)


if __name__ == "__main__":
    debugWindow = GameWindow()
    debugWindow.add_rectangle(1, 1, 1, 1)
    print(debugWindow.shapes)
