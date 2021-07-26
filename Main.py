import tkinter as tk
from tkinter import *
from PIL import ImageTk
from tkinter import filedialog, messagebox
from writeCode.mainWrite import WriteMessage
from writeCode.mainTxt import TextMessage
from writeCode.mainImg import ImageMessage
from writeCode.mainDecrypt import DecriptImage
from writeCode.mainOther import OtherMessage
from writeCode.videoDecrypt import VideoDecrypt
from threading import Thread
import time

class ThreadReturn(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

class DeceryptWin():
    def __init__(self, x):
        self.filename = ''
        self.saveFile = ''
        self.password = ''
        self.decrypt_win = Toplevel(root)
        self.containerValue = tk.IntVar()
        self.decrypt_win.geometry("300x500")
        self.decrypt_win.resizable(width=0, height=0)
        self.decrypt_win.grid_columnconfigure(0, weight=300)
        self.choixContainer = tk.LabelFrame(
            self.decrypt_win, text="type of container", width=250)
        self.choixContainer.grid(
            column=0, row=0, padx=10, pady=10, sticky="we")
        self.labelFrame = tk.LabelFrame(
            self.decrypt_win, text="Open your image", width=250)
        self.labelFrame.grid(column=0, row=1, padx=10, pady=10, sticky="we")
        self.saveFrame = tk.LabelFrame(self.decrypt_win, text="save location ")
        self.saveFrame.grid(column=0, row=2, padx=10, pady=10, sticky="we")
        self.passwordFrame = tk.LabelFrame(
            self.decrypt_win, text="input password")
        self.passwordFrame.grid(column=0, row=3, padx=10, pady=10, sticky="we")
        self.importContainer()
        self.radioContainer()
        self.passwordGrid()
        self.savelocation()
        self.decrypt()

    def deleteFrame(self, element):
        for widget in element.winfo_children():
            widget.grid_forget()

    def search(self):
        self.button = tk.Button(
            self.labelFrame, text="Browse A Image", command=self.fileDialog)
        self.button.grid(column=0, row=1, sticky="W")

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("png files", "*png*"), ("all files", "*.*")))
        label = tk.Label(self.labelFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.filename)
        self.decrypt()

    def savelocation(self):
        self.button3 = tk.Button(
            self.saveFrame, text="Browse A File", command=self.saveDialog)
        self.button3.grid(column=0, row=1, sticky="W")

    def saveDialog(self):
        self.saveFile = filedialog.asksaveasfilename(
            initialdir="/", title="Save location")
        label = tk.Label(self.saveFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.saveFile)
        self.decrypt()

    def passwordGrid(self):
        psw = tk.Entry(self.passwordFrame, font=('calibre', 10, 'normal'))
        psw.grid(column=0, row=1, sticky="W")
        self.button4 = tk.Button(
            self.passwordFrame, text="Confirm", command=lambda: self.confirm(psw))
        self.button4.grid(column=2, row=1, sticky="W")
        self.decrypt()

    def confirm(self, psw):
        self.password = ''
        self.password = psw.get()
        label = tk.Label(self.passwordFrame, text="")
        label.grid(column=0, row=2, sticky="W")
        label.grid(column=0, row=2, sticky="We", columnspan=3)
        if len(self.password) >= 15:
            text = self.password[0:15]
            text += "..."
        else:
            text = self.password
        label.configure(text=text)
        self.decrypt()

    def decrypt(self):
        if self.filename == '' or self.saveFile == '' or self.password == '':
            self.condition = DISABLED
        else:
            self.condition = NORMAL
        self.buttonSend = tk.Button(
            self.decrypt_win, text="Decode", state=self.condition, command=self.decryption)
        self.buttonSend.grid(column=0, row=6, sticky="We")

    def decryption(self):
        self.decrypt_win.config(cursor="wait")
        self.decrypt_win.update()
        t = time.time()
        if self.containerValue.get() == 0:
            t1 = ThreadReturn(target=DecriptImage.decrypt, args=(self.filename, self.password, self.saveFile))
            t1.start()
        else:
            t1 = ThreadReturn(target=VideoDecrypt.decrypt, args=(self.filename, self.password, self.saveFile))
            t1.start()
        elapsed = time.time() - t
        err = t1.join()
        print("execution time", elapsed)
        if err == 0:
            messagebox.showinfo(
                title="Success", message="the message successful decrypted")
            self.decrypt_win.destroy()
        else:
            self.decrypt_win.config(cursor="arrow")
            messagebox.showerror(title="Error", message=err)

    def radioContainer(self):
        rdioOne = tk.Radiobutton(self.choixContainer, text='Image',
                                 variable=self.containerValue, value=0, command=self.importContainer)
        rdioTwo = tk.Radiobutton(self.choixContainer, text='Video',
                                 variable=self.containerValue, value=1, command=self.importContainer)
        rdioOne.grid(column=0, row=0, sticky="W")
        rdioTwo.grid(column=1, row=0, sticky="W")

    def importContainer(self):
        self.deleteFrame(self.labelFrame)
        if self.containerValue.get() == 1:
            self.button1 = tk.Button(
                self.labelFrame, text="Browse A video", command=self.fileVid)
            self.button1.grid(column=0, row=1, sticky="W")
        else:
            self.search()

    def fileVid(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("mp4 files", "*.mp4"), ("avi files", "*.avi"), ("all files", "*.*")))
        label = tk.Label(self.labelFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.filename)
        self.decrypt()

