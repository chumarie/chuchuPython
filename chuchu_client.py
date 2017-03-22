from tkinter import *
from tkinter import scrolledtext, messagebox
import sys, socket, select, _thread

#Interface Tkinter
root = Tk()
frame1 = Frame(root)
#frame2 = Frame(root)
frame1.pack(side=TOP, fill=BOTH, expand=1)
#frame2.pack(side=TOP)
root.wm_title('Chuchu Python Chat')
#history = StringVar()
message = StringVar()
status = StringVar()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label = 'Connect')
filemenu.add_command(label = 'Disconnect')
menubar.add_cascade(label="Statut", menu=filemenu)
optionsmenu = Menu(menubar, tearoff=0)
optionsmenu.add_command(label = 'Create new room')
optionsmenu.add_command(label="Change Chat Room")
optionsmenu.add_command(label = 'Users in my room')
optionsmenu.add_command(label = 'Show webcam')
menubar.add_cascade(label="Options", menu=optionsmenu)
root.config(menu=menubar)
menubar.config(background="pink")

chat = scrolledtext.ScrolledText(frame1 ,height=10, width=80, state=DISABLED)
chat.pack(side=TOP, fill=BOTH, expand=1)
response = Entry(frame1, textvariable = message)
response.focus()
send = Button(frame1, text='Envoyer')
response.pack(side=LEFT, fill=X, expand=1)
send.pack(side=RIGHT)
online_users = Label(root, textvariable = status, relief = SUNKEN, anchor = W)
online_users.pack(side = BOTTOM, fill = X, expand = 1)
root.bind('<Return>')
root.protocol("WM_DELETE_WINDOW")

root.mainloop()