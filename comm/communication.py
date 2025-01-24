import threading
import time

from serial.serialutil import SerialException

from misc import di

import serial.tools.list_ports
import serial

from misc.own_types import TankNumber, CommStatus


class Comm:
    def __init__(self):
        super().__init__()
        self.thread = None
        self.port = None
        self.cycleCommands = ["[get.periph]", "[get.chb]", "[get.ob1]", "[get.ob2]", "[get.ob3]"]
        self.cycleUpdatesValues = [di.Container.periphValues(),
                                   di.Container.tankValues().select(TankNumber.CHB),
                                   di.Container.tankValues().select(TankNumber.OB1),
                                   di.Container.tankValues().select(TankNumber.OB2),
                                   di.Container.tankValues().select(TankNumber.OB3)]
        self.baudrate = 19200
        self.cycleIndex = 0
        self.errorCounter = 0
        self.sendCommand = []
        self.start = False
        self.status = CommStatus.DISCONNECT
        self.bufferSize = 256
        self.sendPeriod = 0.1
        self.readTimeOut = 0.5

        self.maxCountForErrorVis = 20
        self.errorCounter = self.maxCountForErrorVis

    def send(self, command: str):
        if self.disconnected():
            return
        if command not in self.sendCommand:
            self.sendCommand.append(command)

    def runSending(self, device: str):
        try:
            self.port = serial.Serial(device, baudrate=self.baudrate)
            self.port.timeout = self.readTimeOut
            sendFlag = False

            while self.start:
                time.sleep(self.sendPeriod)

                if self.status == CommStatus.RECEIVE_ERROR:
                    pass
                self.port.reset_input_buffer()
                self.port.reset_output_buffer()

                if self.sendCommand and sendFlag:
                    sendFlag = False
                    self.port.write(self.sendCommand.pop(0).encode("ascii"))
                    bad, resp = self.checkResponse(self.port.read(self.bufferSize), b'o', b'k', b"ok")
                    if bad:
                        self.status = CommStatus.RECEIVE_ERROR
                    continue
                else:
                    self.port.write(self.cycleCommands[self.cycleIndex].encode("ascii"))
                    bad, resp  = self.checkResponse(self.port.read(self.bufferSize), b'{', b'}')
                sendFlag = True
                if bad or not self.cycleUpdatesValues[self.cycleIndex].updateValues(resp):
                    self.status = CommStatus.RECEIVE_ERROR
                    continue

                self.cycleIndex += 1
                if self.cycleIndex >= len(self.cycleCommands):
                    self.cycleIndex = 0

                if self.status != CommStatus.CONNECT:
                    self.errorCounter -= 1
                    if self.errorCounter <= 0:
                        self.status = CommStatus.CONNECT
                        self.errorCounter = self.maxCountForErrorVis

        except SerialException:
            self.status = CommStatus.LINK_ERROR
        else:
            self.status = CommStatus.DISCONNECT
        finally:
            self.port.close()

    def checkResponse(self, read, startChar, endChar, content=None):
        try:
            start = read.index(startChar)
            end = read.index(endChar)

            if start == -1 or end == -1:
                return True, None

            subString = read[start: end +1]

            if content is not None and subString != content:
                return True, None

            return False, subString
        except:
            return True, None

    @staticmethod
    def getAvailablePorts():
        result = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            result.append(port.device)
        return result

    def connect(self, device: str):
        self.status = CommStatus.CONNECT
        if self.connected():
            return
        self.thread = threading.Thread(target=self.runSending, args=(device, ))
        self.thread.daemon = True
        self.start = True
        self.thread.start()

    def disconnect(self):
        self.start = False
        self.status = CommStatus.DISCONNECT

    def connected(self):
        return self.port is not None and self.port.is_open and self.thread.is_alive()

    def disconnected(self):
        return not self.connected()

    def getStatus(self):
        return self.status.value