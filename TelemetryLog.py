"""
Instituto Tecnológico de Costa Rica
Computer Engineering
Taller de Programación

Ejemplo Consola Cliente
Implementación del módulo NodeMCU
Proyecto 2 y 3, Semestre 1
2019

Profesor: Milton Villegas Lemus
Autor: Santiago Gamboa Ramirez
       Emanuel Marín Gutiérrez
       Alejandro Vasquez Oviedo

Restricciónes: Python3.7 
Ejemplo de como usar el módudo NodeMCU de wifiConnection

"""
#           _____________________________________________________
#__________/BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from tkinter import messagebox      # AskYesNo ()
from threading import Thread        # p.start()
from random import randint          #
import random                       #
import threading                    # 
import winsound                     # Playsound
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)
import tkinter.scrolledtext as tkscrolled
import pygame

##### Biblioteca para el Carro
from WiFiClient import NodeMCU

#Función para cargar imágenes
#Código tomado de ejemplo de Santiago
def loadImg(name):
    ruta=os.path.join("imgs",name)
    imagen=PhotoImage(file=ruta)
    return imagen

#Variables globales
#Manejo del carro
global Forward, Back, Left, Right, Lfront, Lback, Lleft, Lright, Stop
Forward = 400
Back = -400
Left = False
Left = False
Lfront = False
Lback = False
Lleft = False
Lright = False
Stop = False

#           _____________________________________________________
#__________/ VENTANA PRINCIPAL

#Creación ventana principal y sus atributos
main=Tk()
main.title("Proyecto 3")
main.minsize(800,600)
main.resizable(width=NO,height=NO)

#Canvas de la ventana principal
C_main=Canvas(main, width=800,height=600, bg='white')
C_main.place(x=0,y=0)

#Labels (Más adelante los quitamos)
L_Titulo = Label(C_main,text="Mensajes Enviados",font=('Agency FB',14),bg='white',fg='blue')
L_Titulo.place(x=100,y=10)

L_Titulo = Label(C_main,text="Respuesta Mensaje",font=('Agency FB',14),bg='white',fg='blue')
L_Titulo.place(x=490,y=10)

SentCarScrolledTxt = tkscrolled.ScrolledText(C_main, height=10, width=45)
SentCarScrolledTxt.place(x=10,y=50)

RevCarScrolledTxt = tkscrolled.ScrolledText(C_main, height=10, width=45)
RevCarScrolledTxt.place(x=400,y=50)
 
L_Titulo = Label(C_main,text="Mensaje:",font=('Agency FB',14),bg='white',fg='blue')
L_Titulo.place(x=100,y=250)

E_Command = Entry(C_main,width=30,font=('Agency FB',14))
E_Command.place(x=200,y=250)

L_Titulo = Label(C_main,text="ID mensaje:",font=('Agency FB',14),bg='white',fg='blue')
L_Titulo.place(x=100,y=300)

E_read = Entry(C_main,width=30,font=('Agency FB',14))
E_read.place(x=200,y=300)


def w_description():
    #Esconder ventana principal
    main.withdraw()
    #Ventana de testeo del carro y sus atributos
    about=Toplevel()
    about.title("About of")
    about.minsize(800,600)
    about.resizable(width=NO, height=NO)

    C_about = Canvas(about, width=800, height=600, bg="white")
    C_about.place(x=0, y=0)

    def back():
        about.destroy()
        main.deiconify()

    Btn_back = Button(about, text="Back", command=back, bg="light blue", fg='black')
    Btn_back.place(x=10,y=10)

    main.mainloop()

def positions_table():
    #Esconder ventana principal
    main.withdraw()
    #Ventana de testeo del carro y sus atributos
    positions=Toplevel()
    positions.title("Positions Table")
    positions.minsize(800,600)
    positions.resizable(width=NO, height=NO)

    C_positions = Canvas(positions, width=800, height=600, bg="white")
    C_positions.place(x=0, y=0)

    def back():
        positions.destroy()
        main.deiconify()

    Btn_back = Button(positions, text="Back", command=back, bg="light blue", fg='black')
    Btn_back.place(x=10,y=10)



    main.mainloop()



#           _____________________________________________________
#__________/ DRIVING TEST WINDOW

