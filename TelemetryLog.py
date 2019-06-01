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
from tkinter import ttk

from prueba import *
##### Biblioteca para el Carro
from WiFiClient import NodeMCU

#Función para cargar imágenes
#Código tomado de ejemplo de Santiago
def loadImg(name):
    ruta=os.path.join("Imágenes",name)
    imagen=PhotoImage(file=ruta)
    return imagen

#Imágenes a usar
#2019A = loadImg

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

def move_forward(event):
    mns=str("pwm:600;")
    myCar.send(mns)

def move_back(event):
    mns="pwm:-700;"
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
main.bind ("<Up>", move_forward)
main.bind ("<Down>", move_back)


def w_description():
    #Esconder ventana principal
    main.withdraw()
    #Ventana de testeo del carro y sus atributos
    about=Toplevel()
    about.title("About of")
    about.minsize(800,600)
    about.resizable(width=NO, height=NO)

    C_about = Canvas(about, width=800, height=600, bg="black")
    C_about.place(x=0, y=0)

    fondo = loadImg("about.gif")

    L_fondo = Label(C_about,bg='black')
    L_fondo.place(x=0,y=0)
    L_fondo.config(image=fondo)
    def back():
        about.destroy()
        main.deiconify()

    Btn_back = Button(about, text="Back", command=back, bg="light blue", fg='black')
    Btn_back.place(x=10,y=570)

    main.mainloop()

def positions_table():
    #Esconder ventana principal
    main.withdraw()
    #Ventana de posiciones
    positions=Toplevel()
    positions.title("Positions Table")
    positions.minsize(800,650)
    positions.resizable(width=NO, height=NO)     

#Código para las pestañas    
    tab_control = ttk.Notebook(positions)
    tab1 = ttk.Frame(tab_control) 
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Pilotos')
    tab_control.add(tab2, text='Autos')

    C_positionsP = Canvas(tab1, width=800, height=650)
    C_positionsP.place(x=0, y=0)
    
    C_positionsA = Canvas(tab2, width=800, height=650)
    C_positionsA.place(x=0, y=0)
#Abrir documento de pilotos y autos  
    arch_pilotos = open("Tabla de posiciones Pilotos.txt","r+")
    lista_pilotos = arch_pilotos.readlines()

    arch_autos = open("Tabla de posiciones Autos.txt","r+")
    lista_autos = arch_autos.readlines()
#Imágenes a usar
    Piloto1 = loadImg(lista_pilotos[0][:9])
    Piloto2 = loadImg(lista_pilotos[1][:9])
    Piloto3 = loadImg(lista_pilotos[2][:9])
    Piloto4 = loadImg(lista_pilotos[3][:9])
    Piloto5 = loadImg(lista_pilotos[4][:9])
    Piloto6 = loadImg(lista_pilotos[5][:9])
    Piloto7 = loadImg(lista_pilotos[6][:9])
    Piloto8 = loadImg(lista_pilotos[7][:9])
    Piloto9 = loadImg(lista_pilotos[8][:9])
    Piloto10 = loadImg(lista_pilotos[9][:9])

    Auto1 = loadImg(lista_autos[0][:8])
    Auto2 = loadImg(lista_autos[1][:8])
    Auto3 = loadImg(lista_autos[2][:8])
    Auto4 = loadImg(lista_autos[3][:8])
    Auto5 = loadImg(lista_autos[4][:8])
    Auto6 = loadImg(lista_autos[5][:8])
    Auto7 = loadImg(lista_autos[6][:8])
    Auto8 = loadImg(lista_autos[7][:8])
    Auto9 = loadImg(lista_autos[8][:8])
    Auto10 = loadImg(lista_autos[9][:8])

    Edit_F = loadImg("Fondo.png")
    
#Configuración del Fondo
    Fondo_Pilotos = loadImg("Fondo Tabla Pilotos.png")
    C_positionsP.create_image(0,0,image=Fondo_Pilotos, anchor=NW,state=NORMAL)

    Fondo_Autos = loadImg("Fondo Tabla Autos.png")
    C_positionsA.create_image(0,0,image=Fondo_Autos, anchor=NW,state=NORMAL)

