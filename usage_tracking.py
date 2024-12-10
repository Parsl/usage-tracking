#!/usr/bin/env python3
import socket
import logging
from datetime import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 50077

class Listener (object):

    def __init__ (self, ip=None, port=None, filename=None):
        ''' Initialize sockets and create log files to log
        messages to.
        '''

        self.ip   = ip
        self.port = port
        self.filename = filename
        self.sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP,
                              ) # UDP
        self.sock.bind((ip, port))
        self.current_date = None
        self.set_file_logger(filename=self.filename)


    def listen (self):
        ''' Listen on the socket for UDP messages
        and dump the messages to a daily log file
        '''
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            if self.current_date and self.current_date != datetime.date(datetime.now()):
                # Push file to new log on turn of day
                self.set_file_logger(filename=self.filename)
                print("Rolling over to new log file")
            self.logger.info("Source:{}, Msg:{}".format(addr[0], data.decode("utf-8")))

    def set_file_logger(self, filename=None, name='tracker', level=logging.DEBUG, format_string=None):
        ''' Add a file log handler

        Args:
             - filename (string): Name of the file to write logs to
             - name (string): Logger name
             - level (logging.LEVEL): Set the logging level.
             - format_string (string): Set the format string

        Returns:
             -  None
        '''
        if not filename:
            # The roll over to new log file per day behavior is only
            # when no filename is explicitly specified
            self.current_date = datetime.date(datetime.now())
            filename = "parsl-{0}.log".format(self.current_date)
            print("Setting current_date : ", self.current_date)

        if format_string is None:
            format_string = "%(asctime)s: %(message)s"

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers = []
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.debug("New Log section for new day ===================")

if __name__ == "__main__" :


    listener = Listener(ip=UDP_IP, port=UDP_PORT)
    listener.listen()
