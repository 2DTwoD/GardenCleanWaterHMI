from PyQt6.QtCore import QPoint
from dependency_injector import containers, providers

from widgets.item import Item
from widgets.main_window import MainWindow
from widgets.mouse_pos import MousePos
from misc.own_types import RotateDir, ObjectType
from widgets.seq_window import StatusList


class Container(containers.DeclarativeContainer):
    mainWindow = providers.Singleton(MainWindow)
    mousePos = providers.Singleton(MousePos)
    statusList = providers.Singleton(StatusList)
    item = providers.Factory(
        Item,
        text="None",
        type=ObjectType.PUMP,
        position=QPoint(0, 0),
        rotation=RotateDir.RIGHT
    )
