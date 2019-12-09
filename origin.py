# -*- coding: utf-8 -*-
import socket
import struct
import sys
import os
import json
import pickle
import glob
import numpy
import operator
import time
import copy
from geopy.distance import geodesic

#ITS SURABAYA
lat_from = -7.274330
long_from = 112.797798

pesanDikirim = []
portDistance = []
portDistance_temp = []
jarak = {}

def getLatLong():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "0.0.0.0"
    port = 8005
    server.bind((ip, port))
    server.listen(5)
    #print ('menunggu mendapatkan posisi receiver')
    print ('waiting for position from receiver ...')
    (client_socket, address) = server.accept()
    data = pickle.loads(client_socket.recv(1024))
    print ("========")
    print ("getting lattitude and longitude from receiver ... " + str(data['port']))
   # print ("mendapatkan titik lat long dari receiver port " + str(data['port']))
    print ("isi data :")
    print (data['lat'])
    print (data['long'])
    print ("========")
    jarak[data['port']]=(getDistance(data['lat'],data['long']))
    server.close()

def sendDataInput():
    message = raw_input("enter message > ")
#    message = raw_input("input pesan > ")
    p = portDistance[0][0]

    pesanDikirim.insert(0,message)
    pesanDikirim.insert(1,portDistance)
    # hop
    pesanDikirim.insert(2,0)
    pesanDikirim.insert(3,time.time())
    # durasi kirim
    pesanDikirim.insert(4,0)

    print ('Sending message ... ' + str(p))
    hasil = send(pesanDikirim, p)
    while(hasil == 0):
        hasil = send(pesanDikirim, p)
    print ('sending success! ' + str(p))
    print pesanDikirim


def send(message,port):
    multicast_group = ('224.3.29.71', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    sock.sendto(str(message), multicast_group)
    while True:
        try:
            sock.recvfrom(16)
        except:
            sock.close()
            return 0
        else:
            print ('message sent!')
            del pesanDikirim[:]
            sock.close()
            return 1


def getDistance(lat_to,long_to):
    coords_1 = (lat_from, long_from)
    coords_2 = (lat_to, long_to)
    return geodesic(coords_1, coords_2).km

def getUrutan():
    for jauh in jarak:
        print jarak[jauh]
        jarak_temp = float(jarak[jauh])
        portDistance_temp.append([jauh,jarak_temp])
    return sorted(portDistance_temp, key=operator.itemgetter(1), reverse=False)
    
if __name__ == '__main__':
    print ("sender multicast dtn")
    while 1:
        print ("1. Get all lattitude and longitude")
        print ("2. Rearrange")
        print ("3. Send data")
        print ("4. Exit")
        pilihan = raw_input("Option > ")
        if(pilihan == '1'):
            getLatLong()
        elif(pilihan == '2'):
            portDistance = copy.deepcopy(getUrutan())
            print portDistance
        elif(pilihan == '3'):
            sendDataInput()
        elif(pilihan == '4'):
            exit()