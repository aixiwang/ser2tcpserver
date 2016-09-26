"""ser2tcpserver
serial port -> tcp server
"""

import select
import socket
import argparse
import logging
import serial
import sys
import time

class Ser2TcpClient():
    def __init__(self,host,port,serial_port,serial_baud):   
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock = s
        s.settimeout(10)

        s.connect((host, port))
        print 'connect ', host, port, ' ok'

        self._serial = serial.Serial(
                port=serial_port,
                baudrate=serial_baud,
                timeout = 1
            )
        print 'open serial ',serial_port,' baud=',serial_baud, ' ok'
        
    def process(self):
        print '.'
        buf = self._serial.read()
        self._sock.sendall(buf)


VERSION_STR = "ser2tcpserver v1.0.0"

DESCRIPTION_STR = VERSION_STR + """
(c) 2016 by aixi.wang@gmail.com
"""

def main():
    """Main"""
    parser = argparse.ArgumentParser(description=DESCRIPTION_STR)

    parser.add_argument(
        'serial_port',
        help="Serial port")
    parser.add_argument(
        'serial_baud', type=int,
        help="Serial baud rate")

    parser.add_argument(
        'server_ip',
        help="server ip")
    parser.add_argument(
        'server_port', type=int,
        help="server port")
        
    args = parser.parse_args()


    while True:
        try:
    
            ser2tcp = Ser2TcpClient(
                args.server_ip,
                args.server_port,
                args.serial_port,
                args.serial_baud
            )
            

            while True:
                ser2tcp.process()

        except:
            print 'wait 5 sec...'
            time.sleep(5)
        



if __name__ == '__main__':

    main()