#Imágenes y textos de pilotos
    def carg_pilotos():
        y = 75
        for i in range(0,10):
            C_positionsP.create_text(120,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][10:nombres(lista_pilotos[i])])
            C_positionsP.create_text(405,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][edad(lista_pilotos[i])[0]:edad(lista_pilotos[i])[1]]) #Edad y nacionalidad
            C_positionsP.create_text(528,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][edad(lista_pilotos[i])[1]:edad(lista_pilotos[i])[2]])
            C_positionsP.create_text(592,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][edad(lista_pilotos[i])[2]:])
            
            y+=55
            
        C_positionsP.create_image(65,55,image=Piloto1, anchor=NW,tags=("pilot"),state=NORMAL)           
        C_positionsP.create_image(65,105,image=Piloto2, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,159,image=Piloto3, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,212,image=Piloto4, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,265,image=Piloto5, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,317,image=Piloto6, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,368,image=Piloto7, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,422,image=Piloto8, anchor=NW,tags=("pilot"),state=NORMAL)
        C_positionsP.create_image(65,475,image=Piloto9, anchor=NW,tags=("pilot"),state=NORMAL)    
        C_positionsP.create_image(65,527,image=Piloto10, anchor=NW,tags=("pilot"),state=NORMAL)
        
    carg_pilotos()

#Labels de Autos
    def carg_autos():
        y = 75
        for i in range(0,10):
            C_positionsA.create_text(180,y,font=("Arial", 10, "bold"), anchor=NW,fill="white", text=lista_autos[i][8:nombres(lista_autos[i])])
            C_positionsA.create_text(380,y,font=("Arial", 10, "bold"), anchor=NW,fill="white", text=lista_autos[i][edad_a(lista_autos[i])[0]:edad_a(lista_autos[i])[1]])
            C_positionsA.create_text(500,y,font=("Arial", 10, "bold"), anchor=NW,fill="white", text=lista_autos[i][edad_a(lista_autos[i])[1]:])

            y+=55
            
        C_positionsA.create_image(65,65,image=Auto1, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,115,image=Auto2, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,169,image=Auto3, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,227,image=Auto4, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,280,image=Auto5, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,337,image=Auto6, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,383,image=Auto7, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,437,image=Auto8, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,485,image=Auto9, anchor=NW,state=NORMAL)
        C_positionsA.create_image(65,542,image=Auto10, anchor=NW,state=NORMAL)
            
    carg_autos()
    tab_control.pack(expand=1, fill='both')
