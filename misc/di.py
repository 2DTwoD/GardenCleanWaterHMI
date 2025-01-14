from dependency_injector import containers, providers

from misc.receive import PeriphValues, TankValues
from panels.control_panel import TankLabelList
from panels.main_window import MainWindow
from widgets.mouse_pos import MousePos
from panels.seq_window import StatusList


class Container(containers.DeclarativeContainer):
    mainWindow = providers.Singleton(MainWindow)
    mousePos = providers.Singleton(MousePos)
    statusList = providers.Singleton(StatusList)
    tankLabelList = providers.Singleton(TankLabelList)
    periphValues = providers.Singleton(PeriphValues)
    tankValues = providers.Singleton(TankValues)
