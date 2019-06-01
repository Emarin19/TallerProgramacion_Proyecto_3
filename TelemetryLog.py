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
Ejemplo de como usar el módudo NodeMCU de WifiConnection

"""
#           _____________________________________________________
#__________/ BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from tkinter import messagebox      # AskYesNo ()
from threading import Thread        # p.start()
from random import randint          #
from tkinter.ttk import Progressbar #
from tkinter import ttk             #
import random                       #
import threading                    # 
import winsound                     # Playsound
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)

from Validaciones import *
#Biblioteca para el Carro
from WiFiClient import NodeMCU

#Función para cargar imágenes
def loadImg(name):
    ruta=os.path.join("imagenes",name)
    imagen=PhotoImage(file=ruta)
    return imagen


#VARIABLES GLOBALES

#MANEJO DEL CARRO
global Forward, Back, PWM, Stoped
Forward = 400
Back = -400
PWM = 0

#LUCES
global Lfront, Lback, Lleft, Lright
Lfront = False
Lback = False
Lleft = False
Lright = False

#INTERFAZ
global F_arrow, B_arrow, L_arrow, R_arrow, Front_img, Back_img, Left_img, Right_img, Piloto, Sense, Lista, Bat
Piloto = ""
Sense = ["60;"]
Lista = ["0","1","2","3","4","5","6","7","8","9"]
Bat = False

global LB0, LB10, LB20
LB0 = ""
LB10 = ""
LB20 = ""



#           _____________________________________________________
#__________/ VENTANA PRINCIPAL

def main_window():
    #Creación ventana principal y sus atributos
    main=Tk()
    main.title("Formula E")
    main.minsize(1200, 675)
    main.resizable(width=NO, height=NO)

    #Canvas de la ventana principal
    C_main=Canvas(main, width=1200, height=675, bg="white")
    C_main.place(x=0, y=0)

    def intro():
        #Se corren los Threads del movimiento del fondo de introducción y el sonido de acelaración respectivamente 
        p=Thread(target=move_logo,args=()).start()
        p=Thread(target=song_intro,args=()).start()

        #Fondo de Introducción
        BG = loadImg("FormulaE.png")
        C_main.create_image(0, 0, image=BG, anchor=NW, state=NORMAL)
        time.sleep(2.7)
        
        #Luego de 2.7 segundos la introducción termina y se establece el fondo principal de la interfaz, la música
        #los botones, entre otros.
        C_main.create_image(0, 0, image=BG, anchor=NW, state=HIDDEN)
        
        BG2 = loadImg("MainBG.png")
        C_main.create_image(0, 0, image=BG2, anchor=NW, state=NORMAL)

        p=Thread(target=song_main,args=()).start()

        Music=loadImg("Music.png")
        Btn_song = Button(C_main, command=song_main, fg="black", bg="light blue")
        Btn_song.place(x=10, y=10)
        Btn_song.config(image=Music)

        Mute=loadImg("Mute.png")
        Btn_mute=Button(C_main, command=mute, fg="black",bg="light blue")
        Btn_mute.place(x=10, y=40)
        Btn_mute.config(image=Mute)

        Btn_About = Button(C_main, text="ABOUT", command=w_description, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_About.place(x=1145,y=6)

        Btn_PT = Button(C_main, text="Positions Table", command=positions_table, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_PT.place(x=130,y=500)

        Btn_TD = Button(C_main, text="Test Drive", command=test_drive, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_TD.place(x=1000,y=500)

        Bat = open("Car state.txt","r+")
        Bat_level = Bat.readlines()
        Estado = loadImg(Bat_level[0])
        C_main.create_text(1080, 80, font=("Agency", 16, "bold"), anchor=NW, fill="white", text="CAR STATE") 
        C_main.create_image(1110, 110, image=Estado, anchor=NW, state=NORMAL)
        
        C_main.create_text(200, 80, font=("Agency", 16, "bold"), anchor=NW, fill="white", text="ESCUDERIA")

        Logo_Escuderia = Logos = open("Team information.txt", "r+")
        Logo = Logo_Escuderia.readlines()
        Team_logo = loadImg(Logo[0][:6])
        C_main.create_image(160, 120, image=Team_logo, anchor=NW, state=NORMAL)
        
        Btn_Info = Button(C_main, text="Información", command=information, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_Info.place(x=160,y=350)

        time.sleep(1000000)

    def song_intro():
        winsound.PlaySound("Intro", winsound.SND_ASYNC)

    def song_main():
        winsound.PlaySound("Cars", winsound.SND_LOOP + winsound.SND_ASYNC)

    def mute():
        winsound.PlaySound(None, winsound.SND_ASYNC)

    def move_logo():
        BGL = loadImg("FormulaE2.png")
        Logo = C_main.create_image(-1000, 244, image=BGL, anchor=NW, state=NORMAL)
        x=-1100
        y=244
        return move_logo_aux(Logo,x,y)

    def move_logo_aux(Logo,x,y):
        try:
            while x<=0:
                if x!=-100:
                    C_main.move(Logo,20,0)
                    x=x+20
                    y=y
                    time.sleep(0.001)
                else:
                    C_main.move(Logo,0,0)
                    time.sleep(0.0001)  
        except:
            return    

    def information():
        main.withdraw()
        info=Toplevel()
        info.title("Team Information")
        info.minsize(1200,300)
        info.resizable(width=NO, height=NO)

        C_info = Canvas(info, width=1200, height=300, bg="white")
        C_info.place(x=0, y=0)
        
        Escuderia = open("Team information.txt","r+")
        Escuderia_info = Escuderia.readlines()
        Patro = Escuderia_info[0][37:]

        #Logo de la escuderia
        Logo = loadImg(Escuderia_info[0][:6])
        
        C_info.create_text(100, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Logo")
        C_info.create_image(25, 95, image=Logo, anchor=NW, state=NORMAL)
        
        C_info.create_text(300, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Nombre")
        C_info.create_text(280, 150, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Escuderia_info[0][7:22])
        
        C_info.create_text(430, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Ubicación")
        C_info.create_text(450, 150, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Escuderia_info[0][22:32])
        
        C_info.create_text(570, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="IGE")
        C_info.create_text(570, 150, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Escuderia_info[0][32:37])
        
        C_info.create_text(640, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Pilotos")
        C_info.create_text(765, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Autos")
        
        C_info.create_text(860, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Patrocinadores")

        def patrocinio(Patro,Patrocinador, x, y):
            if Patro=="":
                C_info.create_text(x, y, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Patrocinador)

            elif Patro[0]!=",":
                Patrocinador=Patrocinador+Patro[0]
                return patrocinio(Patro[1:],Patrocinador,x,y)

            else:
                C_info.create_text(x, y, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Patrocinador)
                return patrocinio(Patro[1:], "", x, y+20)

        def chance_logo():
            info.withdraw()
            logo=Toplevel()
            logo.title("Cambiar Logo")
            logo.minsize(1200,620)
            logo.resizable(width=NO, height=NO)

            C_logo = Canvas(logo, width=1200, height=620, bg="white")
            C_logo.place(x=0, y=0)

            Logos_Escuderia = Logos = open("Logos.txt", "r+")
            Logos = Logos_Escuderia.readlines()

            #Se cargan los 8 logos de la Escuderia para seleccionaer un de ellos
            Logo1 = loadImg(Logos[0][:6])
            Logo2 = loadImg(Logos[1][:6])
            Logo3 = loadImg(Logos[2][:6])
            Logo4 = loadImg(Logos[3][:6])
            Logo5 = loadImg(Logos[4][:6])
            Logo6 = loadImg(Logos[5][:6])
            Logo7 = loadImg(Logos[6][:6])
            Logo8 = loadImg(Logos[7][:6])

            C_logo.create_image(60, 60, image=Logo1, anchor=NW, state=NORMAL)
            C_logo.create_image(360, 20, image=Logo2, anchor=NW, state=NORMAL)
            C_logo.create_image(660, 20, image=Logo3, anchor=NW, state=NORMAL)
            C_logo.create_image(960, 60, image=Logo4, anchor=NW, state=NORMAL)
            C_logo.create_image(60, 340, image=Logo5, anchor=NW, state=NORMAL)
            C_logo.create_image(360, 340, image=Logo6, anchor=NW, state=NORMAL)
            C_logo.create_image(660, 340, image=Logo7, anchor=NW, state=NORMAL)
            C_logo.create_image(960, 340, image=Logo8, anchor=NW, state=NORMAL)

            Selected = IntVar()

            rad1 = Radiobutton(logo,text='Logo 1', value=1, variable=Selected)
            rad2 = Radiobutton(logo,text='Logo 2', value=2, variable=Selected)
            rad3 = Radiobutton(logo,text="Logo 3", value=3, variable=Selected)
            rad4 = Radiobutton(logo,text="Logo 4", value=4, variable=Selected)
            rad5 = Radiobutton(logo,text="Logo 5", value=5, variable=Selected)
            rad6 = Radiobutton(logo,text="Logo 6", value=6, variable=Selected)
            rad7 = Radiobutton(logo,text="Logo 7", value=7, variable=Selected)
            rad8 = Radiobutton(logo,text="Logo 8", value=8, variable=Selected)

            

            def back():
                Seleccion = Selected.get()
                print(Seleccion)
                if Seleccion == 1:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L1.png Mercedez-Benz  Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 2:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L2.png Porsche        Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 3:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L3.png Renault        Francia "+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 4:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L4.png Audi           Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()
                    
                elif Seleccion == 5:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L5.png Jaguar         UK      "+Logos[0][30:])
                    Logos_Escuderia.close()
                    print("Logo 5 Seleccionado")

                elif Seleccion == 6:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L6.png Mahindra       India   "+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 7:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L7.png BMW            Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 8:
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L8.png Nissan         Japon   "+Logos[0][30:])
                    Logos_Escuderia.close()
                    
                else:
                    print("No chance")
                    
                logo.destroy()
                information()

            Btn_back = Button(logo, text="Confirmar Cambio", command=back, bg="#cb3234", fg="white")
            Btn_back.place(x=540,y=590)

            rad1.place(x=130, y=230)
            rad2.place(x=425, y=230)
            rad3.place(x=725, y=230)
            rad4.place(x=1030, y=230)
            rad5.place(x=130, y=530)
            rad6.place(x=425, y=530)
            rad7.place(x=725, y=530)
            rad8.place(x=1030, y=530)

            main.mainloop()
            

        def patrocinadores():
            print("Hey2")
        

        def back():
            info.destroy()
            main.destroy()
            main_window()

        patrocinio(Patro,"",900, 75)
        Btn_logo = Button(info, text="Cambiar Logo", command=chance_logo, bg="light blue", fg='black')
        Btn_logo.place(x=1055,y=90)

        Btn_patrocinadores = Button(info, text="Editar Patrocinadores", command=patrocinadores, bg="light blue", fg='black')
        Btn_patrocinadores.place(x=1050,y=200)

        Btn_Pilotos = Button(info, text="Lista Pilotos", command=positions_table, bg="light blue", fg='black')
        Btn_Pilotos.place(x=640,y=150)

        Btn_Autos = Button(info, text="Lista Autos", command=positions_table, bg="light blue", fg='black')
        Btn_Autos.place(x=765,y=150)
        
        Btn_back = Button(info, text="Back", command=back, bg="light blue", fg='black')
        Btn_back.place(x=10,y=10)

        main.mainloop()
        
    p=Thread(target=intro,args=()).start()
    
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
        #Ventana de posisiones
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

#           _____________________________________________________
#__________/ DRIVING TEST WINDOW
    def test_drive():
       #Esconder ventana principal
       main.withdraw()
       #Ventana de para ek manejo del carro y sus atributos
       test=Toplevel()
       test.title("Driving Test")
       test.minsize(450, 625)
       test.resizable(width=NO, height=NO)

       #Canvas de la ventana de testeo
       C_test = Canvas(test, width=450, height=625, bg="white")
       C_test.place(x=0, y=0)

       #Fondo principal
       BG1 = loadImg("Test.png")
       C_test.create_image(0, 0, image=BG1, anchor=NW, state=NORMAL)

       #Se abre el archivo que contiene el estado actual del carro y se coloca una imagen representativa del mismo
       Bat = open("Car state.txt","r+")
       Bat_level = Bat.readlines()
       Estado = loadImg(Bat_level[0])
       C_test.create_text(320, 20, font=("Agency", 16, "bold"), anchor=NW, fill="white", text="CAR STATE")
       C_test.create_image(345, 50, image=Estado, anchor=NW, state=NORMAL)

       def select_pilot():
           #Entradas: Ninguna
           #Salida: Guarda los datos del piloto que el usuario ha seleccionado para realizar el test
           #Restricciones: Deben haber a lo sumo dos pilotos de la Temporada 2019, el usuario debe seleccionar
           #un piloto, de lo contrario no podrá realizar el test
           
           #Descripción: Función que muestra en pantalla todos los datos (Foto, nombre, nacionalidad,
           #Temporada, RGP, REP, entre otros) de los pilotos de la Temporada 2019 para que el usuario pueda
           #seleccionar uno de los dos. Una vez hecha la selección del piloto, todos los datos de este se
           #almacenaran en una variable global para ponerlos en pantalla una vez iniciado el test

           #Ventana para la selección del piloto y sus atributos
           pilot=Toplevel()
           pilot.title("Selección de piloto")
           pilot.minsize(900, 300)
           pilot.resizable(width=NO, height=NO)

           #Canvas de la ventana de selección
           C_pilot = Canvas(pilot, width=900, height=300, bg="white")
           C_pilot.place(x=0, y=0)

           #Se abre el txt con la información de todos los pilotos de Temporadas pasadas y la Temporada 2019
           Pilotos_FE = open("Tabla de posiciones Pilotos.txt","r+")
           Pilotos_2019 = Pilotos_FE.readlines()

           def buscarA(Pilotos_2019,i,PA):
               #Entradas: Lista de todos los pilotos de la Escuderia, un indice para ir buscando al Piloto A de
               #la Temporada 2019 y una variable que contiene al Piloto que se desea encontrar
               #Salida: Piloto A de la Temporada 2019 
               #Restricciones: Debe haber a lo sumo dos pilotos de la Temporada 2019

               #Descripción: Función recursiva que busca al Piloto A de la Temporada 2019 dentro de la lista de todos los
               #pilotos de la Escuderia y una vez que lo encuentra, todos su datos se almacenan en una variable con el fin
               #de ponerlos en la ventana para que el usuario pueda verlos y así selecconarlo o no para hacer el test
               
               if Pilotos_2019[i][:9]==PA:#Condición de finalización
                   return Pilotos_2019[i]

               else:
                   #Llamada recursiva
                   return buscarA(Pilotos_2019,i+1,PA)

           def buscarB(Pilotos_2019,i,PB):
               #Entradas: Lista de todos los pilotos de la Escuderia, un indice para ir buscando al Piloto B de
               #la Temporada 2019 y una variable que contiene al Piloto que se desea encontrar
               #Salida: Piloto B de la Temporada 2019 
               #Restricciones: Debe haber a lo sumo dos pilotos de la Temporada 2019

               #Descripción: Función recursiva que busca al Piloto B de la Temporada 2019 dentro de la lista de todos los
               #pilotos de la Escuderia y una vez que lo encuentra, todos su datos se almacenan en una variable con el fin
               #de ponerlos en la ventana para que el usuario pueda verlos y así selecconarlo o no para hacer el test
               
               if Pilotos_2019[i][:9]==PB:#Condición de finalización
                   return Pilotos_2019[i]

               else:
                   #Llamada recursiva
                   return buscarB(Pilotos_2019,i+1,PB)

           #Variable que contiene todos los datos del Piloto A de la Temporada 2019
           PilotoA = buscarA(Pilotos_2019,0,"2019A.png")
           #Variable que contiene todos los datos del Piloto B de la Temporada 2019
           PilotoB = buscarB(Pilotos_2019,0,"2019B.png")


           #INTERFAZ PARA LA SELECCIÓN DEL PILOTO
           
           #Se carga la imagen del Piloto A
           PilotoA_img = loadImg(PilotoA[0:9])
           C_pilot.create_image(10, 80, image=PilotoA_img, anchor=NW, state=NORMAL)

           #Se carga la imagen del Piloto B
           PilotoB_img = loadImg(PilotoB[0:9])
           C_pilot.create_image(10, 180, image=PilotoB_img, anchor=NW, state=NORMAL)

           #Variable que almacena el valor de la selección de uno de los dos pilotos
           Selected = IntVar()

           #Indicador de selección del Piloto: Si el valor de selección es 1, significa que el usuario ha
           #seleccionado al Piloto A y si el valor de selección es 2, significa que el usuario ha seleccionado
           #al Piloto B
           rad1 = Radiobutton(pilot,text="Piloto 1", value=1, variable=Selected)
           rad2 = Radiobutton(pilot,text="Piloto 2", value=2, variable=Selected)

           #Nombres de los Pilotos
           C_pilot.create_text(320, 10, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="PILOTOS TEMPORADA 2019")
           C_pilot.create_text(150, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Nombre")
           C_pilot.create_text(70, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[12:38])
           C_pilot.create_text(70, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[12:38])

           #Edad de los Pilotos
           C_pilot.create_text(280, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Edad")
           C_pilot.create_text(290, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[41:44])
           C_pilot.create_text(290, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[41:44])

           #Nacionalidad de los Pilotos
           C_pilot.create_text(350, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Nacionalidad")
           C_pilot.create_text(360, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[48:65])
           C_pilot.create_text(360, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[48:65])

           #Temporada, en este caso será la del 2019
           C_pilot.create_text(500, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Temporada")
           C_pilot.create_text(530, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[65:70])
           C_pilot.create_text(530, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[65:70])

           #Número de competiciones de ambos pilotos
           C_pilot.create_text(620, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Competencias")
           C_pilot.create_text(680, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[76:81])
           C_pilot.create_text(680, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[76:81])

           #Rendimiento global de los Pilotos
           C_pilot.create_text(790, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="RGP")
           C_pilot.create_text(795, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[93:97])
           C_pilot.create_text(795, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[93:97])

           #Rendimiento específico de los Pilotos
           C_pilot.create_text(850, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="REP")
           C_pilot.create_text(855, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[97:])
           C_pilot.create_text(855, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[97:])

           def back():
               #Entradas: Ninguna
               #Salida: Datos del Piloto seleccionado por el usuario
               #Restricciones: Se recomienda seleccionar uno de los dos Pilotos, de los contrario no se podrá realizar el test 

               #Descripción: Función que almacena en una variable todos los datos del Piloto seleccionado por el usuario
               global Piloto
               #Se obtiene el valor (1 o 2) de la selección del usuario
               Seleccion = Selected.get()
               #Si el valor de selección es 1, significa que el usuario seleccionó al Piloto A, por lo tanto se almacenarán todos
               #sus datos para ponerlos en la ventana del test
               if Seleccion == 1:
                   Piloto = PilotoA
               #Si el valor de selección es 2, significa que el usuario seleccionó al Piloto B, por lo tanto se almacenarán todos
               #sus datos para ponerlos en la ventana del test
               elif Seleccion == 2:
                   Piloto = PilotoB
               #Si el usuario no hace ninguna selección, se imprimirá el siguiente mensaje
               else:
                   print("Piloto no ha sido seleccionado")

               #Se destuye la ventana de selección del Piloto
               pilot.destroy()
               #Se retorna a la ventana de test_drive
               test.deiconify()

           #Botones de selección de los Pilotos
           rad1.place(x=130, y=130)
           rad2.place(x=130, y=230)

           #Botón para confirmar la selección del Piloto y almacenar los datos del mismo
           Btn_back = Button(pilot, text="Seleccionar", command=back, bg="#cb3234", fg="white")
           Btn_back.place(x=430, y=250)

           main.mainloop()

 
       def drive_car():
           global Piloto
           if Piloto!="":
               return drive_car_aux()

           else:
               messagebox.showwarning("Pilot selection", "No se ha seleccionado un piloto")
               
       def drive_car_aux():
           test.withdraw()
           car=Toplevel()
           car.title("Driving Test")
           car.minsize(1200, 675)
           car.resizable(width=NO, height=NO)

           C_car = Canvas(car, width=1200, height=675, bg="white")
           C_car.place(x=0, y=0)
  

           def intro():
               BG = loadImg("FE.1.png")
               Fondo_intro = C_car.create_image(0, 0, image=BG, anchor=NW, state=NORMAL)
               time.sleep(2.7)
               C_car.itemconfig(Fondo_intro, state=HIDDEN)
               
               global Car_Background1
               BG2 = loadImg("23.1E.png")
               Car_Background1 = C_car.create_image(0, 0, image=BG2, anchor=NW, state=NORMAL)

               global Car_Background2
               BG3 = loadImg("23.N.png")
               Car_Background2 = C_car.create_image(0, 0, image=BG3, anchor=NW, state=HIDDEN)

               global Piloto
               C_car.create_text(840, 5, font=("Agency", 20, "bold"), anchor=NW, fill="white", text=Piloto[12:38])
               C_car.create_text(1000, 45, font=("Agency", 20, "bold"), anchor=NW, fill="white", text=Piloto[48:65])

               Logo_Escuderia = Logos = open("Team information.txt", "r+")
               Logo = Logo_Escuderia.readlines()
               C_car.create_text(100, 250, font=("Agency", 22, "bold"), anchor=NW, fill="white", text=Logo[0][7:22])
               
               global Front_img
               Front = loadImg("F.1.png")
               Front_img = C_car.create_image(880, 200, image=Front, anchor=NW, state=HIDDEN)

               global Back_img
               Back = loadImg("B.1.png")
               Back_img = C_car.create_image(940, 200, image=Back, anchor=NW, state=HIDDEN)

               global Left_img
               Left = loadImg("D.1.png")
               Left_img = C_car.create_image(820, 200, image=Left, anchor=NW, state=HIDDEN)

               global Right_img
               Right = loadImg("D.1.png")
               Right_img = C_car.create_image(1000, 200, image=Right, anchor=NW, state=HIDDEN)

               global F_arrow
               FA = loadImg("FA.1E2.png")
               F_arrow = C_car.create_image(250, 80, image=FA, anchor=NW, state=HIDDEN)

               global B_arrow
               FB = loadImg("FB.1E2.png")
               B_arrow = C_car.create_image(250, 240, image=FB, anchor=NW, state=HIDDEN)

               global Stoped
               ST = loadImg("S.1E2.png")
               Stoped = C_car.create_image(255, 190, image=ST, anchor=NW, state=HIDDEN)

               global L_PWM_aux
               C_car.create_text(560, 400, font=("Agency", 22), anchor=NW, fill="white", text="PWM")
               L_PWM_aux = C_car.create_text(592, 462, font=("Agency", 28), anchor=NW, fill="white", text=str(PWM))

               global L_arrow
               FL = loadImg("FI.1E2.png")
               L_arrow = C_car.create_image(140, 185, image=FL, anchor=NW, state=HIDDEN)

               global R_arrow
               FR = loadImg("FD.1E2.png")
               R_arrow = C_car.create_image(310, 185, image=FR, anchor=NW, state=HIDDEN)

               #NIVEL DE BATERIA
               global Battery
               Battery = C_car.create_text(1108, 255, font=("Agency", 14), anchor=NW, fill="white", text="")

               Btn_back = Button(car, text="TERMINAR TEST", command=back, bg="#cb3234", fg="white")
               Btn_back.place(x=10, y=10)

               time.sleep(100000)

           #Creando el cliente para NodeMCU
           myCar = NodeMCU()
           myCar.start()

           def get_log():
               global Sense, Lista, Bat
               #Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
               indice = 0
               while(myCar.loop):
                   while(indice < len(myCar.log)):
                       mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
                       try:
                           mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
                           Sense = mnsRecv
                           if len(Sense)>=27:
                               Bat = True
                               sense_aux(Sense)
                       except:
                           pass

                       indice+=1
                   time.sleep(0.200)
                   
           def sense():
               mns = "sense;"
               myCar.send(mns)
               time.sleep(2)
               return sense()

           def sense_aux(Sense):
               global Car_Background1, Car_Background2
               if buscar(Sense)== "1":
                   C_car.itemconfig(Car_Background1, state=NORMAL)
                   C_car.itemconfig(Car_Background2, state=HIDDEN)
                   drive_car.update()
                   
               elif buscar(Sense) == "0":
                   C_car.itemconfig(Car_Background1, state=HIDDEN)
                   C_car.itemconfig(Car_Background2, state=NORMAL)
                   drive_car.update()

               else:
                   pass

           def buscar(Sense):
               if Sense[-1] == "1":
                   return "1"

               elif Sense[-1] == "0":
                   return "0"

               else:
                   return buscar(Sense[:-1])

           def battery():
               global Bat, Sense, Lista, L20, L30, L40
               if Bat == True:
                   Car_state = open("Car state.txt","r+")
                   Car_state.seek(0)
                   Battery_Levels = open("Battery_Levels.txt", "r+")
                   BL = Battery_Levels.readlines()
                   try:
                       L_Bat = level_bat(Sense[3:], Lista, "")
                       if L_Bat == "0":
                           B0 = loadImg(BL[0][:6])
                           C_car.create_image(1105, 185, image=B0, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("0% de bateria")
                           Car_state.write("Descargado")
                           Car_state.close()
                           
                       elif L_Bat == "10":
                           B10 = loadImg(BL[1][:7])
                           C_car.create_image(1105, 185, image=B10, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("10% de bateria")
                           Car_state.write("Descargado")
                           Car_state.close()

                       elif L_Bat == "20":
                           B20 = loadImg(BL[2][:7])
                           C_car.create_image(1105, 185, image=B20, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("20% de bateria")
                           Car_state.write("Descargado")
                           Car_state.close()

                       elif L_Bat == "30":
                           B30 = loadImg(BL[3][:7])
                           C_car.create_image(1105, 185, image=B30, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("30% de bateria")
                           Car_state.write("Descargado")
                           Car_state.close()

                       elif L_Bat == "40":
                           B40 = loadImg(BL[4][:7])
                           C_car.create_image(1105, 185, image=B40, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("40% de bateria")
                           Car_state.write("Descargado")
                           Car_state.close()

                       elif L_Bat == "50":
                           B50 = loadImg(BL[5][:7])
                           C_car.create_image(1105, 185, image=B50, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("50% de bateria")
                           Car_state.write("Descargado")
                           Car_state.close()

                       elif L_Bat == "60":
                           B60 = loadImg(BL[6][:7])
                           C_car.create_image(1105, 185, image=B60, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("60% de bateria")
                           Car_state.write("Disponible")
                           Car_state.close()

                       elif L_Bat == "70":
                           B70 = loadImg(BL[7][:7])
                           C_car.create_image(1105, 185, image=B70, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("70% de bateria")
                           Car_state.write("Disponible")
                           Car_state.close()

                       elif L_Bat == "80":
                           B80 = loadImg(BL[8][:7])
                           C_car.create_image(1105, 185, image=B80, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("80% de bateria")
                           Car_state.write("Disponible")
                           Car_state.close()

                       elif L_Bat == "90":
                           B90 = loadImg(BL[9][:7])
                           C_car.create_image(1105, 185, image=B90, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("90% de bateria")
                           Car_state.write("Disponible")
                           Car_state.close()

                       elif L_Bat == "100":
                           B100 = loadImg(BL[10][:8])
                           C_car.create_image(1105, 185, image=B100, anchor=NW, state=NORMAL)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           print("100% de bateria")
                           Car_state.write("Disponible")
                           Car_state.close()
                           
                       else:
                           pass
                   except:
                       pass
               else:
                   pass

               Bat = False
               time.sleep(2.0)
               return battery()

           def level_bat(Sense, Lista, L_Bat):
               if Sense[0]==";":
                   return L_Bat

               elif buscar_level(Sense[0],Lista)==True:
                   L_Bat = L_Bat + Sense[0]
                   return level_bat(Sense[1:], Lista, L_Bat)

               else:
                   return level_bat(Sense[1:], Lista, L_Bat)

           def buscar_level(Ele, Lista):
               if Lista == []:
                   return False

               elif Ele == Lista[0]:
                   return True

               else:
                   return buscar_level(Ele, Lista[1:])
                            
           def lights(event):
               global Lfront, Lback, Lleft, Lright, Front_img, Back_img, Left_img, Right_img
               if event.char == "f":
                   if Lfront == False:
                       C_car.itemconfig(Front_img, state=NORMAL)
                       mns="lf:1;"
                       myCar.send(mns)
                       Lfront = True
                   else:
                       C_car.itemconfig(Front_img, state=HIDDEN)
                       mns="lf:0;"
                       myCar.send(mns)
                       Lfront = False
                    
               if event.char == "b":
                   if Lback == False:
                       C_car.itemconfig(Back_img, state=NORMAL)
                       mns = "lb:1;"
                       myCar.send(mns)
                       Lback = True
                   else:
                       C_car.itemconfig(Back_img, state=HIDDEN)
                       mns = "lb:0;"
                       myCar.send(mns)
                       Lback = False

               if event.char == "l":
                   if Lleft == False:
                       C_car.itemconfig(Left_img, state=NORMAL)
                       mns = "ll:1;"
                       myCar.send(mns)
                       Lleft = True
                   else:
                       C_car.itemconfig(Left_img, state=HIDDEN)
                       mns = "ll:0;"
                       myCar.send(mns)
                       Lleft = False

               if event.char == "r":
                   if Lright == False:
                       C_car.itemconfig(Right_img, state=NORMAL)
                       mns = "lr:1;"
                       myCar.send(mns)
                       Lright = True
                   else:
                       C_car.itemconfig(Right_img, state=HIDDEN)
                       mns = "lr:0;"
                       myCar.send(mns)
                       Lright = False  
               
           def move_forward(event):
               global Forward, Back, L_PWM_aux, F_arrow, B_arrow, Stoped
               Back = -700
               C_car.itemconfig(Stoped, state=HIDDEN)
               C_car.itemconfig(F_arrow, state=NORMAL)
               C_car.itemconfig(B_arrow, state=HIDDEN)
               if Forward <1023:
                   Forward+=1
                   mns = "pwm:" + str(Forward) + ";"
                   print(mns)
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Forward))
                   time.sleep(0.01)
               else:
                   Forward = 1023
                   mns = "pwm:" + str(Forward) + ";"
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Forward))
                   time.sleep(0.01)

           def move_back(event):
               global Forward, Back, L_PWM_aux, F_arrow, B_arrow, Stoped
               Forward = 700
               C_car.itemconfig(Stoped, state=HIDDEN)
               C_car.itemconfig(F_arrow, state=HIDDEN)
               C_car.itemconfig(B_arrow, state=NORMAL)
               if Back>-1023:
                   Back-=1
                   mns = "pwm:" + str(Back) + ";"
                   print(mns)
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Back))
                   time.sleep(0.01)
               else:
                   Back = -1023
                   mns = "pwm:" + str(Back) + ";"
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Back))
                   time.sleep(0.01)

           def stop(event):
               global Forward, Back, L_PWM_aux, F_arrow, B_arrow, L_arrow, R_arrow, Stoped
               Forward = 700
               Back = -700
               Velocidad = 0
               C_car.itemconfig(Stoped, state=NORMAL)
               C_car.itemconfig(F_arrow, state=HIDDEN)
               C_car.itemconfig(B_arrow, state=HIDDEN)
               C_car.itemconfig(R_arrow, state=HIDDEN)
               C_car.itemconfig(L_arrow, state=HIDDEN)
               mns = "pwm:" + str(Velocidad) + ";"
               myCar.send(mns)
               C_car.itemconfig(L_PWM_aux, text=str(Velocidad))

           def move_left(event):
               global L_arrow, R_arrow
               C_car.itemconfig(R_arrow, state=HIDDEN)
               C_car.itemconfig(L_arrow, state=NORMAL)
               p=Thread(target=move_left_aux,args=()).start()
               mns = "dir:-1;"
               myCar.send(mns)

           def move_left_aux():
               mns1 = "ll:1;"
               mns2 = "ll:0;"
               myCar.send(mns1)
               time.sleep(0.5)
               myCar.send(mns2)
               time.sleep(0.5)
               myCar.send(mns1)
               time.sleep(0.5)
               myCar.send(mns2)
               time.sleep(0.5)
               myCar.send(mns1)
               time.sleep(0.5)
               myCar.send(mns2)
	        
           def move_right(event):
               global L_arror, R_arrow
               C_car.itemconfig(R_arrow, state=NORMAL)
               C_car.itemconfig(L_arrow, state=HIDDEN)
               p=Thread(target=move_right_aux,args=()).start()
               mns = "dir:1;"
               myCar.send(mns)

           def move_right_aux():
               mns1 = "lr:1;"
               mns2 = "lr:0;"
               myCar.send(mns1)
               time.sleep(0.5)
               myCar.send(mns2)
               time.sleep(0.5)
               myCar.send(mns1)
               time.sleep(0.5)
               myCar.send(mns2)
               time.sleep(0.5)
               myCar.send(mns1)
               time.sleep(0.5)
               myCar.send(mns2)

           def move_direct(event):
               C_car.itemconfig(R_arrow, state=HIDDEN)
               C_car.itemconfig(L_arrow, state=HIDDEN)
               mns = "dir:0;"
               myCar.send(mns)

           def send (event):
               mns = str(E_Command.get())
               if(len(mns)>0 and mns[-1] == ";"):
                   E_Command.delete(0, 'end')
                   myCar.send(mns)
               else:
                   messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

           def back():
               global Piloto
               Piloto = ""
               car.destroy()
               test.deiconify()


           car.bind("<Up>", move_forward)
           car.bind("<Down>", move_back)
           car.bind("p", stop)
           car.bind("<Left>", move_left)
           car.bind("<Right>", move_right)
           car.bind("d", move_direct)
           car.bind("<Key>",lights)


           p=Thread(target=intro,args=()).start()
           p = Thread(target=get_log).start()
           p = Thread(target=sense).start()
           p = Thread(target=battery).start()
           main.mainloop()

       def back():
           test.destroy()
           main.destroy()
           main_window()

       Btn_back = Button(test, text="ATRAS", command=back, bg="#cb3234", fg="white")
       Btn_back.place(x=10,y=595)

       Btn_pilot = Button(test, text="Seleccionar Piloto", command=select_pilot, bg="#cb3234", fg="white")
       Btn_pilot.place(x=50,y=50)

       Start=loadImg("S1.1.png")
       Btn_start = Button(C_test,command=drive_car, fg="black", bg="light blue")
       Btn_start.place(x=380,y=555)
       Btn_start.config(image=Start)
       
       main.mainloop()    

    print("Working")
    main.mainloop()

main_window()