#Funciones de botones
    def back():
        arch_autos.close()
        arch_pilotos.close()
        positions.destroy()
        main.deiconify()

        
    def edit_textP(y,Elegir,i):
        positions.attributes('-disabled', True)
        edit=Toplevel()
        edit.title("Edit")
        edit.minsize(650,100)
        edit.resizable(width=NO, height=NO)
        C_edit=Canvas(edit, width=650,height=650, bg='light blue')
        C_edit.place(x=0,y=0)
        C_edit.create_image(0,0,image=Edit_F, anchor=NW,state=NORMAL)
        Lista = 0
        arch = 0
        if Elegir == 0:
            arch = open("Tabla de posiciones Autos.txt","r+")
            Lista = arch.readlines()
        if Elegir == 1:    
            arch = open("Tabla de posiciones Pilotos.txt","r+")
            Lista = arch.readlines()
        if Elegir == 1:    
            C_edit.create_text(5,70,font=("Arial", 12, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Nombre:")
            C_edit.create_text(200,80,font=("Arial", 9, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Edad Nacionalidad Temporada")
            C_edit.create_text(380,80,font=("Arial",9,"bold"),anchor=NW,tags=("pilot"),fill="white",text="Compet. RGP REP")
        if Elegir == 0:
            C_edit.create_text(5,70,font=("Arial", 12, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Marca:")
            C_edit.create_text(200,80,font=("Arial", 9, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Modelo Temp.")
            C_edit.create_text(380,80,font=("Arial",9,"bold"),anchor=NW,tags=("pilot"),fill="white",text="Eficiencia") 
        
        E_name = Entry(C_edit,text="hola",width=25,font=("Agency FB",14))
        E_name.place(x=0,y=100)
        E_age = Entry(C_edit,text="texto",width=20,font=("Agency FB",14))
        E_age.place(x=210,y=100)
        E_rest = Entry(C_edit,width=15,font=("Agency FB",14))
        E_rest.place(x=380,y=100)
        def mod_entry(y,i,n,Elegir):
            if Elegir == 1:
                if y == 75:
                    E_name.insert(END,Lista[0][9:nombres(Lista[0])]) #This works
                    E_age.insert(0,Lista[0][edad(lista_pilotos[0])[0]:edad(lista_pilotos[0])[2]])
                    E_rest.insert(0,Lista[0][edad(lista_pilotos[0])[2]:])
                    return
                if y == n:
                    E_name.insert(END,Lista[i][9:nombres(Lista[i])])
                    E_age.insert(0,Lista[i][edad(lista_pilotos[i])[0]:edad(lista_pilotos[i])[2]])
                    E_rest.insert(0,Lista[0][edad(lista_pilotos[i])[2]:])
                    return
                else:
                    return mod_entry(y,i+1,n+55,Elegir)
            elif Elegir == 0:
                if y == 75:
                    E_name.insert(END,Lista[0][9:nombres(Lista[0])]) #This works
                    E_age.insert(0,Lista[0][edad_a(lista_autos[0])[0]:edad_a(lista_autos[0])[1]])
                    E_rest.insert(0,Lista[0][edad_a(lista_autos[0])[1]:])
                    return
                if y == n:
                    E_name.insert(END,Lista[i][9:nombres(Lista[i])])
                    E_age.insert(0,Lista[i][edad_a(lista_autos[i])[0]:edad_a(lista_autos[i])[1]])
                    E_rest.insert(0,Lista[i][edad_a(lista_autos[i])[1]:])
                    return
                else:
                    return mod_entry(y,i+1,n+55,Elegir)
        mod_entry(y,1,125,Elegir)
        def cambiar(i,Lista,Elegir):
            Nombre = str(E_name.get())
            Datos1 = str(E_age.get())
            Datos2 = str(E_rest.get())
            AEscribir = Lista[i][:10]+str(E_name.get())+str(E_age.get())+" "+str(E_rest.get())
            
            Lista[i] = AEscribir
            if Elegir == 0:
                arch = open("Tabla de posiciones Autos.txt","w")
                arch.writelines(Lista)
                arch.close

            elif Elegir == 1:
                arch = open("Tabla de posiciones Pilotos.txt","w")
                arch.writelines(Lista)
                arch.close
            
            E_name.delete(0, END)
            E_age.delete(0, END)
            E_rest.delete(0,END)
            arch.close()
            positions.attributes('-disabled', False)
            edit.destroy()
            positions.destroy()
            positions_table()
        def disable_event():
            E_name.delete(0, END)
            E_age.delete(0, END)
            E_rest.delete(0,END)
            arch.close()
            positions.attributes('-disabled', False)
            edit.destroy()
        edit.protocol("WM_DELETE_WINDOW", disable_event)
        Btn_back = Button(edit, text="Confirmar cambio", command=lambda: cambiar(i,Lista,Elegir), bg="light blue", fg='black')
        Btn_back.place(x=530,y=100)

        
################  FUNCIONES ORDENAMIENTO AUTOS ##########################
    def descendenteA():
        def seleccion(Lista):
            return seleccion_aux(Lista,0,len(Lista),0)

        def menor(Lista,j,n,Min):
            if j == n:
                return Min
            if Lista[j][-6:] > Lista[Min][-6:]:
                Min = j
            return menor(Lista,j+1,n,Min)
            
        def seleccion_aux(Lista,i,n,ContadorRep):
            if i == n:
                return Lista
            Min = menor(Lista,i+1,n,i)
            Tmp = Lista[i]
            Lista[i] = Lista[Min]
            Lista[Min] = Tmp
            return seleccion_aux(Lista,i+1,n,ContadorRep+1)
        TablaAutos = open("Tabla de posiciones Autos.txt","r+")
        Lista = TablaAutos.readlines()
        TablaAutos.seek(0)
        TablaAutos.write(''.join(seleccion(Lista)))
        TablaAutos.close()
        positions.destroy()
        positions_table()

    def ascendenteA():
        def seleccion(Lista):
            return seleccion_aux(Lista,0,len(Lista),0)

        def menor(Lista,j,n,Min):
            if j == n:
                return Min
            if Lista[j][-6:] < Lista[Min][-6:]:
                Min = j
            return menor(Lista,j+1,n,Min)
            
        def seleccion_aux(Lista,i,n,ContadorRep):
            if i == n:
                return Lista
            Min = menor(Lista,i+1,n,i)
            Tmp = Lista[i]
            Lista[i] = Lista[Min]
            Lista[Min] = Tmp
            return seleccion_aux(Lista,i+1,n,ContadorRep+1)
        TablaAutos = open("Tabla de posiciones Autos.txt","r+")
        Lista = TablaAutos.readlines()
        TablaAutos.seek(0)
        TablaAutos.write(''.join(seleccion(Lista)))
        positions.update
        TablaAutos.close()
        positions.update
        positions.destroy()
        positions_table()
        #Thread(target=positions_table,args=()).start()
########################################################################


################  FUNCIONES ORDENAMIENTO PILOTOS ##########################
    def descendenteP_REP():
        def seleccion(Lista):
            return seleccion_aux(Lista,0,len(Lista),0)

        def menor(Lista,j,n,Min):
            if j == n:
                return Min
            if Lista[j][-6:] > Lista[Min][-6:]:
                Min = j
            return menor(Lista,j+1,n,Min)
            
        def seleccion_aux(Lista,i,n,ContadorRep):
            if i == n:
                return Lista
            Min = menor(Lista,i+1,n,i)
            Tmp = Lista[i]
            Lista[i] = Lista[Min]
            Lista[Min] = Tmp
            return seleccion_aux(Lista,i+1,n,ContadorRep+1)
        TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
        Lista = TablaAutos.readlines()
        TablaAutos.seek(0)
        TablaAutos.write(''.join(seleccion(Lista)))
        TablaAutos.close()
        positions.destroy()
        #positions.delete("pilot")
        positions_table()

    def ascendenteP_REP():
        def seleccion(Lista):
            return seleccion_aux(Lista,0,len(Lista),0)

        def menor(Lista,j,n,Min):
            if j == n:
                return Min
            if Lista[j][-6:] < Lista[Min][-6:]:
                Min = j
            return menor(Lista,j+1,n,Min)
            
        def seleccion_aux(Lista,i,n,ContadorRep):
            if i == n:
                return Lista
            Min = menor(Lista,i+1,n,i)
            Tmp = Lista[i]
            Lista[i] = Lista[Min]
            Lista[Min] = Tmp
            return seleccion_aux(Lista,i+1,n,ContadorRep+1)
        TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
        Lista = TablaAutos.readlines()
        TablaAutos.seek(0)
        TablaAutos.write(''.join(seleccion(Lista)))
        TablaAutos.close()
        positions.destroy()
        positions_table()
        #positions_table()
###########################################################################
    def descendenteP_RGP():
        def seleccion(Lista):
            return seleccion_aux(Lista,0,len(Lista),0)

        def menor(Lista,j,n,Min):
            if j == n:
                return Min
            if Lista[j][-12:-6] > Lista[Min][-12:-6]:
                print(Lista[j][-12:-6])
                Min = j
            return menor(Lista,j+1,n,Min)
            
        def seleccion_aux(Lista,i,n,ContadorRep):
            if i == n:
                return Lista
            Min = menor(Lista,i+1,n,i)
            Tmp = Lista[i]
            Lista[i] = Lista[Min]
            Lista[Min] = Tmp
            return seleccion_aux(Lista,i+1,n,ContadorRep+1)
        TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
        Lista = TablaAutos.readlines()
        TablaAutos.seek(0)
        TablaAutos.write(''.join(seleccion(Lista)))
        TablaAutos.close()
        positions.destroy()
        positions_table()

    def ascendenteP_RGP():
        def seleccion(Lista):
            return seleccion_aux(Lista,0,len(Lista),0)

        def menor(Lista,j,n,Min):
            if j == n:
                return Min
            if Lista[j][-12:-6] < Lista[Min][-12:-6]:
                Min = j
            return menor(Lista,j+1,n,Min)
            
        def seleccion_aux(Lista,i,n,ContadorRep):
            if i == n:
                return Lista
            Min = menor(Lista,i+1,n,i)
            Tmp = Lista[i]
            Lista[i] = Lista[Min]
            Lista[Min] = Tmp
            return seleccion_aux(Lista,i+1,n,ContadorRep+1)
        TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
        Lista = TablaAutos.readlines()
        TablaAutos.seek(0)
        TablaAutos.write(''.join(seleccion(Lista)))
        TablaAutos.close()
        positions.destroy()
        positions_table()

###########################################################################
        
#Botones de la ventana
    Btn_back = Button(positions, text="Back", command=back, bg="light blue", fg='black')
    Btn_back.place(x=750,y=615)    
#Botones pestaña pilotos
    Btn_Descendente =Button(tab1, text="Descendente REP", command=descendenteP_REP, bg="light blue", fg='black')
    Btn_Descendente.place(x=270,y=592)
    
    Btn_Ascendente =Button(tab1, text="Ascendente REP", command=ascendenteP_REP, bg="light blue", fg='black')
    Btn_Ascendente.place(x=380,y=592)

    Btn_Descendente =Button(tab1, text="Descendente RGP", command=descendenteP_RGP, bg="light blue", fg='black')
    Btn_Descendente.place(x=490,y=592)
    
    Btn_Ascendente =Button(tab1, text="Ascendente RGP", command=ascendenteP_RGP, bg="light blue", fg='black')
    Btn_Ascendente.place(x=600,y=592)
    
    #Botones de edición de texto
    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(75,1,0), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=75)
    
    Btn_Edit =Button(tab1, text="Edit", command= lambda: edit_textP(125,1,1), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=125)

    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(180,1,2), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=180)

    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(235,1,3), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=235)
    
    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(290,1,4), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=290)
    
    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(345,1,5), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=345)

    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(400,1,6), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=400)

    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(455,1,7), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=455)

    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(510,1,8), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=510)

    Btn_Edit =Button(tab1, text="Edit", command=lambda: edit_textP(565,1,9), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=565)
    
