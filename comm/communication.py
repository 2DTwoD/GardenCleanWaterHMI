import threading
import time

from misc import di

import serial.tools.list_ports
import serial

from misc.own_types import TankNumber


class Comm:
    def __init__(self):
        super().__init__()
        self.thread: threading.Thread = None
        self.port: serial.Serial = None
        self.baudrate = 115200
        self.cycleCommands = ["[get.periph]", "[get.chb]", "[get.ob1]", "[get.ob2]", "[get.ob3]"]
        self.cycleUpdatesValues = [di.Container.periphValues(),
                                   di.Container.tankValues().select(TankNumber.CHB),
                                   di.Container.tankValues().select(TankNumber.OB1),
                                   di.Container.tankValues().select(TankNumber.OB2),
                                   di.Container.tankValues().select(TankNumber.OB3)]
        self.cycleIndex = 0
        self.sendCommand = ""
        self.stop = True

    def send(self, command: str):
        pass

    def runSending(self, device: str):
        try:
            self.port = serial.Serial(device, baudrate=self.baudrate)
            while(not self.stop):
                self.port.reset_input_buffer()
                self.port.write(self.cycleCommands[self.cycleIndex].encode("ascii"))
                count = 512
                resp = ""
                while count > 0 and not self.stop:
                    read = self.port.read()
                    if read == b'\n':
                        break
                    if read != b'':
                        resp += read.decode()
                    count -= 1
                self.cycleUpdatesValues[self.cycleIndex].updateValues(resp)
                self.cycleIndex += 1
                if self.cycleIndex >= len(self.cycleCommands):
                    self.cycleIndex = 0
                time.sleep(0.05)
        except:
            print("что-то пошло не так")
        finally:
            if self.port is not None and self.port.is_open:
                self.port.close()

    def getAvailablePorts(self):
        result = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            result.append(port.device)
        return result

    def connect(self, device: str):
        if self.connected():
            return
        self.thread = threading.Thread(target=self.runSending, args=(device, ))
        self.thread.daemon = True
        self.thread.start()
        self.stop = False

    def connected(self):
        return self.port is not None and self.port.is_open

    def disconnect(self):
        if self.disconnected():
            return
        self.stop = True

    def disconnected(self):
        return self.port is None or self.port.closed