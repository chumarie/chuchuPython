import socket

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
                    socket.send(('<?info?>'+str(len(sock_list)-1)+'\n').encode())
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
        roomlist = 'Available rooms are:\n'
        for i in range(1, len(history)+1):
            roomlist = roomlist + 'Room' + str(i) + ' '
        roomlist = roomlist + 'NewGroup+'
        conn.send(('Which Group would you like to join in?\n'+roomlist).encode())
        choice = conn.recv(4096).decode()
        flag = 1
        while flag:
            try:
                choice = int(choice)
                flag = 0
            except:
                conn.send('Invalid Input. Try Again.'.encode())
                choice = conn.recv(4096).decode()

        while choice > len(history)+1:
            conn.send('Invalid Input. Try Again.'.encode())
            choice = conn.recv(4096).decode()
            flag = 1
            while flag:
                try:
                    choice = int(choice)
                    flag = 0
                except:
                    conn.send('Invalid Input. Try Again.'.encode())
                    choice = conn.recv(4096).decode()
        if len(history)>=choice:
        #if 1:
            conn.send('Type in your username'.encode())
            username = conn.recv(4096).decode()
            player_maps[conn] = [choice, username]
            conn.send(history[choice-1].encode())
            broadcast(username+' is online', conn, choice)
        else:
            history.append('Room'+str(choice)+':')
            conn.send('Type in your username'.encode())
            username = conn.recv(4096).decode()
            player_maps[conn] = [choice, username]
            conn.send(history[choice-1].encode())
            broadcast(username+' is online', conn, choice)
    except:
        if sock in sock_list:
            sock_list.remove(conn)
        broadcast_to_all()
        if sock in player_maps.keys():
            del player_maps[sock]
