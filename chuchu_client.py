from tkinter import *
from tkinter import scrolledtext, messagebox
import sys, socket, select, _thread


running = False

#Action for command
def send():
   data = message.get()
   try:
      s.send(data.encode())
   except:
      error = messagebox.showinfo('Disconnected', 'Server is not active')
      exit()
   response.delete(0, END)
   chat.config(state=NORMAL)
   chat.insert(END ,'<You>' + data + '\n')
   chat.see(END)
   chat.config(state=DISABLED)

def sendonreturn(event):
   try:
      s.send(data.encode())
   except:
      error = messagebox.showinfo('Disconnected', 'Server is not active')
      exit()
   response.delete(0, END)
   chat.config(state=NORMAL)
   chat.insert(END ,'<You>' + data + '\n')
   chat.see(END)
   chat.config(state=DISABLED)

def receive():
   global running
   while running:
      try:
         data = s.recv(4096)
         data = data.decode()
         if '<info>' in data:
            ind = data.index('\n')
            status.set('Users Online: '+data[8:ind])
            if len(data) > ind+1:
               chat.config(state=NORMAL)
               chat.insert(END, data[ind+1:] + '\n')
               chat.see(END)
               chat.config(state=DISABLED)
         else:
            chat.config(state=NORMAL)
            chat.insert(END, data + '\n')
            chat.see(END)
            chat.config(state=DISABLED)
      except:
         running = False


def available():
   s.send('<available>'.encode())

def change():
   s.send('<change>'.encode())

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def webcam():
   s.send('<webcam>'.encode())

def change():
   s.send('<change>'.encode())
def webcamFiltreNB():
   s.send('<wnb>'.encode())
def Quit():
   try:
      s.send('<quit>'.encode())
   except:
      pass
   s.close()
   root.destroy()
   global running
   running = False
   quit()

def on_closing():
   if messagebox.askokcancel("Quit", "Do you want to quit?"):
      try:
         s.send('<quit>'.encode())
      except:
         pass
      s.close()
      root.destroy()


#Run Server

host = '127.0.0.1'
port = 6000
flag = 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Tkinter View
root = Tk()
frame1 = Frame(root)
frame1.pack(side=TOP, fill=BOTH, expand=1)
root.wm_title('Chuchu Python Chat')
message = StringVar()
status = StringVar()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Quit)
menubar.add_cascade(label="File", menu=filemenu)
optionsmenu = Menu(menubar, tearoff=0)
optionsmenu.add_command(label = 'Qui est dans cette room ?', command=available)
optionsmenu.add_command(label="Change Chat Room", command=change)
optionsmenu.add_command(label="webcam Normal", command=webcam)
optionsmenu.add_command(label="webcam B&W", command=webcamFiltreNB)
menubar.add_cascade(label="Options", menu=optionsmenu)
root.config(menu=menubar)
menubar.config(background="pink")

chat = scrolledtext.ScrolledText(frame1, height=10, width=80, state=DISABLED)
chat.pack(side=TOP, fill=BOTH, expand=1)
response = Entry(frame1, textvariable = message)
response.focus()
send = Button(frame1, text='Send', command=send)
response.pack(side=LEFT, fill=X, expand=1)
send.pack(side=RIGHT)
online_users = Label(root, textvariable = status, relief = SUNKEN, anchor = W)
online_users.pack(side = BOTTOM, fill = X, expand = 1)
root.bind('<Return>', sendonreturn)
root.protocol("WM_DELETE_WINDOW", on_closing)

#if true
if flag == 1:
   try :
      s.connect((host, port))
   except:
      error = messagebox.showinfo('Unable to Connect', 'Server is not active')
      root.destroy()
      _thread.interrupt_main()
      quit()
   running = True
   _thread.start_new_thread(receive, ())
   status.set('Users Online: ')
   flag+=1
root.mainloop()



