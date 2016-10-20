#===================================
# ser2tcpserver
# serial port <-> tcp server
# (c) 2016 by aixi.wang@hotmail.com
#===================================

import select
import socket
import argparse
import logging
import serial
import sys
import time
import threading

class Ser2TcpClient():
    def __init__(self,host,port,serial_port,serial_baud):   
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p1_terminal_flag = False
        self.p2_terminal_flag = False
        
        #s.settimeout(10)
        print 'step 1'
        
        print 'step 2'
        self.tcp_s.connect((host, port))
        
        self.tcp_s.setblocking(1)
        print 'connect ', host, port, ' ok'

        self._serial = serial.Serial(
                port=serial_port,
                baudrate=serial_baud,
                timeout = 0
            )
        print 'open serial ',serial_port,' baud=',serial_baud, ' ok'
        
    def process(self):
        while True:
            try:
                if self.p2_terminal_flag == True:
                    return            
                #print '.'
                buf = self._serial.read(256)
                if len(buf) > 0:
                    print 'serial recv:',buf
                    self.tcp_s.sendall(buf)
                else:
                    time.sleep(0.01)                
            except:
                print 'process exception'
                self.p1_terminal_flag = True
                return                
                
    def process2(self):        
        while True:
            
            try:
                if self.p1_terminal_flag == True:
                    return
                    
                print '='
                buf2 = self.tcp_s.recv(256)
                if not buf2:
                    print "connection closed"
                    self.tcp_s.close()
                    print 'process2 exception 1'
                    self.p2_terminal_flag = True
                    return
                            
                if len(buf2) > 0:
                    print 'socket recv(hex):',buf2.encode('hex')
                    self._serial.write(buf2)
                else:
                    time.sleep(0.01)
            except:
                print 'process2 exception 2'
                self.p2_terminal_flag = True
                return
                

VERSION_STR = "ser2tcpserver v1.0.0"

DESCRIPTION_STR = VERSION_STR + """
(c) 2016 by aixi.wang@hotmail.com
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
            print 'args.server_ip:',args.server_ip
            print 'args.server_port:',args.server_port
            print 'args.serial_port:',args.serial_port
            print 'args.serial_baud:',args.serial_baud

            ser2tcp = Ser2TcpClient(
                args.server_ip,
                args.server_port,
                args.serial_port,
                args.serial_baud
            )
            
            print 'start thread 1'
            threading.Thread(target=ser2tcp.process).start()
            time.sleep(0.1)
            
            print 'start thread 2'            
            threading.Thread(target=ser2tcp.process2).start()
            time.sleep(0.1)
        
            while True:
                if ser2tcp.p1_terminal_flag == True or ser2tcp.p2_terminal_flag == True:
                    ser2tcp._serial.close()
                    ser2tcp.tcp_s.close()               
                    print '=============>'
                    break;

        except Exception as e:
        
            print ' wait 5 sec...',str(e)
            try:
                ser2tcp._serial.close()
                ser2tcp.tcp_s.close()
            except:
                pass
            time.sleep(5)
        



if __name__ == '__main__':

    main()
