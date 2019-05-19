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
Forward = False
Back = False
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

#Creando el cliente para NodeMCU
myCar = NodeMCU()
myCar.start()

def get_log():
    """
    Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
    """
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
    
p = Thread(target=get_log)
p.start()
           
L_Titulo = Label(C_main,text="Mensaje:",font=('Agency FB',14),bg='white',fg='blue')
L_Titulo.place(x=100,y=250)

E_Command = Entry(C_main,width=30,font=('Agency FB',14))
E_Command.place(x=200,y=250)

L_Titulo = Label(C_main,text="ID mensaje:",font=('Agency FB',14),bg='white',fg='blue')
L_Titulo.place(x=100,y=300)

E_read = Entry(C_main,width=30,font=('Agency FB',14))
E_read.place(x=200,y=300)

    
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

def sendShowID():
    """
    Ejemplo como capturar un ID de un mensaje específico.
    """
    mns = str(E_Command.get())
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        mnsID = myCar.send(mns)
        messagebox.showinfo("Mensaje pendiente", "Intentando enviar mensaje, ID obtenido: {0}\n\
La respuesta definitiva se obtine en un máximo de {1}s".format(mnsID, myCar.timeoutLimit))
        
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

def read():
    """
    Ejemplo de como leer un mensaje enviado con un ID específico
    """
    mnsID = str(E_read.get())
    if(len(mnsID)>0 and ":" in mnsID):
        mns = myCar.readById(mnsID)
        if(mns != ""):
            messagebox.showinfo("Resultado Obtenido", "El mensaje con ID:{0}, obtuvo de respuesta:\n{1}".format(mnsID, mns))
            E_read.delete(0, 'end')
        else:
            messagebox.showerror("Error de ID", "No se obtuvo respuesta\n\
El mensaje no ha sido procesado o el ID es invalido\n\
Asegurese que el ID: {0} sea correcto".format(mnsID))

    else:
        messagebox.showwarning("Error en formato", "Recuerde ingresar el separador (':')")

main.bind('<Return>', send) #Vinculando tecla Enter a la función send



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
#__________/ DRIVING TEST WINDOWS

def test_drive():
    #Esconder ventana principal
    main.withdraw()
    #Ventana testeo del carro y sus atributos
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
        """
        Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
        """
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


    def move_forward(event):
        pwm=400
        mns="pwm:"
        En=1
        p=Thread(target=move_forward_aux,args=(pwm,mns,En)).start()

    def move_forward_aux(pwm,mns,En):
        global Stop
        if Stop == False:
            if pwm<1000 and En==1:
                print("A")
                mns=mns+str(pwm)+";"
                myCar.send(mns)
                pwm=pwm+10
                time.sleep(0.01)
                test.update()
                return move_forward_aux(pwm+10,mns,En)
            else:
                En=0
                print("B")
                pwm=pwm-10
                mns=mns+str(pwm)+";"
                myCar.send(mns)
                time.sleep(0.01)
                test.update()
                return move_forward_aux(pwm-10,mns,En)
        else:
            print("I can´t")

    def stop(event):
        Stop=True
        print(Stop)
        test.update()
            

    def move_back(event):
        mns="pwm:-700;"
        myCar.send(mns)

    def front_lights(event):
        global Lfront
        if Lfront == False:
            mns="lf:1;"
            myCar.send(mns)
            Lfront = True

        else:
            mns="lf:0;"
            myCar.send(mns)
            Lfront = False

    def back_lights(event):
        global Lback
        if Lback == False:
            mns = "lb:1;"
            myCar.send(mns)
            Lback = True

        else:
            mns = "lb:0;"
            myCar.send(mns)
            Lback = False

    def left_light(event):
        global Lleft
        if Lleft == False:
            mns = "ll:1;"
            myCar.send(mns)
            Lleft = True

        else:
            mns = "ll:0;"
            myCar.send(mns)
            Lleft = False

    def right_light(event):
        global Lright
        if Lright == False:
            mns = "lr:1;"
            myCar.send(mns)
            Lright = True

        else:
            mns = "lr:0;"
            myCar.send(mns)
            Lright = False
        
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


    test.bind('<Return>', send) #Vinculando tecla Enter a la función send
    test.bind("<Up>", move_forward)
    test.bind("<Down>", move_back)
    test.bind("<KeyRelease>",stop)
    test.bind("b", back_lights)
    test.bind("f", front_lights)
    test.bind("l", left_light)
    test.bind("r", right_light)
    
    p = Thread(target=get_log)
    p.start()
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
