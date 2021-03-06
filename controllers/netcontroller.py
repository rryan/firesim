import time
import logging as log
import struct

from profilehooks import profile

from PySide import QtCore, QtNetwork


class NetController(QtCore.QObject):

    ready_to_read = QtCore.Signal()
    data_received = QtCore.Signal()

    def __init__(self, app):
        super(NetController, self).__init__()
        self.socket = None
        self.app = app
        self.updates = 0
        self.last_time = time.clock()
        self.init_socket()
        self._byte_array_cache = {}

    def init_socket(self):
        self.socket = QtNetwork.QUdpSocket(self)
        self.socket.readyRead.connect(self.read_datagrams)
        self.socket.bind(3020, QtNetwork.QUdpSocket.ShareAddress | QtNetwork.QUdpSocket.ReuseAddressHint)
        log.info("Listening on UDP 3020")

    @QtCore.Slot()
    @profile
    def read_datagrams(self):
        while self.socket.hasPendingDatagrams():
            datagram_size = self.socket.pendingDatagramSize()

            datagram = self._byte_array_cache.get(datagram_size, None)
            if datagram is None:
                datagram = QtCore.QByteArray()
                datagram.resize(datagram_size)
                self._byte_array_cache[datagram_size] = datagram

            (datagram, sender, sport) = self.socket.readDatagram(datagram_size)

            buffer = struct.unpack('B' * datagram_size, datagram.data())
            self.app.scenecontroller.process_command(buffer)
        self.updates += 1
        self.data_received.emit()

    #@QtCore.Slot(result=float)
    def get_ups(self):
        dt = time.clock() - self.last_time
        if dt == 0:
            return 0
        ups = self.updates / dt
        self.last_time = time.clock()
        self.updates = 0
        return ups