def test_drive():
    #Esconder ventana principal
    main.withdraw()
    #Ventana de testeo del carro y sus atributos
    test=Toplevel()
    test.title("Driving Test")
    test.minsize(800,600)
    test.resizable(width=NO, height=NO)

    C_test = Canvas(test, width=800, height=600, bg="white")
    C_test.place(x=0, y=0)

    #Creando el cliente para NodeMCU
    myCar = NodeMCU()
    myCar.start()

    def get_log():
        #Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
        indice = 0
        while(myCar.loop):
            while(indice < len(myCar.log)):
                mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
                SentCarScrolledTxt.insert(END,mnsSend)
                SentCarScrolledTxt.see("end")

                mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
                RevCarScrolledTxt.insert(END, mnsRecv)
                RevCarScrolledTxt.see('end')

                indice+=1
            time.sleep(0.200)

    def lights(event):
        global Lfront, Lback, Lleft, Lright 
        if event.char == "f":
            if Lfront == False:
                mns="lf:1;"
                myCar.send(mns)
                Lfront = True
            else:
                mns="lf:0;"
                myCar.send(mns)
                Lfront = False
                
        if event.char == "b":
            if Lback == False:
                mns = "lb:1;"
                myCar.send(mns)
                Lback = True
            else:
                mns = "lb:0;"
                myCar.send(mns)
                Lback = False

        if event.char == "l":
            if Lleft == False:
                mns = "ll:1;"
                myCar.send(mns)
                Lleft = True
            else:
                mns = "ll:0;"
                myCar.send(mns)
                Lleft = False

        if event.char == "r":
            if Lright == False:
                mns = "lr:1;"
                myCar.send(mns)
                Lright = True
            else:
                mns = "lr:0;"
                myCar.send(mns)
                Lright = False

    def move_forward(event):
        global Forward, Back
        Back = -400
        if Forward <1023:
            Forward+=1
            print(Forward)
            mns = "pwm:" + str(Forward) + ";"
            myCar.send(mns)
            time.sleep(0.01)
        else:
            Forward = 1023
            print(Forward)
            mns = "pwm:" + str(Forward) + ";"
            myCar.send(mns)
            time.sleep(0.01)
 
    def move_back(event):
        global Forward, Back
        Forward = 400
        if Back>-1023:
            Back-=1
            print(Back)
            mns = "pwm:" + str(Back) + ";"
            myCar.send(mns)
            time.sleep(0.01)
        else:
            Back = -1023
            print(Back)
            mns = "pwm:" + str(Back) + ";"
            myCar.send(mns)
            time.sleep(0.01)
            
    def stop(event):
    	global Forward, Back
    	Forward = 400
    	Back = -400
    	velocidad = 0
    	mns = "pwm:" + str(velocidad) + ";"
    	myCar.send(mns)


    def move_left(event):
        mns = "dir:-1;"
        myCar.send(mns)
        
    def move_right(event):
        mns = "dir:1;"
        myCar.send(mns)

    def move_direct(event):
        mns = "dir:0;"
        myCar.send(mns)

    def send (event):
        """
        Ejemplo como enviar un mensaje sencillo sin importar la respuesta
        """
        mns = str(E_Command.get())
        if(len(mns)>0 and mns[-1] == ";"):
            E_Command.delete(0, 'end')
            myCar.send(mns)
        else:
            messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

    def back():
        test.destroy()
        main.deiconify()

    Btn_back = Button(test, text="Back", command=back, bg="light blue", fg='black')
    Btn_back.place(x=10,y=10)

    test.bind("<Up>", move_forward)
    test.bind("<Down>", move_back)
    test.bind("p", stop)
    test.bind("<Left>", move_left)
    test.bind("<Right>", move_right)
    test.bind("d", move_direct)
    #test.bind("<KeyRelease>",stop)
    test.bind("<Key>",lights)

    p = Thread(target=get_log).start()
    main.mainloop()
    
#           ____________________________
#__________/BOTONES VENTANA PRINCIPAL

Btn_Test_Drive = Button(C_main,text="About",command=w_description,fg="white",bg="blue", font=("Agency FB",12))
Btn_Test_Drive.place(x=300,y=550)

Btn_Test_Drive = Button(C_main,text="Positions Table",command=positions_table,fg="white",bg="blue", font=("Agency FB",12))
Btn_Test_Drive.place(x=500,y=550)

Btn_Test_Drive = Button(C_main,text="Test Drive",command=test_drive,fg="white",bg="blue", font=("Agency FB",12))
Btn_Test_Drive.place(x=500,y=500)

Btn_ConnectControl = Button(C_main,text='Send',command=lambda:send(None),fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=250)

Btn_Controls = Button(C_main,text='Send & Show ID',command=sendShowID,fg='white',bg='blue', font=('Agency FB',12))
Btn_Controls.place(x=500,y=250)

Btn_ConnectControl = Button(C_main,text='Leer Mensaje',command=read,fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=300)
main.mainloop()
