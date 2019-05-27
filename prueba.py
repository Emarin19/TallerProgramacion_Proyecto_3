from tkinter import *

master = Tk()

listbox = Listbox(master)
listbox.pack()
arch = open("Tabla de posiciones Autos.txt","r+")
Lista = arch.readlines()

#listbox.insert(END, Lista)

for item in Lista:
    listbox.insert(END, item)

mainloop()
