from dependency_injector import containers, providers

from comm.communication import Comm
from comm.receive import PeriphValues, TankValues
from panels.control_panel import TankLabelList
from panels.main_window import MainWindow
from widgets.mouse_pos import MousePos
from panels.seq_window import StatusList, StatusColors


class Container(containers.DeclarativeContainer):
    mainWindow = providers.Singleton(MainWindow)
    mousePos = providers.Singleton(MousePos)
    statusList = providers.Singleton(StatusList)
    statusColors = providers.Singleton(StatusColors)
    tankLabelList = providers.Singleton(TankLabelList)
    periphValues = providers.Singleton(PeriphValues)
    tankValues = providers.Singleton(TankValues)
    comm = providers.Singleton(Comm)
