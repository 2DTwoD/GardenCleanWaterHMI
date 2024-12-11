from PyQt6.QtCore import QPoint
from dependency_injector import containers, providers

from item import Item
from main_window import MainWindow
from mouse_pos import MousePos
from own_types import RotateDir, ObjectType


class Container(containers.DeclarativeContainer):
    mainWindow = providers.Singleton(MainWindow)
    mousePos = providers.Singleton(MousePos)
    item = providers.Factory(
        Item,
        text="None",
        type=ObjectType.PUMP,
        position=QPoint(0, 0),
        rotation=RotateDir.RIGHT
    )