class EncryptWin():
    def __init__(self, x):
        self.password = ''
        self.filename = ''
        self.hiddename = ''
        self.saveFile = ''
        self.encrypt_win = Toplevel(root)
        self.radioValue = tk.IntVar()
        self.containerValue = tk.IntVar()
        self.encrypt_win.geometry("300x550")
        self.encrypt_win.resizable(width=0, height=0)
        self.encrypt_win.grid_columnconfigure(0, weight=300)
        self.choixContainer = tk.LabelFrame(
            self.encrypt_win, text="type of container", width=250)
        self.choixContainer.grid(
            column=0, row=0, padx=10, pady=10, sticky="we")
        self.labelFrame = tk.LabelFrame(
            self.encrypt_win, text="Open container")
        self.labelFrame.grid(column=0, row=1, padx=10, pady=10, sticky="we")
        self.choixFrame = tk.LabelFrame(
            self.encrypt_win, text="type of your hidden file")
        self.choixFrame.grid(column=0, row=2, padx=10, pady=10, sticky="we")
        self.hiddenFrame = tk.LabelFrame(self.encrypt_win, text="hidden file")
        self.hiddenFrame.grid(column=0, row=3, padx=10, pady=10, sticky="we")
        self.saveFrame = tk.LabelFrame(self.encrypt_win, text="save location ")
        self.saveFrame.grid(column=0, row=4, padx=10, pady=10, sticky="we")
        self.passwordFrame = tk.LabelFrame(
            self.encrypt_win, text="input password")
        self.passwordFrame.grid(column=0, row=5, padx=10, pady=10, sticky="we")
        self.passwordGrid()
        self.importSneakMess()
        self.importContainer()
        self.radioContainer()
        self.choix()
        self.savelocation()
        self.encrypt()

    def encryption(self):
        self.encrypt_win.config(cursor="wait")
        print(self.containerValue)
        t = time.time()
        if self.containerValue.get() == 1:
            container = "video"
        else:
            container = "image"
        if self.radioValue.get() == 2:
            t1 = ThreadReturn(target=WriteMessage.encrypt, args=(
                self.hiddename, self.password, self.filename, self.saveFile, container))
            t1.start()
        elif self.radioValue.get() == 1:
            t1 = ThreadReturn(target=TextMessage.encrypt, args=(
                self.hiddename, self.password, self.filename, self.saveFile, container))
            t1.start()
        elif self.radioValue.get() == 3:
            t1 = ThreadReturn(target=ImageMessage.encrypt, args=(
                self.hiddename, self.password, self.filename, self.saveFile, container))
            t1.start()
        else:
            t1 = ThreadReturn(target=OtherMessage.encrypt, args=(
                self.hiddename, self.password, self.filename, self.saveFile, container))
            t1.start()
        err = t1.join()
        elapsed = time.time() - t
        print("execution time", elapsed)
        if err == 0:
            messagebox.showinfo(
                title="Success", message="the new image is successful create")
            self.encrypt_win.destroy()
        else:
            self.encrypt_win.config(cursor="arrow")
            messagebox.showerror(title="Error", message=err)

    def encrypt(self):
        print(self.filename, self.hiddename, self.saveFile, self.password)
        if self.filename == '' or self.hiddename == '' or self.saveFile == '' or self.password == '' or self.containerValue == '':
            condition = DISABLED
        else:
            condition = NORMAL
        self.buttonSend = tk.Button(
            self.encrypt_win, text="Encode", state=condition, command=self.encryption)
        self.buttonSend.grid(column=0, row=6, sticky="We")

    def savelocation(self):
        self.button3 = tk.Button(
            self.saveFrame, text="Browse A File", command=self.saveDialog)
        self.button3.grid(column=0, row=1, sticky="W")

    def saveDialog(self):
        self.saveFile = filedialog.asksaveasfilename(
            initialdir="/", title="Save location")
        label = tk.Label(self.saveFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.saveFile)
        self.encrypt()

    def search(self):
        self.button = tk.Button(
            self.labelFrame, text="Browse A image", command=self.fileDialog)
        self.button.grid(column=0, row=1, sticky="W")

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("jpeg files", "*.jpg"), ("png files", "*png*"), ("all files", "*.*")))
        label = tk.Label(self.labelFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.filename)
        self.encrypt()

    def fileImg(self):
        self.hiddename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("jpeg files", "*.jpg"), ("png files", "*png*"), ("all files", "*.*")))
        label = tk.Label(self.hiddenFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.hiddename)
        self.encrypt()

    def fileTxt(self):
        self.hiddename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("text files", "*.txt"), ("all files", "*.*")))
        label = tk.Label(self.hiddenFrame, text="")
        label.grid(column=0, row=2, sticky="W")
        label.configure(text=self.hiddename)
        self.encrypt()

    def fileother(self):
        self.hiddename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("all files", "*.*"),))
        label = tk.Label(self.hiddenFrame, text="")
        label.grid(column=0, row=2, sticky="W")
        label.configure(text=self.hiddename)
        self.encrypt()

    def passwordGrid(self):
        psw = tk.Entry(self.passwordFrame, font=('calibre', 10, 'normal'))
        psw.grid(column=0, row=1, sticky="W")
        self.button4 = tk.Button(
            self.passwordFrame, text="Confirm", command=lambda: self.confirm(psw))
        self.button4.grid(column=1, row=1, sticky="We")
        self.encrypt()

    def confirm(self, psw):
        self.password = ''
        self.password = psw.get()
        label = tk.Label(self.passwordFrame, text="")
        label.grid(column=0, row=2, sticky="We", columnspan=3)
        if len(self.password) >= 15:
            text = self.password[0:15]
            text += "..."
        else:
            text = self.password
        label.configure(text=text)
        self.encrypt()

    def deleteFrame(self, element):
        for widget in element.winfo_children():
            widget.grid_forget()

    def choix(self):
        rdioOne = tk.Radiobutton(self.choixFrame, text='Image',
                                 variable=self.radioValue, value=3, command=self.importSneakMess)
        rdioTwo = tk.Radiobutton(self.choixFrame, text='txt file',
                                 variable=self.radioValue, value=1, command=self.importSneakMess)
        rdioThree = tk.Radiobutton(self.choixFrame, text='Write',
                                   variable=self.radioValue, value=2, command=self.importSneakMess)
        rdiofor = tk.Radiobutton(self.choixFrame, text='Other',
                                 variable=self.radioValue, value=0, command=self.importSneakMess)

        rdioOne.grid(column=0, row=0, sticky="W")
        rdioTwo.grid(column=1, row=0, sticky="W")
        rdioThree.grid(column=0, row=1, sticky="W")
        rdiofor.grid(column=1, row=1, sticky="W")

    def radioContainer(self):
        rdioOne = tk.Radiobutton(self.choixContainer, text='Image',
                                 variable=self.containerValue, value=0, command=self.importContainer)
        rdioTwo = tk.Radiobutton(self.choixContainer, text='Video',
                                 variable=self.containerValue, value=1, command=self.importContainer)
        rdioOne.grid(column=0, row=0, sticky="W")
        rdioTwo.grid(column=1, row=0, sticky="W")

    def importContainer(self):
        self.deleteFrame(self.labelFrame)
        if self.containerValue.get() == 1:
            self.button1 = tk.Button(
                self.labelFrame, text="Browse A video", command=self.fileVid)
            self.button1.grid(column=0, row=1, sticky="W")
        else:
            self.search()

    def fileVid(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(("mp4 files", "*.mp4"), ("avi files", "*.avi"), ("all files", "*.*")))
        label = tk.Label(self.labelFrame, text="")
        label.grid(column=0, row=2, sticky="We")
        label.configure(text=self.filename)
        self.encrypt()

    def validation(self, mess):
        self.hiddename = mess.get()
        label = tk.Label(self.hiddenFrame, text="")
        label.grid(column=0, row=2, sticky="We", columnspan=3)
        if len(self.hiddename) >= 15:
            text = self.hiddename[0:15]
            text += "..."
        else:
            text = self.hiddename
        label.configure(text=text)
        self.encrypt()

    def importSneakMess(self):
        self.deleteFrame(self.hiddenFrame)
        self.hiddename = ''
        if self.radioValue.get() == 3:
            self.button2 = tk.Button(
                self.hiddenFrame, text="Browse A Image", command=self.fileImg)
            self.button2.grid(column=0, row=1, sticky="W")
        elif self.radioValue.get() == 1:
            self.button2 = tk.Button(
                self.hiddenFrame, text="Browse A Txt", command=self.fileTxt)
            self.button2.grid(column=0, row=1, sticky="W")
        elif self.radioValue.get() == 2:
            mess = tk.Entry(self.hiddenFrame, font=('calibre', 10, 'normal'))
            mess.grid(column=0, row=1, sticky="W")
            self.button2 = tk.Button(
                self.hiddenFrame, text="Valider", command=lambda: self.validation(mess))
            self.button2.grid(column=2, row=1, sticky="W")
        else:
            self.button2 = tk.Button(
                self.hiddenFrame, text="Browse", command=self.fileother)
            self.button2.grid(column=0, row=1, sticky="W")

        self.encrypt()


