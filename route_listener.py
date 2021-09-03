from twisted.internet.protocol import DatagramProtocol, ProcessProtocol
from twisted.internet import reactor, utils
from twisted.logger import Logger, STDLibLogObserver
import logging
import socket

logging.basicConfig(level=logging.DEBUG)
log = Logger(observer=STDLibLogObserver())


LOCAL_IP_ADDRESS = socket.gethostbyname(socket.gethostname())


class BroadcastRouteProtocol(DatagramProtocol):
    def startProtocol(self):
        self.transport.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

    def datagramReceived(self, datagram, addr):
        destination = datagram.decode().strip('\n')

        log.debug(f'Received {destination} from {addr}.')
        if addr[0] != LOCAL_IP_ADDRESS:
            log.debug('Appending route.')

            # Broadcast came from addr so we now that client 'destination' is connected to this node.
            append_route(destination, addr[0])
        else:
            log.debug('Doing nothing because broadcast came from us.')


def append_route(destination: str, gateway: str):
    log.debug(f'/sbin/ip route del {destination}')
    output = utils.getProcessOutput('/sbin/ip', ['route', 'del', destination])
    output.addCallback(log.debug)

    log.debug(f'/sbin/ip route add {destination} via {gateway}')
    output = utils.getProcessOutput('/sbin/ip', ['route', 'add', destination, 'via', gateway])
    output.addCallback(log.debug)


class LoggingProcessProtocol(ProcessProtocol):
    def processExited(self, reason):
        log.debug(f'Openvpn stopped: {reason}')

    def outReceived(self, data):
        log.debug(data.decode().strip('\r\n'))

    def errReceived(self, data):
        log.debug(data.decode().strip('\r\n'))


class OpenvpnServer:
    def __init__(self):
        self._process = None

    def start(self):
        log.debug('Spawning openvpn process')
        self._process = reactor.spawnProcess(LoggingProcessProtocol(), '/usr/local/bin/ovpn_run', args=['/usr/local/bin/ovpn_run'], env={'HOME': '/root', 'DEBUG': '1', 'OPENVPN': '/etc/openvpn'}, usePTY=True)
        log.debug(str(self._process.pid))

    def stop(self):
        pass


def main():
    log.debug('Starting up...')

    # Listen at broadcast port 12345
    route_proto = BroadcastRouteProtocol()
    lp = reactor.listenUDP(12345, route_proto)

    # Start the OpenVPN process
    openvpn_process = OpenvpnServer()
    openvpn_process.start()

    reactor.run()


if __name__ == '__main__':
    main()
