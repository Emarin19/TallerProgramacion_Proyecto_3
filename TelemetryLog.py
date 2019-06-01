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
Forward = 700
Back = -700
PWM = 0

#LUCES
global Lfront, Lback, Lleft, Lright
Lfront = False
Lback = False
Lleft = False
Lright = False

#INTERFAZ
global F_arrow, B_arrow, L_arrow, R_arrow, Front_img, Back_img, Left_img, Right_img, Piloto
Piloto = ""



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

        Bat = open("Battery_level.txt","r+")
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
        print("Hey")
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
       test.minsize(450, 625)
       test.resizable(width=NO, height=NO)

       C_test = Canvas(test, width=450, height=625, bg="white")
       C_test.place(x=0, y=0)

       BG1 = loadImg("T.2.png")
       C_test.create_image(0, 0, image=BG1, anchor=NW, state=NORMAL)

       Bat = open("Battery_level.txt","r+")
       Bat_level = Bat.readlines()
       Estado = loadImg(Bat_level[0])
       C_test.create_text(320, 20, font=("Agency", 16, "bold"), anchor=NW, fill="white", text="CAR STATE")
       C_test.create_image(345, 50, image=Estado, anchor=NW, state=NORMAL)

       def select_pilot():
           pilot=Toplevel()
           pilot.title("Selección de piloto")
           pilot.minsize(900, 300)
           pilot.resizable(width=NO, height=NO)

           C_pilot = Canvas(pilot, width=900, height=300, bg="white")
           C_pilot.place(x=0, y=0)
           
           Pilotos_FE = open("Tabla de posiciones Pilotos.txt","r+")
           Pilotos_2019 = Pilotos_FE.readlines()

           def buscarA(Pilotos_2019,i,PA):
               if Pilotos_2019[i][:9]==PA:
                   return Pilotos_2019[i]

               else:
                   return buscarA(Pilotos_2019,i+1,PA)

           def buscarB(Pilotos_2019,i,PB):
               if Pilotos_2019[i][:9]==PB:
                   return Pilotos_2019[i]

               else:
                   return buscarB(Pilotos_2019,i+1,PB)

           PilotoA = buscarA(Pilotos_2019,0,"2019A.png")
           PilotoB = buscarB(Pilotos_2019,0,"2019B.png")
           
           PilotoA_img = loadImg(PilotoA[0:9])
           C_pilot.create_image(10, 80, image=PilotoA_img, anchor=NW, state=NORMAL)

           PilotoB_img = loadImg(PilotoB[0:9])
           C_pilot.create_image(10, 180, image=PilotoB_img, anchor=NW, state=NORMAL)

           Selected = IntVar()

           rad1 = Radiobutton(pilot,text="Piloto 1", value=1, variable=Selected)
           rad2 = Radiobutton(pilot,text="Piloto 2", value=2, variable=Selected)

           C_pilot.create_text(320, 10, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="PILOTOS TEMPORADA 2019")
           C_pilot.create_text(150, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Nombre")
           C_pilot.create_text(70, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[12:38])
           C_pilot.create_text(70, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[12:38])
           
           C_pilot.create_text(280, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Edad")
           C_pilot.create_text(290, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[41:44])
           C_pilot.create_text(290, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[41:44])

           C_pilot.create_text(350, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Nacionalidad")
           C_pilot.create_text(360, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[48:65])
           C_pilot.create_text(360, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[48:65])
           
           C_pilot.create_text(500, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Temporada")
           C_pilot.create_text(530, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[65:70])
           C_pilot.create_text(530, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[65:70])
           
           C_pilot.create_text(620, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Competencias")
           C_pilot.create_text(680, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[76:81])
           C_pilot.create_text(680, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[76:81])

           C_pilot.create_text(790, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="RGP")
           C_pilot.create_text(795, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[93:97])
           C_pilot.create_text(795, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[93:97])
           
           C_pilot.create_text(850, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="REP")
           C_pilot.create_text(855, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[97:])
           C_pilot.create_text(855, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[97:])


           def back():
               global Piloto
               Seleccion = Selected.get()
               print(Seleccion)
               if Seleccion == 1:
                   Piloto = PilotoA
               elif Seleccion == 2:
                   Piloto = PilotoB
               else:
                   print("Piloto no ha sido seleccionado")

               pilot.destroy()
               test.deiconify()

           rad1.place(x=130, y=130)
           rad2.place(x=130, y=230)
           
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
           #global Sense12
           test.withdraw()
           car=Toplevel()
           car.title("Driving Test")
           car.minsize(1200, 675)
           car.resizable(width=NO, height=NO)

           C_car = Canvas(car, width=1200, height=675, bg="white")
           C_car.place(x=0, y=0)

           """global Piloto
           L_Name = Label(C_car, text=Piloto[12:38], font=("Agency",20), bg="#2cb1a9", fg="white")
           L_Name.place(x=860, y=5)

           L_Nacionality = Label(C_car, text=Piloto[48:65], font=("Agency",22), bg="#2cb1a9", fg="white")
           L_Nacionality.place(x=1000, y=45)

           Logo_Escuderia = Logos = open("Team information.txt", "r+")
           Logo = Logo_Escuderia.readlines()
           L_Escuderia = Label(C_car, text=Logo[0][7:22], font=("Agency",16), bg="#2cb1a9", fg="white")
           L_Escuderia.place(x=10, y=250)"""
           
           
           

    
           """global B0_level
           B0 = loadImg("B50.png")
           B0_level = Label(C_car)
           B0_level.place(x=-1105, y=185)
           B0_level.config(image=B0)
           B0_level.lift()

           global B10_level
           B10 = loadImg("B10.png")
           B10_level = Label(C_car)
           B10_level.place(x=-1105, y=185)
           B10_level.config(image=B10)
           B10_level.lift()

           global B20_level
           B20 = loadImg("B20.png")
           B20_level = Label(C_car)
           B20_level.place(x=-1105, y=185)
           B20_level.config(image=B20)
           B20_level.lift()"""
           
           #L_PWM = Label(C_car, text="PWM", font=("Agency",22), bg="#2cb1a9", fg="white")
           #L_PWM.place(x=560, y=400)

           #global L_PWM_aux
           #L_PWM_aux = Label(C_car, text=str(PWM), font=("Agency",18), bg="#2cb1a9", fg="white")
           #L_PWM_aux.place(x=592, y=462)


           def intro():
               BG = loadImg("FE.1.png")
               C_car.create_image(0, 0, image=BG, anchor=NW, state=NORMAL)
               time.sleep(2.7)
               C_car.create_image(0, 0, image=BG, anchor=NW, state=HIDDEN)
               

               global Car_Background1
               BG2 = loadImg("23.1E.png")
               Car_Background1 = C_car.create_image(0, 0, image=BG2, anchor=NW, state=NORMAL)

               global Car_Background2
               BG3 = loadImg("23.N.png")
               Car_Background2 = C_car.create_image(-2000, 0, image=BG3, anchor=NW, state=HIDDEN)

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

               Btn_back = Button(car, text="TERMINAR TEST", command=back, bg="#cb3234", fg="white")
               Btn_back.place(x=0, y=0)

               time.sleep(100000)

           #Creando el cliente para NodeMCU
           myCar = NodeMCU()
           myCar.start()

           def get_log():
               global Sense12
               #Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
               indice = 0
               while(myCar.loop):
                   while(indice < len(myCar.log)):
                       mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
                       try:
                           mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
                           Sense12 = mnsRecv
                           
                           if len(Sense12)>=27:
                               sense_aux(Sense12)
                               battery(Sense12),sense_aux(Sense12)
                               
                       except:
                           pass

                       indice+=1
                   time.sleep(0.200)
                   
           def sense():
               mns = "sense;"
               myCar.send(mns)
               time.sleep(2)
               return sense()

           def sense_aux(Sense12):
               print("Hey")
               global Car_Backgroud1, Car_Background2
               if Sense12[-4]=="1":
                   Car_Background2.place(x=-2000, y=0)
                   Car_Background1.place(x=0, y=0)
                   drive_car.update()
               elif Sense12[-4]=="0":
                   Car_Background1.place(x=-2000, y=0)
                   Car_Background2.place(x=0, y=0)
                   drive_car.update()
                   
           def battery(Sense12):
               global B0_level, B10_level, B20_level
               print("HOLA")
               print(Sense12[18])
               Bat = open("Battery_level.txt","r+")
               Bat.seek(0)
               
               if Sense12[17] or Sense12[18] or Sense12[19] == "0":
                   B0_level.place(x=105, y=185)
                   B10_level.place(x=-1105, y=185)
                   B20_level.place(x=-1105, y=185)
                   Bat.write("Descargado")
                   Bat.close()
                   drive_car.update()

               if Sense12[17] or Sense12[18] or Sense12[19] == "1":
                   B0_level.place(x=-1105, y=185)
                   B10_level.place(x=205, y=185)
                   B20_level.place(x=-1105, y=185)
                   Bat.write("Descargado")
                   Bat.close()
                   drive_car.update()

               if Sense12[17] or Sense12[18] or Sense12[19] == "2":

                   B0_level.place(x=-1105, y=185)
                   B10_level.place(x=-1105, y=185)
                   B20_level.place(x=305, y=185)
                   Bat.write("Descargado")
                   Bat.close()
                   drive_car.update()
                   
                   
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
