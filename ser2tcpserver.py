"""ser2tcpserver
serial port -> tcp server
"""

import select
import socket
import argparse
import logging
import serial
import sys


class Ser2TcpClient():
    def __init__(self,host,port,serial_port,serial_baud):   
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock = s
        s.settimeout(10)
        try:
            s.connect((host, port))
            
        except:
            sys.stdout.write('Unable to connect\n')
            sys.stdout.flush()
            sys.exit(1)
        
        self._serial = serial.Serial(
                port=serial_port,
                baudrate=serial_baud,
            )

        
    def process(self):
        buf = self._serial.read()
        if len(buf) > 0:
            self._sock.sendall(buf)
        
        


VERSION_STR = "ser2tcp v1.0.0"

DESCRIPTION_STR = VERSION_STR + """
(c) 2016 by pavel.revak@gmail.com
https://github.com/pavelrevak/ser2tcp
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
        
    #parser.add_argument(
    #    'flags', nargs='*', choices=['NONE', 'EVEN', 'ODD', 'ONE', 'TWO'],
    #    help="Serial parameters: parity: [NONE|EVEN|ODD], stop bits: [ONE|TWO], default: NONE ONE")
    args = parser.parse_args()



    ser2tcp = Ser2TcpClient(
        args.server_ip,
        args.server_port,
        args.serial_port,
        args.serial_baud
    )
    
    try:
        while True:
            ser2tcp.process()
    except Exception as err:
        print("%s" % err)
        raise err
    except KeyboardInterrupt:
        pass



if __name__ == '__main__':

    main()