class MainView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        global img, img1
        height = 150
        width = 200
        encryptframe = tk.Frame(parent, bg='#007fff',
                                borderwidth=10, highlightbackground="black")
        labelEncrypt = tk.Label(encryptframe, text="Encode", font=(
            "Helvetica", 20, 'bold'), bg='#007fff', fg="white")
        labelEncrypt.pack()

        img = ImageTk.PhotoImage(file="ressource/encrypt.jpg")
        encryptCan = tk.Canvas(encryptframe, width=width, height=height,
                               bg='#007fff', bd=0, highlightthickness=0, cursor='hand2')
        encryptImage = encryptCan.create_image(
            height / 2, width / 2, image=img)
        encryptCan.tag_bind(encryptImage, '<1>', EncryptWin)
        encryptCan.pack()

        decryptframe = tk.Frame(parent, bg='#007fff',
                                borderwidth=10, highlightbackground="black")
        labelDecrypt = tk.Label(decryptframe, text="Decode", font=(
            "Helvetica", 20, 'bold'), bg='#007fff', fg="white")
        labelDecrypt.pack()

        img1 = ImageTk.PhotoImage(file="ressource/decripte.jpg")
        decryptCan = tk.Canvas(decryptframe, width=width, height=height,
                               bg='#007fff', bd=0, highlightthickness=0, cursor='hand2')
        decryptImage = decryptCan.create_image(
            height / 2, width / 2, image=img1)
        decryptCan.tag_bind(encryptImage, '<1>', DeceryptWin)
        decryptCan.pack()

        decryptframe.pack(side=tk.RIGHT, padx=10)
        encryptframe.pack(side=tk.LEFT, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("ressource/logo.ico")
    main = MainView(root)
    root.title("Bicryptimage")
    root.geometry("520x380")
    root.resizable(width=0, height=0)
    root.config(bg='#007fff')
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
