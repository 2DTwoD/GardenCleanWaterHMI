from dependency_injector import containers, providers

from comm.communication import Comm
from comm.receive import PeriphValues, TankValues
from panels.main_window import MainWindow
from widgets.mouse_pos import MousePos


class Container(containers.DeclarativeContainer):
    mainWindow = providers.Singleton(MainWindow)
    mousePos = providers.Singleton(MousePos)
    periphValues = providers.Singleton(PeriphValues)
    tankValues = providers.Singleton(TankValues)
    comm = providers.Singleton(Comm)
