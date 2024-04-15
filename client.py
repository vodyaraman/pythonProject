import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 9090


class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()
        self.nicknames = []

        while True:
            self.nickname = simpledialog.askstring("Nickname", "Please, choose a nickname", parent=msg).strip()
            if self.nickname != "":
                self.gui_done = False
                self.running = True

                gui_tread = threading.Thread(target=self.gui_loop)
                receive_thread = threading.Thread(target=self.receive)

                receive_thread.start()
                gui_tread.start()
                break
            else:
                continue

    def gui_loop(self):
    #
        self.win = tkinter.Tk()
        self.win.title(f"Чат от имени {self.nickname}")
        self.win.configure(bg="lightgray")
        self.win.geometry("600x600+20+20")
    #
        self.chat_label = tkinter.Label(self.win, text="Сообщения: ", bg="lightgray")
        self.chat_label.config(font=("Arial", 14))
        self.chat_label.place(relx=0.13, rely=0.01, relwidth=0.45, relheight=0.07)
    #
        self.chat_label = tkinter.Label(self.win, text="Список участников: ", bg="lightgray")
        self.chat_label.config(font=("Arial", 14))
        self.chat_label.place(relx=0.65, rely=0.01, relwidth=0.35, relheight=0.07)
    #
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(font=("Arial", 12), state='disabled')
        self.text_area.place(x=10, rely=0.1, relwidth=0.65, relheight=0.62)
    #
        self.nickname_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.nickname_area.config(font=("Arial", 12), state='disabled')
        self.nickname_area.place(relx=0.679, rely=0.1, relwidth=0.3, relheight=0.62)
    #
        self.msg_label = tkinter.Label(self.win, text="Введите сообщение: ", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.place(x=10, rely=0.74, relwidth=0.965, relheight=0.07)
    #
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.config(font=("Arial", 12))
        self.input_area.place(x=10, rely=0.8, relwidth=0.965, relheight=0.09)
    #
        self.send_button = tkinter.Button(self.win, text='Отправить сообщение', command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.place(x=11, rely=0.9, relwidth=0.965, relheight=0.07)
    #
        self.gui_done = True
        self.sock.send("gui_done".encode('utf-8'))

        self.win.protocol('WM_DELETE_WINDOW', self.stop)
        self.win.mainloop()

    def stop(self):
        self.win.destroy()
        self.running = False
        self.sock.close()
        exit(0)

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                elif message.split("'")[0] == '[':
                    self.client_list(message)
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Exception")
                self.sock.close()
                break

    def client_list(self, message):
        self.nickname_area.config(state="normal")
        self.nickname_area.delete(1.0, 'end')
        self.nickname_area.config(state="disabled")
        self.nicknames = message.strip('[]').replace(' ', '').split(',')
        print(self.nicknames)
        if self.gui_done:
            for user in self.nicknames:
                self.nickname_area.config(state='normal')
                self.nickname_area.insert('end', f"{str(user.replace("'", ''))}\n")
                self.nickname_area.yview('end')
                self.nickname_area.config(state='disabled')


client = Client(HOST, PORT)
