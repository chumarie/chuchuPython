#Import librairie
import socket
import select
import _thread
import numpy as np
import cv2


#Initialisation
host = '127.0.0.1'
port = 6000
sock_list = []
player_maps = {}
history = ['Room1:']
capArray = []

#Init socket
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(30)
sock_list.append(server_socket)

def broadcast(data, sock, group):
    for socket in sock_list:
        if socket != sock and socket != server_socket:
            if player_maps[socket][0] == group:
                try:
                    socket.send(('<'+player_maps[sock][1]+'> '+data).encode())
                except:
                    socket.close()
                    if socket in sock_list:
                        user = player_maps[socket][1]
                        del player_maps[socket]
                        broadcast_to_all()
                        sock_list.remove(socket)
                        broadcast_offline(user, group)

def broadcast_offline(user, group):
    for socket in sock_list:
        if socket != server_socket:
            if player_maps[socket][0] == group:
                try:
                    socket.send(('<'+user+'> is offline').encode())
                except:
                    socket.close()
                    if socket in sock_list:
                        flag = 0
                        if socket in player_maps.keys():
                            user = player_maps[socket][1]
                            del player_maps[socket]
                            flag = 1
                        broadcast_to_all()
                        sock_list.remove(socket)
                        if flag == 1:
                            broadcast_offline(user, group)

def broadcast_to_all():
    for socket in sock_list:
        if socket != server_socket:
                try:
                    socket.send(('<info>'+str(len(sock_list)-1)+'\n').encode())
                except:
                    socket.close()
                    if socket in sock_list:
                        user = player_maps[socket][1]
                        del player_maps[socket]
                        broadcast_to_all()
                        sock_list.remove(socket)
                        broadcast(user+' is offline', socket, group)

def handle(conn):
    try:
        sock_list.append(conn)
        broadcast_to_all()
        roomlist = 'Listes des rooms:\n'
        roomlist = roomlist + 'Room1 ' + 'Add Room'
        conn.send(('Choisissez votre room\n\n'+roomlist).encode())
        choice = conn.recv(4096).decode()
        print(sock_list)
        flag = 1
        while flag:
            try:
                choice = int(choice)
                flag = 0
            except:
                conn.send('Valeur incorrect. Veuillez réessayer.'.encode())
                choice = conn.recv(4096).decode()

        while choice > len(history)+1:
            conn.send('Valeur incorrect. Veuillez réessayer.'.encode())
            choice = conn.recv(4096).decode()
            flag = 1
            while flag:
                try:
                    choice = int(choice)
                    flag = 0
                except:
                    conn.send('Invalid Input. Try Again.'.encode())
                    choice = conn.recv(4096).decode()
        #room dans history
        if len(history)>=choice:
            conn.send('Tapez votre pseudo'.encode())
            username = conn.recv(4096).decode()
            player_maps[conn] = [choice, username]
            conn.send(history[choice-1].encode())
            print("ok1")
            print(history[choice-1].encode())
            broadcast(username+' est connecté', conn, choice)
        #new room
        else:
            history.append('Room'+str(choice)+':')
            conn.send('Tapez votre pseudo'.encode())
            username = conn.recv(4096).decode()
            player_maps[conn] = [choice, username]
            conn.send(history[choice-1].encode())
            broadcast(username+' est connecté', conn, choice)
    except:
        if sock in sock_list:
            sock_list.remove(conn)
        broadcast_to_all()
        if sock in player_maps.keys():
            del player_maps[sock]

while 1:
    ready_to_read, ready_to_write, in_error = select.select(sock_list,[],[])
    for sock in ready_to_read:
        if sock == server_socket:
            sockfd, addr = server_socket.accept()
            _thread.start_new_thread(handle, (sockfd,))
            print ("Client (%s, %s) connected" % addr)
        else:
            try:
                data = sock.recv(4096).decode()
                if data == '<change>':
                    roomlist = 'Available rooms are:\n'
                    prev = player_maps[sock][0]
                    if len(history) == 1:
                        sock.send('No other available groups to join.'.encode())
                        continue
                    for i in range(1, len(history)+1):
                        if i != prev:
                            roomlist = roomlist + 'Room' + str(i) + ' '
                    sock.send(('Which room would you like to choose? ' + roomlist).encode())
                    user = player_maps[sock][1]
                    ind = sock.recv(4096).decode()
                    print(ind)
                    try:
                        ind = int(ind)
                    except:
                        sock.send('Invalid Input. Try Again.'.encode())
                        continue
                    if ind > len(history):
                        sock.send('Invalid Input. Try Again.'.encode())
                        continue
                    if prev == ind:
                        sock.send('You are currently in the group you are requesting to join'.encode())
                        continue
                    player_maps[sock][0] = ind
                    sock.send(history[ind-1].encode())
                    broadcast(user+' is offline', sock, prev)
                    broadcast(user+' is online', sock, ind)
                elif data == '<available>':
                    text = '('
                    for socket in sock_list:
                        if socket != server_socket:
                            if player_maps[sock][0] == player_maps[socket][0]:
                                text = text + player_maps[socket][1] + ', '
                    text = text[:-2] + ')'
                    sock.send(text.encode())
                elif data == '<quit>':
                    user = player_maps[sock][1]
                    group = player_maps[sock][0]
                    del player_maps[sock]
                    sock_list.remove(sock)
                    broadcast_to_all()
                    sock.close()
                    broadcast_offline(user, group)
                elif data == '<webcam>':
                    cap = cv2.VideoCapture(0)
                    capArray.append(cap)
                    while(True):
                        ret, frame = cap.read()
                        cv2.imshow('frame',frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                elif data == '<test>':
                    cap = capArray[0]
                    capArray.append(cap)
                    while(True):
                        ret, frame = cap.read()
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        cv2.imshow('frame',gray)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                elif data:
                    history[player_maps[sock][0]-1] = history[player_maps[sock][0]-1]+'\n<'+player_maps[sock][1]+'> '+data
                    broadcast(data, sock, player_maps[sock][0])
                else:
                    if sock in sock_list:
                        user = player_maps[sock][1]
                        group = player_maps[sock][0]
                        del player_maps[sock]
                        sock_list.remove(sock)
                        broadcast_to_all()
                        sock.close()
                        broadcast_offline(user, group)
                        #print(2)
            except:
                if sock in sock_list:
                    sock_list.remove(sock)
                if sock in player_maps.keys():
                    user = player_maps[sock][1]
                    group = player_maps[sock][0]
                    broadcast_to_all()
                    sock.close()
                    broadcast_offline(user, group)
                #print(3)