#Botones pestaña autos
    Btn_DescendenteA =Button(tab2, text="Descendente", command=descendenteA, bg="light blue", fg='black')
    Btn_DescendenteA.place(x=500,y=587)
    
    Btn_AscendenteA =Button(tab2, text="Ascendente", command=ascendenteA, bg="light blue", fg='black')
    Btn_AscendenteA.place(x=600,y=587)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(75,0,0), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=75)
    
    Btn_Edit =Button(tab2, text="Edit", command= lambda: edit_textP(125,0,1), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=125)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(180,0,2), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=180)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(235,0,3), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=235)
    
    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(290,0,4), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=290)
    
    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(345,0,5), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=345)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(400,0,6), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=400)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(455,0,7), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=455)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(510,0,8), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=510)

    Btn_Edit =Button(tab2, text="Edit", command=lambda: edit_textP(565,0,9), bg="light blue", fg='black')
    Btn_Edit.place(x=750,y=565)
    
    main.mainloop()

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

    def back():
        test.destroy()
        main.deiconify()

    Btn_back = Button(test, text="Back", command=back, bg="light blue", fg='black')
    Btn_back.place(x=10,y=10)

    main.mainloop()
        
#           ____________________________
#__________/BOTONES VENTANA PRINCIPAL

Btn_Test_Drive = Button(C_main,text="About",command=w_description,fg="white",bg="blue", font=("Agency FB",12))
Btn_Test_Drive.place(x=300,y=550)

Btn_Table_Position = Button(C_main,text="Positions Table",command=positions_table,fg="white",bg="blue", font=("Agency FB",12))
Btn_Table_Position.place(x=500,y=550)

Btn_Test_Drive = Button(C_main,text="Test Drive",command=test_drive,fg="white",bg="blue", font=("Agency FB",12))
Btn_Test_Drive.place(x=500,y=500)

Btn_ConnectControl = Button(C_main,text='Send',command=lambda:send(None),fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=250)

Btn_Controls = Button(C_main,text='Send & Show ID',command=sendShowID,fg='white',bg='blue', font=('Agency FB',12))
Btn_Controls.place(x=500,y=250)

Btn_ConnectControl = Button(C_main,text='Leer Mensaje',command=read,fg='white',bg='blue', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=300)
main.mainloop()
