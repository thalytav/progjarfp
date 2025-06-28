from socket import *
import socket
import time
import sys
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer  

httpserver = HttpServer()

#untuk menggunakan threadpool executor, karena tidak mendukung subclassing pada process,
#maka class ProcessTheClient dirubah dulu menjadi function, tanpa memodifikasi behaviour didalamnya

def ProcessTheClient(connection,address):
    rcv=""
    while True:
        try:
            data = connection.recv(32)
            if data:
                d = data.decode()
                rcv=rcv+d
                if rcv[-2:]=='\r\n':
                    hasil = httpserver.proses(rcv)
                    hasil=hasil+"\r\r".encode()
                    connection.sendall(hasil)
                    rcv=""
                    connection.close()
                    return
            else:
                break
        except OSError as e:
            pass
    connection.close()
    return

def Server():
    the_clients = []
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    my_socket.bind(('0.0.0.0', 8885))
    my_socket.listen(1)

    with ThreadPoolExecutor(20) as executor:
        while True:
            connection, client_address = my_socket.accept()
            p = executor.submit(ProcessTheClient, connection, client_address)
            the_clients.append(p)
            jumlah = ['x' for i in the_clients if i.running()==True]
            print(jumlah)

def main():
    Server()

if __name__=="__main__":
    main()
