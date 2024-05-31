#!/usr/bin/python
import socket,subprocess,os,base64,time

def main():
    pass

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('100.69.249.146', 2333)
    try:
        message = 'Hello, UDP server!'
        client_socket.sendto(message.encode(), server_address)
        data, server = client_socket.recvfrom(4096)
        print(f"Received: {data.decode()}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    udp_client()
