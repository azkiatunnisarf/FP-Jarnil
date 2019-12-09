# -*- coding: utf-8 -*-
import socket
import struct
import sys
import pickle
import ast
import time

#Unesa
lat_to = -7.965540
long_to = 112.617190

jalur = []
port = 8002
limit_time = 30
hop_limit = 1
pesanDikirim = []

def sendPosition():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(20)
    client.connect(('127.0.0.1', 8005))
    data = {
        'port' : port,
        'lat' : lat_to,
        'long' : long_to
    }
    client.send(pickle.dumps(data))
    print 'sukses mengirim lokasi !'
    return client.close()

def multicast():
    multicast_group = '224.3.29.71'
    server_address = ('', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(1024)
        
        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        data = ast.literal_eval(data)

        pesan = data[0]
        print 'isi pesan : ' + pesan
        print data
        
        rute = data[1]
        global jalur
        if not jalur:
            jalur = data[1]
        tujuan = data[4]
        print >>sys.stderr, 'sending acknowledgement to', address
        sock.sendto('ack', address)
        hop = data[2]        
        if(data[2] > hop_limit):
            print 'jumlah hop : ' + str(hop)
            print 'hop telah melebihi limit'
            break
        
        getSecond = time.time() - data[3]
        timestamp = time.time()

        duration = data[4] + getSecond

        if(getSecond > limit_time):
            print 'telah melebihi limit waktu'
            break

        if tujuan == port:
            print 'pengiriman selesai'
            break
        hop = data[2] + 1
        print 'pengiriman selanjutnya ke port ' + str(rute[hop][0])
        sendData(pesan,rute,hop,timestamp,duration,tujuan)
        break

def sendData(pesan,rute,hop,timestamp,duration,tujuan):
    p = rute[hop][0]
    pesanDikirim.insert(0,pesan)
    pesanDikirim.insert(1,rute)
    pesanDikirim.insert(2,hop)
    pesanDikirim.insert(3,timestamp)
    pesanDikirim.insert(4,duration)
    pesanDikirim.insert(5,tujuan)
    hasil = send(pesanDikirim, p)
    print ('mengirimkan pesan ke port ' + str(p))
    while(hasil == 0):
        hasil = send(pesanDikirim, p)
    print ('pengiriman berhasil ke port ' + str(p))
    print pesanDikirim

def sendDataInput():
    message = raw_input("input pesan > ")
    tujuan = raw_input("input port tujuan > ")
    global port
    tetangga1 = "null"
    tetangga2 = "null"
    for x in jalur:
        print len(jalur)
        if x[0] == port:
            if jalur.index(x) != 0:
                tetangga1 = jalur.index(x)-1
            if jalur.index(x) < len(jalur)-1:
                tetangga2 = jalur.index(x)+1
    print tetangga1, tetangga2

    p = jalur[tetangga1][0]
    p2 = jalur[tetangga2][0]
    pesanDikirim.insert(0,message)
    pesanDikirim.insert(1,jalur)
    # hop
    pesanDikirim.insert(2,0)
    pesanDikirim.insert(3,time.time())
    # durasi kirim
    pesanDikirim.insert(4,0)
    pesanDikirim.insert(5,tujuan)
    print pesanDikirim
    print ('mengirimkan pesan ke port ' + str(p))
    hasil = send(pesanDikirim, p)
    while(hasil == 0):
        hasil = send(pesanDikirim, p)
    print ('pengiriman berhasil ke port ' + str(p))

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
            print ('pesan berhasil dikirim')
            del pesanDikirim[:]
            sock.close()
            return 1

if __name__ == '__main__':
    print "receiver port " + str(port) + ": "
    print "=============="
    while 1:
        print "1. mengirimkan posisi ke sender"
        print "2. menerima data rute dan mengirimkan ke alamat selanjutnya"
        print "3. mengirim pesan ke tujuan"
        print "4. keluar"
        inputan = raw_input('Pilihan > ')
        if(inputan == '1'):
            sendPosition()
        elif(inputan == '2'):
            multicast()
        elif(inputan == '3'):
            sendDataInput()
        elif(inputan == '4'):
            exit()    
        else :
            print 'inputan salah'