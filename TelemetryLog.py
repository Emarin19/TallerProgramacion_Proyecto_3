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
from tkinter import ttk             # Pestañas, radiobuttons
import threading                    # Threads
import winsound                     # Playsound
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)

#Módulo de limitación para el txt de pilotos y autos
from Validaciones import *
#Biblioteca para el Carro
from WiFiClient import NodeMCU

#Función para cargar imágenes
def loadImg(name):
    ruta=os.path.join("imagenes", name)
    imagen=PhotoImage(file=ruta)
    return imagen


#VARIABLES GLOBALES

#MANEJO DEL CARRO
global Forward, Back
Forward = 700
Back = -700

#LUCES
global Lfront, Lback, Lleft, Lright
Lfront = False
Lback = False
Lleft = False
Lright = False

#INTERFAZ
global F_arrow, B_arrow, L_arrow, R_arrow, Front_img, Back_img, Left_img, Right_img, Piloto, Sense, Lista, Bat
Piloto = ""
Lista = ["0","1","2","3","4","5","6","7","8","9"]
Bat = False

#           _____________________________________________________
#__________/ VENTANA PRINCIPAL
def main_window():
    """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: main_window()
Descripción: Ventana que contiene a las demas ventanas con sus respectivas subventanas.

Entrada: Ninguna
Salida: Acceso a la ventana de información de la Escuderia, a la tabla de posiciones de autos y pilotos, a la ventana
Test Drive y la ventana de About, ver el Estado del carro, reproducir y silenciar la canción de fondo.
Restricciones: No presenta"""
    #Creación ventana principal y sus atributos
    main=Tk()
    main.title("Formula E")#Título de la ventana
    main.minsize(1200, 675)#Tamaño mímimo de la ventana
    main.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

    #Canvas de la ventana principal
    C_main=Canvas(main, width=1200, height=675, bg="white")
    C_main.place(x=0, y=0)

    def intro():
        """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: intro()
Descripción: Función que realiza la animación de la interfaz la cual tiene una duración de 2.7 segundos, una vez terminada
#la animación se muestran en pantalla el fondo principal, se corre la música de fondo, se muestra los botones para los
#accesos a las demás ventanas y se muestra el estado actual del carro.

Entrada: Ninguna
Salida: Animación inicial de la interfaz, luego de que concluya la animación, se muestra el fondo de la ventana principal,
acceso a las demás ventanas
Restricciones: No presenta"""
        #Se corren los Threads del movimiento del fondo de animación y el sonido de acelaración respectivamente 
        p=Thread(target=move_logo,args=()).start()
        p=Thread(target=song_intro,args=()).start()

        #Fondo de animación incial
        BG = loadImg("FormulaE.png")
        C_main.create_image(0, 0, image=BG, anchor=NW, state=NORMAL)
        
        #Tiempo de duración de la animación inicial de 2.7 segundos con el fin de llamar la atención del usuario por
        #la interfaz
        time.sleep(2.7)
        
        #Luego de los 2.7 segundos, la animación termina y se establece el fondo principal de la interfaz, la música
        #los botones para el acceso a las demás ventana, entre otros.
        C_main.create_image(0, 0, image=BG, anchor=NW, state=HIDDEN)

        #Fonde de la ventana principal
        BG2 = loadImg("MainBG.png")
        C_main.create_image(0, 0, image=BG2, anchor=NW, state=NORMAL)

        #Se corre el Thread para la música de Fondo de la interfaz, se configura para que se reproduzca infinitamente
        #hasta que el usario decida silenciarla o volcerla a reproducir desde el inicio.
        p=Thread(target=song_main,args=()).start()

        #Botón para reproducir la canción de Fondo
        Music=loadImg("Music.png")
        Btn_song = Button(C_main, command=song_main, fg="black", bg="light blue")
        Btn_song.place(x=10, y=10)
        Btn_song.config(image=Music)

        #Botón para silenciar la canción de Fondo
        Mute=loadImg("Mute.png")
        Btn_mute=Button(C_main, command=mute, fg="black",bg="light blue")
        Btn_mute.place(x=10, y=40)
        Btn_mute.config(image=Mute)

        #Botón para acceder a la ventana de About
        Btn_About = Button(C_main, text="ABOUT", command=w_description, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_About.place(x=1145,y=6)

        #Botón para acceder a la tabla de posiciones de los pilotos y los autos de la Escudería
        Btn_PT = Button(C_main, text="Positions Table", command=positions_table, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_PT.place(x=130,y=500)

        #Botón para acceder a la ventana previa a realizar el Test Drive
        Btn_TD = Button(C_main, text="Test Drive", command=test_drive, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_TD.place(x=1000,y=500)

        #Desde un txt se lee el estado del carro desde la última vez que se utilizó para realizar el Test Drive; si el estado del
        #carro es "Disponible" se pondrá una imagen que represente que el estado está cargado, si el txt dice "Descargado", se pondrá
        #una imagen que represente que en efecto el carro está descargado. Esto es muy importante porque más adelante si el usuario
        #desea realizar el Test Drive, el estado previo del carro será fundamental para habilitar o no realizarlo
        Bat = open("Car state.txt","r+")
        Bat_level = Bat.readlines()
        Estado = loadImg(Bat_level[0])
        C_main.create_text(1080, 80, font=("Agency", 16, "bold"), anchor=NW, fill="white", text="CAR STATE") 
        C_main.create_image(1110, 110, image=Estado, anchor=NW, state=NORMAL)

        C_main.create_text(200, 80, font=("Agency", 16, "bold"), anchor=NW, fill="white", text="ESCUDERIA")

        #Se carga el logo de la Escudería que el usuario cambió o no, la última vez que usó la interfaz
        Logo_Escuderia = Logos = open("Team information.txt", "r+")
        Logo = Logo_Escuderia.readlines()
        Team_logo = loadImg(Logo[0][:6])
        C_main.create_image(160, 120, image=Team_logo, anchor=NW, state=NORMAL)

        #Bóton para la ventana de Información de la Escudería, aquí el usuario puede ver tanto la información de la Escudería
        #como cambiar el logo y agregar o quitar los patrocinadores de la misma
        Btn_Info = Button(C_main, text="Información", command=information, bg="#cb3234", fg="white", font=("Agency FB",16))
        Btn_Info.place(x=160,y=350)

        #Se establece un amplio tiempo para que el usuario pueda usar la interfaz
        time.sleep(1000000)

    def song_intro():
        #Descripción: Función que corre durante el tiempo establecido para la animación incial de la interfaz (2.7 segundos).
        #Consiste en el sonido de un carro de carreras acelerando
        
        #Entrada: Ninguna
        #Salida: Sonido de aceleración
        #Restrición: El sonido debe estar formato .WAV
        winsound.PlaySound("Intro", winsound.SND_ASYNC)

    def song_main():
        #Descripción: Función que corre indefinidamente una canción de Fondo para la interfaz de Formula E, una vez que ha
        #concluido la animación inicial

        #Entrada: Ninguna
        #Salida: Canción de Fondo para la interfaz
        #Restrición: La canción debe estar en formato .WAV
        winsound.PlaySound("Cars", winsound.SND_LOOP + winsound.SND_ASYNC)

    def mute():
        #Descripción: Función que detiene (silencia) la canción de Fondo de la interfaz

        #Entrada: Ninguna
        #Salida: Detiene y reinicia la canción de Fondo de la interfaz
        #Restrición: La canción debe estar en formato .WAV
        winsound.PlaySound(None, winsound.SND_ASYNC)

    def move_logo():
        #Descripción: Función principal para mover el logo de Formula E en el tiempo establecido de la animación incial, desde
        #aquí se carga el fondo del logo y se configura las posiciones iniciales para que desde una función auxiliar empiece a
        #moverse

        #Entrada: Ninguna
        #Salida: Llamada a la función auxiliar para mover el logo previamente cargado
        #Restrición: Ninguna
        BGL = loadImg("FormulaE2.png")#Logo Fórmula E
        Logo = C_main.create_image(-1000, 244, image=BGL, anchor=NW, state=NORMAL)
        #Posiciones iniciales del logo
        x=-1100
        y=244
        #Llamada a la función auxiliar
        return move_logo_aux(Logo,x,y)

    def move_logo_aux(Logo,x,y):
        #Descripción: Función auxiliar encargado de mover el logo de Formula E mediante un estatuto while, se podría realizar
        #recursivamente pero se podría presentar el incoveniente de que la pila del sistema se llene

        #Entrada: Logo y posicones inciales del mismo
        #Salida: Movimiento del Logo para el efecto de animación inicial de la interfaz
        #Restrición: Ninguna
        
        #Se capta cualquier excepción que se pueda generar considerando que al establecerce un tiempo de 2.7 segundos para la
        #animación, se pueda o no interrumpir el Thread, afectando el ejecucuón del programa
        try:
            #Condición de finalización
            while x<=0:
                #Mientras el logo no se encuentre en la posición establecida se irá movimiendo en el eje x
                if x!=-100:
                    C_main.move(Logo,20,0)
                    x=x+20
                    y=y
                    time.sleep(0.001)
                #Una vez que el logo llega a la posición establecida, este se mantendrá en el mismo punto del eje x
                #hasta que se cumpla el tiempo de 2.7 segundos
                else:
                    C_main.move(Logo,0,0)
                    time.sleep(0.0001)  
        except:
            return    

    def information():
        """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: information()
Descripción: Ventana que contiene toda la información de la Escudería (nombre, ubicación, índice ganador, patrocinadores y
acceso a la lista de pilotos y autos de la misma), tambien permite cambiar el logo y su vez la información general de la
#Escudería y también permite editar (agregar o quitar) los patrocinadores.

Entrada: Ninguna
Salida: Acceso a la ventana de las posiciones de los pilotos y autos, información de la Escudería y poder editar tanto el
logo como los patrocinadores de la misma.
Restricciones: No escribir tantos patrocinadores, ni tampoco quitarlos todos."""
        #Se esconde la ventana principal
        main.withdraw()
        #Se crea la ventana de información con sus respectivos atributos
        info=Toplevel() 
        info.title("Team Information")#Título de la ventana
        info.minsize(1200,300)#Tamaño de la ventana
        info.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

        #Canvas de la ventana de información de la Escudería
        C_info = Canvas(info, width=1200, height=300, bg="white")
        C_info.place(x=0, y=0)

        #Background = loadImg("
        #C_info.create_image(25, 95, image=Logo, anchor=NW, state=NORMAL)

        #Se abre el txt que contiene toda la información de la Escudería y se le asigana a una variable (patro)
        #todos los patrocinadores actuales de la Escudería para ponerlos en la ventana
        Escuderia = open("Team information.txt","r+")
        Escuderia_info = Escuderia.readlines()
        Patro = Escuderia_info[0][37:]

        #Logo de la escuderia
        Logo = loadImg(Escuderia_info[0][:6])
        C_info.create_text(100, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Logo")
        C_info.create_image(25, 95, image=Logo, anchor=NW, state=NORMAL)

        #Nombre de la Escudería 
        C_info.create_text(300, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Nombre")
        C_info.create_text(300, 150, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Escuderia_info[0][7:22])

        #Ubicación de la Escudería
        C_info.create_text(430, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Ubicación")
        C_info.create_text(450, 150, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Escuderia_info[0][22:32])

        #Índice ganador de la Escudería
        C_info.create_text(570, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="IGE")
        C_info.create_text(570, 150, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Escuderia_info[0][32:37])

        #Pilotos y autos de la Escudería 
        C_info.create_text(640, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Pilotos y Autos")

        #Patrocinadores de la Escudería
        C_info.create_text(860, 50, font=("Agency", 18, "bold"), anchor=NW, fill="#009186", text="Patrocinadores")

        def patrocinio(Patro,Patrocinador, x, y):
            #Descripción: Función que lee cada uno de los patrocinadores actuales de la Escudería y los coloca verticalmente
            #en la ventana de información de la Escudería

            #Entradas: Patrocinadores actuales de la Escudería, variable para almacenar cada Patrocinador (se establece que
            #cada patrocinador está diferenciado por una coma), coordenadas para ir colocando cada patrocinador verticalmente
            #sobre la ventana
            #Salida: Despliegue vertical de todos los patrocinadores actuales de la Escudería
            #Restricciones: Debe haber al menos un patrocinador

            #Condición de finalización, es cuando ya se han leido y puesto en la ventana todos los patrocinadores de la Escudería
            if Patro=="":
                C_info.create_text(x, y, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Patrocinador)

            #Diferenciador entre un patrocinador y otro de la Escuderia, mientras no se encuentre, se irá almacenado poco a poco
            #en la variable Patrocinador
            elif Patro[0]!=",":
                Patrocinador=Patrocinador+Patro[0]
                return patrocinio(Patro[1:],Patrocinador,x,y)
            
            #Cuando se encuentra el diferenciador entre un patrocinador y otro sabe que la variable Patrocinador ya ha almacenado
            #a equis patrocinador y es por esto que inmediantamente lo coloca en la ventana para almacenar al siguiente patrocinador
            #y asi sucesivamente
            else:
                C_info.create_text(x, y, font=("Agency", 12, "bold"), anchor=NW, fill="black", text=Patrocinador)
                return patrocinio(Patro[1:], "", x, y+20)

        def chance_logo():
            """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: chance_logo()
Descripción: Ventana en la cual el usuario puede cambiar el logo de la Escuderia, y con ello la información (nombre y
#ubicación de la misma, tener acceso a la ventana de los pilotos y los autos y editar (quitar o agregar) los patrocinadores.

Entrada: Ninguna
Salida: Modificación del logo y la información, siempre que el usuario lo cambie, acceso a la ventana de posiciones de
#pilotos y autos, y edición de los patrocinadores de la Escudería.
Restricciones: El usuario no puede quitar todos los patrocinadores de la Escudería"""
            #Se esconde la ventana de información de la Escudería
            info.withdraw()
            #Se crea una ventana para mostrar en pantalla ocho logos para que el usuario pueda seleccionar o no uno de ellos
            logo=Toplevel()
            logo.title("Cambiar Logo")#Título de la ventana
            logo.minsize(1200,620)#Tamaño mímimo de la ventana
            logo.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

            #Canvas de la ventana de selección del logo
            C_logo = Canvas(logo, width=1200, height=620, bg="white")
            C_logo.place(x=0, y=0)

            #Se cargan desde un txt todas las imágenes de los ocho pricipales logos que compiten en Formula E para que el
            #usuario tenga la opciónn de seleccionar uno de ellos.
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

            #Variable para que en conjunto con el método radio button pueda captar la selección del usuario
            Selected = IntVar()

            #Radio buttons asociados a cada uno de los logos
            rad1 = Radiobutton(logo,text='Logo 1', value=1, variable=Selected)
            rad2 = Radiobutton(logo,text='Logo 2', value=2, variable=Selected)
            rad3 = Radiobutton(logo,text="Logo 3", value=3, variable=Selected)
            rad4 = Radiobutton(logo,text="Logo 4", value=4, variable=Selected)
            rad5 = Radiobutton(logo,text="Logo 5", value=5, variable=Selected)
            rad6 = Radiobutton(logo,text="Logo 6", value=6, variable=Selected)
            rad7 = Radiobutton(logo,text="Logo 7", value=7, variable=Selected)
            rad8 = Radiobutton(logo,text="Logo 8", value=8, variable=Selected)

            def back():
                #Descripción: Función que una vez que el usuario ha seleccionado o no un nuevo logo, actuliza inmediatamente
                #el logo seleccionado en la ventana y su respectiva información

                #Entrada: Ninguna
                #Salida: Actualización inmediata del nuevo logo seleccionado por el usuario
                #Restriccione El usuario puede o no seleccionar un nuevo logo para la Escudería

                #Se obtiene un valor específico asociado a la selección del logo seleccionado
                Seleccion = Selected.get()
                print(Seleccion)
                
                if Seleccion == 1:
                    #Si el valor de la selección es 1, significa que el usuario ha seleccionado el logo de Mercedez-Benz
                    #y con ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L1.png Mercedez-Benz  Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 2:
                    #Si el valor de la selección es 2, significa que el usuario ha seleccionado el logo de Porshe
                    #y con ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L2.png Porsche        Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 3:
                    #Si el valor de la selección es 3, significa que el usuario ha seleccionado el logo de Renault
                    #y con ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L3.png Renault        Francia "+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 4:
                    #Si el valor de la selección es 4, significa que el usuario ha seleccionado el logo de Audi y con
                    #ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L4.png Audi           Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()
    
                elif Seleccion == 5:
                    #Si el valor de la selección es 5, significa que el usuario ha seleccionado el logo de Jaguar y con
                    #ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L5.png Jaguar         UK      "+Logos[0][30:])
                    Logos_Escuderia.close()
                    print("Logo 5 Seleccionado")
 
                elif Seleccion == 6:
                    #Si el valor de la selección es 6, significa que el usuario ha seleccionado el logo de Mahindra y con
                    #ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L6.png Mahindra       India   "+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 7:
                    #Si el valor de la selección es 7, significa que el usuario ha seleccionado el logo de BMW y con
                    #ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L7.png BMW            Alemania"+Logos[0][30:])
                    Logos_Escuderia.close()

                elif Seleccion == 8:
                    #Si el valor de la selección es 8, significa que el usuario ha seleccionado el logo de Nissan y con
                    #ello se modificará toda la información respectiva con esa Escudería
                    Logos_Escuderia = open("Team information.txt", "r+")
                    Logos = Logos_Escuderia.readlines()
                    Logos_Escuderia.seek(0)
                    Logos_Escuderia.write("L8.png Nissan         Japon   "+Logos[0][30:])
                    Logos_Escuderia.close()
                     
                else:
                    #Si el valor de la selección no es ninguno de los anteriores significa que el usuario no ha seleccionado
                    #ningún logo y por lo tanto el txt con la información de la Escudería quedará intacto 
                    print("No chance")
                    
                logo.destroy()#Destruir la ventana de selección de logo
                information()#Se vuelve a cargar la ventana para que se vea la

            #Botón para confirmar cambio de la selección o no del logo
            Btn_back = Button(logo, text="Confirmar Cambio", command=back, bg="#cb3234", fg="white")
            Btn_back.place(x=540,y=590)

            #Posición estratégica de los radio buttons para cada logo seleccionable por el usuario
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
            """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: patrocinadores()
Descripción: Ventana para poder editar(agregar o quitar) los patrocinadores de la Escudería

Entrada: Ninguna
Salida: Lista actualizada de los patrocinadores cada vez que el usario decida editarla
Restricciones: La Escudería debe tener al menos un patrocinador"""

            #Se deshabilita los atributos de la ventana de información de la Escudería hasta que el usuario termine
            #de editar los patrocinadores
            info.attributes('-disabled', True)
            #Se crea la ventana para la edición de los patrocinadores y sus atributos
            patro = Toplevel()
            patro.title("Patrocinadores")#Título de la ventana
            patro.minsize(650,100)#Tamaño mímimo de la ventana
            patro.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

            #Canvas de la ventana de patrocinadores
            C_patro = Canvas(patro, width=650, height=650, bg="white")
            C_patro.place(x=0, y=0)

            #Entry para poner en la ventana todos los patrocinadores actuales de la Escudería
            E_patro = Entry(C_patro, text="hola", width=60,font=("Agency FB",14))
            E_patro.place(x=5, y=75)

            #Se abre el txt que contiene la información de la Escudería
            Logos_Escuderia = open("Team information.txt", "r+")
            Logos = Logos_Escuderia.readlines()
            Logos_Escuderia.seek(0)

            #Se insertan sobre el Entry todos los patrocinadores actuales de la Escudería
            E_patro.insert(0, Logos[0][37:])

            def confirmar():
                #Se almacena en una variable todo los patrocinadores que el usuario ha editado y los que previamente estaban
                AEscribir = str(E_patro.get())
                print(AEscribir)
                #Se específica dónde escribir los patrocinadores en el txt que contiene la información general de la Escudería
                Logos_Escuderia.seek(37)
                #Se escribe en el txt en lugar previamente indicado
                Logos_Escuderia.write(AEscribir)
                #Se elimina el Entry
                E_patro.delete(0, END)
                #Se cierra el archivo txt para guardar los datos previamente modificados
                Logos_Escuderia.close()
                #Se deshabiltan los atributos para poder seguir usando la ventana de información, por si se requiere realizar
                #o no otro cambio
                info.attributes('-disabled', False)
                patro.destroy()#Se destruye la ventana de patrocinadores
                info.destroy()#Se destruye la ventana de información
                information()#Se vuelve a cargar la ventana de información para visualizar los cambios que el usuario ha hecho con
                             #respecto a los patrocinadores de la Escudería

            #Botón para confirmar los cambios hechos a los patrocinadores de la Escudería   
            Btn_confirmar = Button(patro, text="Confirmar cambios", command=confirmar, bg="light blue", fg='black')
            Btn_confirmar.place(x=300, y=100)

            main.mainloop()
            
        def back():
            #Descripción: Función para cerrar la ventana de información una vez que el usuario ha podido visualizar y editar la
            #información de la Escudería

            #Entrada: Ninguna
            #Salida: Actualización de todos los cambios hecho en la ventana de información de la Escudería 
            #Restricción: El usuario no está obligado a cambiar la información de la Escudería
            info.destroy()#Se destruye la ventana de información de la Escudería
            main.destroy()#Se destruye la ventana principal 
            main_window()#Se vuelva a cargar la ventana principal para actualizar posibles cambios que el usuario haya hecho
                         #en la venatana de información de la Escudería

        #Función para poner sobre la ventana de información de la Escudería todos los patrocinadores actuales de la misma
        patrocinio(Patro,"",900, 75)

        #Botón para la ventana encargada de cambiar el logo de la Escudería y su respectiva información(nombre y ubicación)
        Btn_logo = Button(info, text="Cambiar Logo", command=chance_logo, bg="light blue", fg='black')
        Btn_logo.place(x=1055,y=90)

        #Botón para la ventana encargada de editar(agregar o quitar) los patrocinadores de la Escudería
        Btn_patrocinadores = Button(info, text="Editar Patrocinadores", command=patrocinadores, bg="light blue", fg='black')
        Btn_patrocinadores.place(x=1050,y=200)

        #Botón para ir a la ventana de tablas de posiciones de pilotos y autos
        Btn_Pilotos = Button(info, text="Lista Pilotos y Autos", command=positions_table, bg="light blue", fg='black')
        Btn_Pilotos.place(x=665,y=150)

        #Botón para regresar a la ventana principal
        Btn_back = Button(info, text="Back", command=back, bg="light blue", fg='black')
        Btn_back.place(x=10,y=10)

        main.mainloop()

    #Thread para iniciar la animación inicial de la interfaz  
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
        """
        Instituto Tecnológico de Costa Rica
        Ingeniería en Computadores
        Introducción a la programación
        Profesor: Milton Villegas Lemus
        Autor: Alejandro Vásquez Oviedo
        Programa: positions_table
        Última fecha de modificación: 2/6/2019
        Versión: 1.0
        Lenguaje: Python 3.7.3
        Entradas: Ninguna
        Restricciones: No tiene
        Salidas: Muestra la ventana que posee la tabla de posiciones de autos y pilotos, muestra además
        los datos solititados para los pilotos y los autos, además permite su ordenamiento según el REP,
        RGP o eficiencia en caso de los carros. Además permite la edición en su totalidad de los datos de
        ambas tablas. Utiliza para esta tarea distintas funciones auxiliares tales como:
        -carg_pilotos
        -carg_autos
        -edit_textP
        -cambiar
        -mod_entry
        -descendenteA
        -descendenteP_REP
        -descendenteP_RGP
        -ascendenteA
        -ascendenteP_REP
        -ascendenteP_RGP
        Si desea información específica de cada función por favor utilice el método correspondiente utilizando print.

        Llama además las función del archivo Validaciones que permiten mostrar los datos en una posición adecuada.
        """
        #Esconder ventana principal
        main.withdraw()
        #Ventana de posisiones
        positions=Toplevel()
        positions.title("Positions Table")#Nombre de la ventana
        positions.minsize(800,650)#Tamaño de la ventana
        positions.resizable(width=NO, height=NO)#Evita que se pueda modificar el tamaño de la ventana

        #Código para las pestañas    
        tab_control = ttk.Notebook(positions)#Habilita el método de pestañas
        tab1 = ttk.Frame(tab_control)#Crea la primera pestaña
        tab2 = ttk.Frame(tab_control)#Crea la segunda pestaña
        tab_control.add(tab1, text='Pilotos')#Asigna nombre a la pestaña
        tab_control.add(tab2, text='Autos')#Asigna nombre a la pestaña

        C_positionsP = Canvas(tab1, width=800, height=650)
        C_positionsP.place(x=0, y=0)
    
        C_positionsA = Canvas(tab2, width=800, height=650)
        C_positionsA.place(x=0, y=0)

        #Abrir documento de pilotos y autos  
        arch_pilotos = open("Tabla de posiciones Pilotos.txt","r+")#Abre el documento de pilotos
        lista_pilotos = arch_pilotos.readlines()#Lo transforma a una lista

        arch_autos = open("Tabla de posiciones Autos.txt","r+")#Abre el documento de autos
        lista_autos = arch_autos.readlines()#Lo transforma a lista

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
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_pilotos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: mostrar en pantalla los distintos textos e imágenes de todos los pilotos según su posición en el archivo txt
            del cual se obtienen los datos. Esto a través de una for que recorre todas las filas del documento por medio de un range
            con lo cual siempre muestra todos los datos. La idea de utilizar un for para simplificar el código fue dada por el
            compañero David Solís, gracias a esta idea se creó el código utilizado.
            """
            y = 75
            for i in range(0,10):#Indica que la primera posición es a los 75 pixeles en el eje y
                C_positionsP.create_text(120,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][10:nombres(lista_pilotos[i])])
                C_positionsP.create_text(405,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][edad(lista_pilotos[i])[0]:edad(lista_pilotos[i])[1]]) #Edad y nacionalidad
                C_positionsP.create_text(528,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][edad(lista_pilotos[i])[1]:edad(lista_pilotos[i])[2]])
                C_positionsP.create_text(592,y,font=("Arial", 10, "bold"), anchor=NW,tags=("pilot"),fill="white", text=lista_pilotos[i][edad(lista_pilotos[i])[2]:])
            
                y+=55#Aumenta la posición en y del nuevo texto en 55 pixeles
            
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
        
        carg_pilotos()#Llama a la función encargada de cargar los datos e imágenes de los pilotos

        #Datos e imágenes de Autos
        def carg_autos():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_autos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: mostrar en pantalla los distintos textos e imágenes de todos los autos según su posición en el archivo txt
            del cual se obtienen los datos. Esto a través de una for que recorre todas las filas del documento por medio de un range
            con lo cual siempre muestra todos los datos. La idea de utilizar un for para simplificar el código fue dada por el
            compañero David Solís, gracias a esta idea se creó el código utilizado.
            """
            y = 75#Indica que la primera posición es a los 75 pixeles en el eje y 
            for i in range(0,10):
                C_positionsA.create_text(180,y,font=("Arial", 10, "bold"), anchor=NW,fill="white", text=lista_autos[i][8:nombres(lista_autos[i])])
                C_positionsA.create_text(380,y,font=("Arial", 10, "bold"), anchor=NW,fill="white", text=lista_autos[i][edad_a(lista_autos[i])[0]:edad_a(lista_autos[i])[1]])
                C_positionsA.create_text(500,y,font=("Arial", 10, "bold"), anchor=NW,fill="white", text=lista_autos[i][edad_a(lista_autos[i])[1]:])

                y+=55#Aumenta la posición en y del nuevo texto en 55 pixeles
            
            C_positionsA.create_image(65,65,image=Auto1, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,115,image=Auto2, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,169,image=Auto3, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,227,image=Auto4, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,280,image=Auto5, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,337,image=Auto6, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,383,image=Auto7, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,437,image=Auto8, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,485,image=Auto9, anchor=NW,state=NORMAL)#Imagen del piloto
            C_positionsA.create_image(65,542,image=Auto10, anchor=NW,state=NORMAL)#Imagen del piloto
            
        carg_autos()#Llama a la función que carga toda la información e imágenes de los autos
        tab_control.pack(expand=1, fill='both')#Línea que termina la creación correcta de las pestañas

        #Funciones de botones
        def back():#Función que permite regresar a la ventana principal
            arch_autos.close()
            arch_pilotos.close()
            positions.destroy()
            main.deiconify()

        def edit_textP(y,Elegir,i):
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: edit_textP
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: la coordenada en y del botón seleccionado, el indicador de si es un botón de autos o pilotos, y un contador
            que permite identificar la fila debe mostrarse para edición en los Entrys.
            Restricciones: no hay
            Salidas: muestra una ventana nueva, deshabilitando la de posiciones, donde se muestra al usuario tres entrys que le permiten editar
            los distintos aspectos de los autos o los pilotos y es la función encargada de reescribir la información y actualizar la ventana para
            mosrar los cambios. Esto gracias a las funciones auxiliares como:
            -cambiar
            -mod_entry
            Y las funciones que se encuentran en el archivo Validación.py
            """
            positions.attributes('-disabled', True)#Comando que deshabilita todos los botones de la tabla de posiciones mientras se muestre la
            #ventana de edición
            edit=Toplevel()#Crea la ventana
            edit.title("Edit")#Da un nombre a la ventana
            edit.minsize(650,100)#Define el tamaño de la ventana
            edit.resizable(width=NO, height=NO)#Evita que se pueda modificar el tamaño de la ventana
            C_edit=Canvas(edit, width=650,height=650, bg='light blue')#Crea un canvas en la ventana
            C_edit.place(x=0,y=0)#Posiciona el canvas en las coordenadas (0,0)
            C_edit.create_image(0,0,image=Edit_F, anchor=NW,state=NORMAL)#Define el fondo del canvas
            Lista = 0#Define la variable que contendrá a la lista del archivo
            arch = 0#Defina la variable donde se guardará el archivo
            
            if Elegir == 0:#Si es 0 indica que se presionó un botón de autos y abre este archivo
                arch = open("Tabla de posiciones Autos.txt","r+")#Asigna el archivo a la variable
                Lista = arch.readlines()#Asigna la lista del archivo a la variable
                
            if Elegir == 1:#Si es 1 indica que se presionó un botón de pilotos y abre este archivo    
                arch = open("Tabla de posiciones Pilotos.txt","r+")#Asigna el archivo a la variable
                Lista = arch.readlines()#Asigna la lista del archivo a la variable
                
            if Elegir == 1:#Si es 1 muestra el texto con los datos que se muestran en esta pestaña de los pilotos   
                C_edit.create_text(5,70,font=("Arial", 12, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Nombre:")
                C_edit.create_text(200,80,font=("Arial", 9, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Edad Nacionalidad Temporada")
                C_edit.create_text(380,80,font=("Arial",9,"bold"),anchor=NW,tags=("pilot"),fill="white",text="Compet. RGP REP")
                
            if Elegir == 0:#Si es 0 muestra el texto con los datos que se muestran en esta pestaña de los autos
                C_edit.create_text(5,70,font=("Arial", 12, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Marca:")
                C_edit.create_text(200,80,font=("Arial", 9, "bold"), anchor=NW,tags=("pilot"),fill="white", text="Temp. Modelo")
                C_edit.create_text(380,80,font=("Arial",9,"bold"),anchor=NW,tags=("pilot"),fill="white",text="Eficiencia") 
        
            E_name = Entry(C_edit,text="hola",width=25,font=("Agency FB",14))#Se crea el primer entry
            E_name.place(x=0,y=100)#Se coloca el primer entry
            E_age = Entry(C_edit,text="texto",width=20,font=("Agency FB",14))#Se crea el segundo entry
            E_age.place(x=210,y=100)#Se posiciona el segundo entry
            E_rest = Entry(C_edit,width=15,font=("Agency FB",14))#Se crea el tercer entry
            E_rest.place(x=380,y=100)#Se posiciona el segundo entry
            def mod_entry(y,i,n,Elegir):
                """
                Instituto Tecnológico de Costa Rica
                Ingeniería en Computadores
                Introducción a la programación
                Profesor: Milton Villegas Lemus
                Autor: Alejandro Vásquez Oviedo
                Programa: mod_entry
                Última fecha de modificación: 2/6/2019
                Versión: 1.0
                Lenguaje: Python 3.7.3
                Entradas: coordenada dle botón, indicador de fila, comparador de la coordenada con la fila y el valor que indica si
                auto o piloto.
                Restricciones: no hay
                Salidas: es la función encargada de mostrar en los distintos entrys los datos correspondientes según sea el botón
                que se presione
                """
                if Elegir == 1:#Se eligieron pilotos
                    if y == 75: #Quiere decir que es desde el botón de la primera fila
                        E_name.insert(END,Lista[0][9:nombres(Lista[0])])#Inserta el nombre
                        E_age.insert(0,Lista[0][edad(lista_pilotos[0])[0]:edad(lista_pilotos[0])[2]])#Inserta la edad, la temporada
                        E_rest.insert(0,Lista[0][edad(lista_pilotos[0])[2]:])#Inserta el número de competencias, REP y RGP
                        return#Sale de la función
                    if y == n:#Entra aquí una vez se encuentre la fila para cual coincide la coordenada del botón enviada
                        E_name.insert(END,Lista[i][9:nombres(Lista[i])])#Inserta el nombre
                        E_age.insert(0,Lista[i][edad(lista_pilotos[i])[0]:edad(lista_pilotos[i])[2]])#Inserta la edad y la temporada
                        E_rest.insert(0,Lista[0][edad(lista_pilotos[i])[2]:])#Inserta el número de competencias, REP y RGP
                        return#Sale de la función
                    else:
                        return mod_entry(y,i+1,n+55,Elegir)#En caso de no ser la primera fila y no coincidir la y con la n se hará una
                                                            #llamada recursiva aumentnado la n en 55 y la i en 1 para poder revisar si
                                                            #ahora sí corresponde a la y enviada y cargar esa fila.
                elif Elegir == 0:#Se eligieron autos
                    if y == 75:#Quiere decir que es desde el botón de la primera fila
                        E_name.insert(END,Lista[0][9:nombres(Lista[0])])#Inserta la marca
                        E_age.insert(0,Lista[0][edad_a(lista_autos[0])[0]:edad_a(lista_autos[0])[1]])#Inserta la temporada y el modelo
                        E_rest.insert(0,Lista[0][edad_a(lista_autos[0])[1]:])#Inserta la eficiencia
                        return
                    if y == n:#Entra aquí una vez se encuentre la fila para cual coincide la coordenada del botón enviada
                        E_name.insert(END,Lista[i][9:nombres(Lista[i])])#Inserta la marca
                        E_age.insert(0,Lista[i][edad_a(lista_autos[i])[0]:edad_a(lista_autos[i])[1]])#Inserta la temporada y el modelo
                        E_rest.insert(0,Lista[i][edad_a(lista_autos[i])[1]:])#Inserta la eficiencia
                        return
                    else:
                        return mod_entry(y,i+1,n+55,Elegir)#En caso de no ser la primera fila y no coincidir la y con la n se hará una
                                                            #llamada recursiva aumentnado la n en 55 y la i en 1 para poder revisar si
                                                            #ahora sí corresponde a la y enviada y cargar esa fila.
                    
            mod_entry(y,1,125,Elegir)#Llama a la función que se encarga de mostrar los datos en los entrys
            def cambiar(i,Lista,Elegir):
                """
                Instituto Tecnológico de Costa Rica
                Ingeniería en Computadores
                Introducción a la programación
                Profesor: Milton Villegas Lemus
                Autor: Alejandro Vásquez Oviedo
                Programa: cambiar
                Última fecha de modificación: 2/6/2019
                Versión: 1.0
                Lenguaje: Python 3.7.3
                Entradas: indicador de la fila, la lista del documento, y el indicador de si es la lista de pilotos o autos
                Restricciones: no hay
                Salidas: función cuya labor es tomar los textos de los entrys, unirlos en un solo string, y cargarlo en la posición
                i correspondiente para luego reescribir esta lista en el txt ahora modificado por el usuario
                """
                Nombre = str(E_name.get())#Toma el texto del primer entry
                Datos1 = str(E_age.get())#Toma el texto del segundo entry
                Datos2 = str(E_rest.get())#Toma el texto del tercer entry
                AEscribir = Lista[i][:9]+str(E_name.get())+str(E_age.get())+" "+str(E_rest.get())#Une los tres entrys en una sola variable de tipo string
            
                Lista[i] = AEscribir#Inserta la nueva información en la columna correspondiente
                if Elegir == 0:#Indica que se debe escribir en el archivo de autos
                    arch = open("Tabla de posiciones Autos.txt","w")#Abre el archivo para escribir
                    arch.writelines(Lista)#Inserta ahora la lista modificada
                    arch.close#Cierra el archivo

                elif Elegir == 1:#Indica que se debe escribir en el archivo de pilotos
                    arch = open("Tabla de posiciones Pilotos.txt","w")#Abre el archivo para escribir
                    arch.writelines(Lista)#Inserta ahora la lista modificada
                    arch.close#Cierra el archivo
            
                E_name.delete(0, END)#Elimina el texto de entry
                E_age.delete(0, END)#Elimina el texto de entry
                E_rest.delete(0,END)#Elimina el texto de entry
                arch.close()#Cierra el archivo
                positions.attributes('-disabled', False)#Habilita nuevamente los botones de la ventana de posiciones
                edit.destroy()#Destruye la ventana de edición
                positions.destroy()#Destruye la ventana de posiciones
                positions_table()#Crea nuevamente la ventana de posiciones
            def disable_event():#Función en caso de que se presione la "x" en la ventana
                E_name.delete(0, END)#Elimina el texto de entry
                E_age.delete(0, END)#Elimina el texto de entry
                E_rest.delete(0,END)#Elimina el texto de entry
                arch.close()#Cierra el archivo
                positions.attributes('-disabled', False)#Habilita nuevamente los botones de la ventana de posiciones
                edit.destroy()#Destruye la ventana de edición
            edit.protocol("WM_DELETE_WINDOW", disable_event)#Llama a la función que indica qué debe hacer la "x"
            Btn_back = Button(edit, text="Confirmar cambio", command=lambda: cambiar(i,Lista,Elegir), bg="light blue", fg='black')#Define el botón de confirmar cambio
            Btn_back.place(x=530,y=100)#Posiciona el botón de comfirmar cambio

        def new_car():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: new_car
            Última fecha de modificación: 3/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: muestra una ventana nueva, deshabilitando la de posiciones, en la cual se puede ingresar un nuevo auto para la temporada
            Utiliza la función auxiliar:
            -crear
            """
            positions.attributes('-disabled', True) #Comando que deshabilita todos los botones de la tabla de posiciones mientras se muestre la
            #ventana de edición
            new=Toplevel() #Crea la ventana
            new.title("Add") #Da un nombre a la ventana
            new.minsize(650,100) #Define el tamaño de la ventana
            new.resizable(width=NO, height=NO) #Evita que se pueda modificar el tamaño de la ventana
            C_new=Canvas(new, width=650,height=650, bg='light blue') #Crea un canvas en la ventana
            C_new.place(x=0,y=0)#Posiciona el canvas en las coordenadas (0,0)
            C_new.create_image(0,0,image=Edit_F, anchor=NW,state=NORMAL) #Define el fondo del canvas

            arch = open("Tabla de posiciones Autos.txt","r+")
            Lista = arch.readlines()

            E_new = Entry(C_new,text="",width=40, font=("Agency FB",14))
            E_new.place(x=0,y=100)

            def crear():
                """
                Esta función se encarga de agregar el nuevo carro al archivo de texto
                """
                New_car = str(E_new.get())
                AEscribir = New_car
                Lista.insert(0,[AEscribir])

                arch = open("Tabla de posiciones Autos.txt","w")#Abre el archivo para escribir
                arch.writelines(Lista) #Inserta la lista modificada
                arch.close #Cierra el archivo
                
                E_new.delete(0, END)#Elimina el texto de entry

                #arch.close()#Cierra el archivo
                positions.attributes('-disabled', False)#Habilita nuevamente los botones de la ventana de posiciones
                new.destroy()#Destruye la ventana de edición
                positions.destroy()#Destruye la ventana de posiciones
                positions_table()#Crea nuevamente la ventana de posiciones
                
            def disable_event(): #Función en caso de que se presione la "x" en la ventana
                E_new.delete(0, END)#Elimina el texto de entry
                arch.close()#Cierra el archivo
                positions.attributes('-disabled', False)#Habilita nuevamente los botones de la ventana de posiciones
                new.destroy()#Destruye la ventana de edición
                new.protocol("WM_DELETE_WINDOW", disable_event)#Llama a la función que indica qué debe hacer la "x"
            Btn_back = Button(new, text="Agregar nuevo carro", command=crear, bg="light blue", fg='black')#Define el botón de agregar nuevo carro
            Btn_back.place(x=530,y=100)#Posiciona el botón de comfirmar cambio

############################### FUNCIONES ORDENAMIENTO AUTOS #############################      
        def descendenteA():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: descendenteA
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: es la función encargada del ordenamiento por eficiencia de los carros, de forma
            descendente, utilizando el método de ordenamiento por selección cuyo código fue dado por
            el profesor Milton Villegas Lemus, se adaptó de manera que cumpliera con la función
            requerida. 
            """
            def seleccion(Lista):
                return seleccion_aux(Lista,0,len(Lista),0)#Llama la función auxiliar

            def menor(Lista,j,n,Min):
                if j == n:
                    return Min
                if Lista[j][-6:] > Lista[Min][-6:]:#Compara los últimos elementos de la fila actual y la fila menor
                    Min = j
                return menor(Lista,j+1,n,Min)#Retorna la función con la siguiente fila a evaluar
            
            def seleccion_aux(Lista,i,n,ContadorRep):
                if i == n:#Condición de parada
                    return Lista
                Min = menor(Lista,i+1,n,i)#Llama a la función que calcula el elemento menor
                Tmp = Lista[i]#Elemento temporal donde se guarda el elemento a cambiar
                Lista[i] = Lista[Min]#Reemplazo de elementos
                Lista[Min] = Tmp#Se utiliza la variable temportal
                return seleccion_aux(Lista,i+1,n,ContadorRep+1)#Llamada recursiva
            TablaAutos = open("Tabla de posiciones Autos.txt","r+")
            Lista = TablaAutos.readlines()
            TablaAutos.seek(0)
            TablaAutos.write(''.join(seleccion(Lista)))#Escribe la nueva lista ordenada según se solicitó
            TablaAutos.close()
            positions.destroy()#Cierra la ventana
            positions_table()#La vuelve a crear con los datos actualizados 

        def ascendenteA():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_autos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: es la función encargada del ordenamiento por eficiencia de los carros, de forma
            ascendente, utilizando el método de ordenamiento por selección cuyo código fue dado por
            el profesor Milton Villegas Lemus, se adaptó de manera que cumpliera con la función
            requerida.
            """
            def seleccion(Lista):
                return seleccion_aux(Lista,0,len(Lista),0)#Llama la función auxiliar

            def menor(Lista,j,n,Min):
                if j == n:
                    return Min
                if Lista[j][-6:] < Lista[Min][-6:]:#Compara los últimos elementos de la fila actual y la fila menor
                    Min = j
                return menor(Lista,j+1,n,Min)#Retorna la función con la siguiente fila a evaluar
            
            def seleccion_aux(Lista,i,n,ContadorRep):
                if i == n:#Condición de parada
                    return Lista
                Min = menor(Lista,i+1,n,i)#Llama a la función que calcula el elemento menor 
                Tmp = Lista[i]#Elemento temporal donde se guarda el elemento a cambiar
                Lista[i] = Lista[Min]#Reemplazo de elementos
                Lista[Min] = Tmp#Se utiliza la variable temportal
                return seleccion_aux(Lista,i+1,n,ContadorRep+1)#Llamada recursiva
            TablaAutos = open("Tabla de posiciones Autos.txt","r+")
            Lista = TablaAutos.readlines()
            TablaAutos.seek(0)
            TablaAutos.write(''.join(seleccion(Lista)))#Escribe la lista modificada
            positions.update
            TablaAutos.close()
            positions.update
            positions.destroy()#Cierra la ventana
            positions_table()#La muestra nuevamente pero con los datos actualizados

############################## FUNCIONES ORDENAMIENTO PILOTOS ##########################
        def descendenteP_REP():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_autos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: es la función encargada del ordenamiento por REP de los autos, de forma
            descendente, utilizando el método de ordenamiento por selección cuyo código fue dado por
            el profesor Milton Villegas Lemus, se adaptó de manera que cumpliera con la función
            requerida.
            """
            def seleccion(Lista):
                return seleccion_aux(Lista,0,len(Lista),0)#Llama a la función auxiliar

            def menor(Lista,j,n,Min):
                if j == n:
                    return Min
                if Lista[j][-6:] > Lista[Min][-6:]:#Compara el elemento actual con el elemento menor
                    Min = j
                return menor(Lista,j+1,n,Min)#Llamada recurisiva con la siguiente fila a evaluar
            
            def seleccion_aux(Lista,i,n,ContadorRep):
                if i == n:#Condición de parada
                    return Lista
                Min = menor(Lista,i+1,n,i)#Llama a la función que calcula el mayor más pequeño
                Tmp = Lista[i]#Variable temporal
                Lista[i] = Lista[Min]#Reasigna valores 
                Lista[Min] = Tmp
                return seleccion_aux(Lista,i+1,n,ContadorRep+1)#Llamada recursiva
            TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
            Lista = TablaAutos.readlines()
            TablaAutos.seek(0)
            TablaAutos.write(''.join(seleccion(Lista)))#Escribe la nueva lista modificada
            TablaAutos.close()
            positions.destroy()#Cierra la ventana
            positions_table()#Vuelve a crearla con los datos actualizados

        def ascendenteP_REP():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_autos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: es la función encargada del ordenamiento por REP de los pilotos, de forma
            ascendente, utilizando el método de ordenamiento por selección cuyo código fue dado por
            el profesor Milton Villegas Lemus, se adaptó de manera que cumpliera con la función
            requerida.
            """
            def seleccion(Lista):
                return seleccion_aux(Lista,0,len(Lista),0)#Llama a la función auxiliar

            def menor(Lista,j,n,Min):
                if j == n:
                    return Min
                if Lista[j][-6:] < Lista[Min][-6:]:#Compara el elemento actual con el menor
                    Min = j
                return menor(Lista,j+1,n,Min)#Llama la función con la siguiente fila a evaluar
            
            def seleccion_aux(Lista,i,n,ContadorRep):
                if i == n:
                    return Lista
                Min = menor(Lista,i+1,n,i)#Llama a la función que calcula el menor
                Tmp = Lista[i]#Variable temporal donde se guarda el dato
                Lista[i] = Lista[Min]
                Lista[Min] = Tmp
                return seleccion_aux(Lista,i+1,n,ContadorRep+1)
            TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
            Lista = TablaAutos.readlines()
            TablaAutos.seek(0)
            TablaAutos.write(''.join(seleccion(Lista)))#Escribe la lista ya modificada
            TablaAutos.close()
            positions.destroy()#Cierra la ventana
            positions_table()#La vuelve a mostrar pero con datos actualizados
            
###########################################################################
        def descendenteP_RGP():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_autos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: es la función encargada del ordenamiento por RGP de los pilotos, de forma
            descendente, utilizando el método de ordenamiento por selección cuyo código fue dado por
            el profesor Milton Villegas Lemus, se adaptó de manera que cumpliera con la función
            requerida.
            """
            def seleccion(Lista):
                return seleccion_aux(Lista,0,len(Lista),0)#Llama a la función auxiliar

            def menor(Lista,j,n,Min):
                if j == n:
                    return Min
                if Lista[j][-12:-6] > Lista[Min][-12:-6]:#Compara para saber cuál es el elemento menor
                    print(Lista[j][-12:-6])
                    Min = j
                return menor(Lista,j+1,n,Min)#Llama a la función con la siguiente fila a evaluar
            
            def seleccion_aux(Lista,i,n,ContadorRep):
                if i == n:#Condición de parada
                    return Lista
                Min = menor(Lista,i+1,n,i)#Llama a la función que calcula el elemento menor
                Tmp = Lista[i]#Variable temporal donde se almacena el elemento
                Lista[i] = Lista[Min]#Reasignación de variables
                Lista[Min] = Tmp
                return seleccion_aux(Lista,i+1,n,ContadorRep+1)
            TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
            Lista = TablaAutos.readlines()
            TablaAutos.seek(0)
            TablaAutos.write(''.join(seleccion(Lista)))#Escribe la nueva lista modificada en el txt
            TablaAutos.close()
            positions.destroy()#Destruye la ventana 
            positions_table()#Crea la ventana con los datos actualizados

        def ascendenteP_RGP():
            """
            Instituto Tecnológico de Costa Rica
            Ingeniería en Computadores
            Introducción a la programación
            Profesor: Milton Villegas Lemus
            Autor: Alejandro Vásquez Oviedo
            Programa: carg_autos
            Última fecha de modificación: 2/6/2019
            Versión: 1.0
            Lenguaje: Python 3.7.3
            Entradas: ninguna
            Restricciones: no hay
            Salidas: es la función encargada del ordenamiento por RGP de los pilotos, de forma
            ascendente, utilizando el método de ordenamiento por selección cuyo código fue dado por
            el profesor Milton Villegas Lemus, se adaptó de manera que cumpliera con la función
            requerida.
            """
            def seleccion(Lista):
                return seleccion_aux(Lista,0,len(Lista),0)#Llama a la función auxiliar

            def menor(Lista,j,n,Min):
                if j == n:
                    return Min
                if Lista[j][-12:-6] < Lista[Min][-12:-6]:#Compara el elemento actual con el menor
                    Min = j
                return menor(Lista,j+1,n,Min)#Llama a la función para evaluar la siguiente fila
            
            def seleccion_aux(Lista,i,n,ContadorRep):
                if i == n:#Condición de parada
                    return Lista
                Min = menor(Lista,i+1,n,i)#Llama a la función que calcula el mínimo 
                Tmp = Lista[i]#Usa una variable temporal para almacenar el dato
                Lista[i] = Lista[Min]#Reasigna valores
                Lista[Min] = Tmp
                return seleccion_aux(Lista,i+1,n,ContadorRep+1)
            TablaAutos = open("Tabla de posiciones Pilotos.txt","r+")
            Lista = TablaAutos.readlines()
            TablaAutos.seek(0)
            TablaAutos.write(''.join(seleccion(Lista)))#Reescribe la lista en el documento txt
            TablaAutos.close()
            positions.destroy()#Destruye la ventana
            positions_table()#Crea la ventana con los datos actualizados

###########################################################################
        #Botones de la ventana
        Btn_back = Button(positions, text="Back", command=back, bg="light blue", fg='black')#Botón para regresar a la ventana principal
        Btn_back.place(x=750,y=615)

        #Botones pestaña pilotos
        Btn_Descendente =Button(tab1, text="Descendente REP", command=descendenteP_REP, bg="light blue", fg='black')#Botón de ordenamiento por REP de los pilotos descendente
        Btn_Descendente.place(x=270,y=592)
    
        Btn_Ascendente =Button(tab1, text="Ascendente REP", command=ascendenteP_REP, bg="light blue", fg='black')#Botón de ordenamiento por REP de los pilotos ascendente
        Btn_Ascendente.place(x=380,y=592)

        Btn_Descendente =Button(tab1, text="Descendente RGP", command=descendenteP_RGP, bg="light blue", fg='black')#Botón de ordenamiento por RGP de los pilotos descendente
        Btn_Descendente.place(x=490,y=592)
    
        Btn_Ascendente =Button(tab1, text="Ascendente RGP", command=ascendenteP_RGP, bg="light blue", fg='black')#Botón de ordenamiento por RGP de los pilotos ascendente
        Btn_Ascendente.place(x=600,y=592)

        #Botones de edición de texto de la pestaña de pilotos
        #Se utiliza lambda en los commands para evitar que se ejecuten de manera instantánea ya que poseen argumentos
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

        Btn_Crear =Button(tab2, text="Añadir auto", command=new_car, bg="light blue", fg='black')#Botón de ordenamiento por eficiencia de los autos ascendente
        Btn_Crear.place(x=400,y=587)

        
        #Botones de edición de la pestaña de autos
        #Se utiliza lambda en los commands para evitar que se ejecuten de manera instantánea ya que poseen argumentos
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
       """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: test_drive()
Descripción: Ventana para poder realizar el Test Drive al cumplirse que el usuario haya seleccionado primeramente un piloto
de la Temporada actual y que el estado del carro es Disponible.

Entrada: Ninguna
Salida: Ventana auxiliar para realizar el Test del carro y ventana para la selección del piloto de la Temporada actual
Restricciones: Para poder realizar el Test Drive el usuario debe seleccionar un piloto de la presente Temporada y el estado
del carro deber ser Disponible, es decir, estar cargado."""
       
       #Esconder ventana principal
       main.withdraw()
       #Ventana de para ek manejo del carro y sus atributos
       test=Toplevel()
       test.title("Driving Test")#Título de la ventana de Test Drive
       test.minsize(450, 625)#Tamaño mínimo de la ventana
       test.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

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
           """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: test_drive()
Descripción: Función que muestra en pantalla todos los datos (Foto, nombre, nacionalidad, Temporada, RGP, REP, entre otros)
de los pilotos de la Temporada 2019 para que el usuario pueda seleccionar uno de los dos. Una vez hecha la selección del
piloto, todos los datos de este se almacenaran en una variable global para ponerlos en pantalla una vez iniciado el test.

Entrada: Ninguna
Salida: Guarda los datos del piloto que el usuario ha seleccionado para realizar el test
Restricciones: Deben haber a lo sumo dos pilotos de la Temporada 2019, el usuario debe seleccionar
un piloto, de lo contrario no podrá realizar el test."""
           
           #Ventana para la selección del piloto y sus atributos
           pilot=Toplevel()
           pilot.title("Selección de piloto")#Título de la ventana
           pilot.minsize(900, 300)#Tamaño mímimo de la ventana
           pilot.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

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
           C_pilot.create_text(70, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[10:35])
           C_pilot.create_text(70, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[10:35])

           #Edad de los Pilotos
           C_pilot.create_text(280, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Edad")
           C_pilot.create_text(290, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[35:37])
           C_pilot.create_text(290, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[35:37])

           #Nacionalidad de los Pilotos
           C_pilot.create_text(350, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Nacionalidad")
           C_pilot.create_text(360, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[38:53])
           C_pilot.create_text(360, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[38:53])

           #Temporada, en este caso será la del 2019
           C_pilot.create_text(500, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Temporada")
           C_pilot.create_text(530, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[53:58])
           C_pilot.create_text(530, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[53:58])

           #Número de competiciones de ambos pilotos
           C_pilot.create_text(620, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="Competencias")
           C_pilot.create_text(680, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[58:63])
           C_pilot.create_text(680, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[58:63])

           #Rendimiento global de los Pilotos
           C_pilot.create_text(790, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="RGP")
           C_pilot.create_text(795, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[63:69])
           C_pilot.create_text(795, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[63:69])

           #Rendimiento específico de los Pilotos
           C_pilot.create_text(850, 50, font=("Agency", 16, "bold"), anchor=NW, fill="black", text="REP")
           C_pilot.create_text(855, 110, font=("Agency", 12), anchor=NW, fill="black", text=PilotoA[69:74])
           C_pilot.create_text(855, 210, font=("Agency", 12), anchor=NW, fill="black", text=PilotoB[69:74])

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
           #Descripción: Funcón que verifica que el usuario haya seleccionado uno de los pilotos de la presente
           #Temporada para que en conjunto con el Estado actual del carro, se pueda o no realizar el Test Drive

           #Entrada: Ninguna
           #Salida: Se llama a la ventana auxiliar para el manejo del carro en
           #Restriciones: El usuario debe seleccionar uno de los pilotos si quiere realizar el Test Drive del carro

           #Varable global que almacena el piloto seleccionado por el usuario para poner los datos en la ventana
           #de Drive Car para manejar el carro
           global Piloto

           #Si la variable no está vacía, significa que el usuario ya ha seleccionado uno de los dos pilotos y por
           #lo tanto sí podra realizar el Drive Car, también considerando el estado actual del carro para tal efecto
           if Piloto!="":
               return drive_car_aux()

           #Si la variable está vacía, significa que el usuario aún no ha seleccionado a ningún piloto para realizar
           #el Drive Car. Considerando lo anterior, si el usuario desea iniciar el Drive Car, aparecerá un messagebox
           #indicando que no puede realizar el Drive Car por tal motivo 
           else:
               messagebox.showwarning("Pilot selection", "No se ha seleccionado un piloto")
               
       def drive_car_aux():
           """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: drive_car_aux()
Descripción: Ventana para manejar el carro mediante teclas, poder visualizar cada acción que el usuario decide en
la interfaz, ver el nombre y nacionalidad del piloto que el usuario decidió realizar el Drive Car, ver el nivel de
batería, detectar el tiempo(día o noche), además poder visualizar el nombre de la escuderia, así como realizar la
celebración característica del piloto y los comandos especiales del carro(Circle, Infinite, ZigZag y Katarsys)

Entrada: Ninguna
Salida: Manejo completo del carro, interfaz asociada a cada acción del mismo, celebraciones de los pilotos y
movimientos especiales del carro de la Temporada actual
Restricciones:."""

           #Se esconde la ventana Test Drive
           test.withdraw()
           #Se crea la ventana de Drive Car y sus atributos
           car=Toplevel()
           car.title("Driving Test")#Título de la ventana
           car.minsize(1200, 675)#Tamaño mínimo de la ventana
           car.resizable(width=NO, height=NO)#Se deshabilita poder editar el tamaño de la ventana

           #Canvas de la ventana Drive Car
           C_car = Canvas(car, width=1200, height=675, bg="white")
           C_car.place(x=0, y=0)
  
        
           def intro():
               """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: intro()
Descripción: Función que realiza la animación de la interfaz la cual tiene una duración de 2.7 segundos, una vez terminada
la animación se muestran en pantalla la interfaz completa para el manejo del carro, se muestra los botones para los comandos
especiales de movimiento del carro y la celebración característica del Piloto seleccionado para realizar tal Test

Entrada: Ninguna
Salida: Animación inicial de la interfaz, luego de que concluya la animación, se muestra el fondo de la interfaz y los botones,
para los comandos especiales y la celebración característica del piloto seleccionado.
Restricciones: No presenta"""

               #Fondo de la animación de la interfaz
               BG = loadImg("FE.1.png")
               Fondo_intro = C_car.create_image(0, 0, image=BG, anchor=NW, state=NORMAL)
               time.sleep(2.7)
               C_car.itemconfig(Fondo_intro, state=HIDDEN)

               #Fondo de la interfaz cuando es de día 
               global Car_Background1
               BG2 = loadImg("23.1E.png")
               Car_Background1 = C_car.create_image(0, 0, image=BG2, anchor=NW, state=NORMAL)

               #Fondo de la interfaz cuando es de noche
               global Car_Background2
               BG3 = loadImg("23.N.png")
               Car_Background2 = C_car.create_image(0, 0, image=BG3, anchor=NW, state=HIDDEN)

               #Fondo principal para el cambio en el manejo del carro y el encendido y apagado de las luces
               W = loadImg("Widgets.png")
               C_car.create_image(0, 0, image=W, anchor=NW, state=NORMAL)

               LB = loadImg("PB.png")
               C_car.create_image(100, 10, image=LB, anchor=NW, state=NORMAL)

               #Se carga el nombre y la nacionalidad del piloto seleccionado por el usuario para realizar el Drive Car
               global Piloto
               C_car.create_text(890, 5, font=("Agency", 20, "bold"), anchor=NW, fill="white", text=Piloto[10:35])
               C_car.create_text(1000, 45, font=("Agency", 20, "bold"), anchor=NW, fill="white", text=Piloto[38:53])

               #Se abre el txt con la información de la Escudería y se carga en pantalla el nombre de la misma
               Logo_Escuderia = Logos = open("Team information.txt", "r+")
               Logo = Logo_Escuderia.readlines()
               C_car.create_text(100, 250, font=("Agency", 22, "bold"), anchor=NW, fill="white", text=Logo[0][7:22])

               #Imagen para el encendido y apagado de las luces frontales del carro       
               global Front_img
               Front = loadImg("Frontales.png")
               Front_img = C_car.create_image(860, 180, image=Front, anchor=NW, state=HIDDEN)

               #Imagen para el encendido y apagado de las luces traseras del carro
               global Back_img
               Back = loadImg("traseras.png")
               Back_img = C_car.create_image(860, 180, image=Back, anchor=NW, state=HIDDEN)

               #Imagen para el encendido y apagado de las luz direccional izquierda del carro
               global Left_img
               Left = loadImg("di.png")
               Left_img = C_car.create_image(860, 180, image=Left, anchor=NW, state=HIDDEN)

               #Imagen para el encendido y apagado de las luz direccional derecha del carro
               global Right_img
               Right = loadImg("dd.png")
               Right_img = C_car.create_image(860, 180, image=Right, anchor=NW, state=HIDDEN)

               #Imagen para cuando el carro se mueve hacia adelante
               global F_arrow
               FA = loadImg("F.png")
               F_arrow = C_car.create_image(0, 0, image=FA, anchor=NW, state=HIDDEN)

               #Imagen para cuando el carro se mueve hacia atras
               global B_arrow
               FB = loadImg("B.png")
               B_arrow = C_car.create_image(0, 0, image=FB, anchor=NW, state=HIDDEN)

               #Se crea sobre el canvas un medio para visualizar en tiempo real la acelaración del carro
               global L_PWM_aux
               C_car.create_text(560, 400, font=("Agency", 22), anchor=NW, fill="white", text="PWM")
               L_PWM_aux = C_car.create_text(592, 462, font=("Agency", 28), anchor=NW, fill="white", text="0")

               #ACELERACION
               global LV1_aux, LV2_aux, LV3_aux
               LV1 = loadImg("LV.png")
               LV1_aux = C_car.create_image(50, 500, image=LV1, anchor=NW, state=HIDDEN)

               LV2 = loadImg("LV.png")
               LV2_aux = C_car.create_image(125, 500, image=LV2, anchor=NW, state=HIDDEN)

               LV3 = loadImg("LV.png")
               LV3_aux = C_car.create_image(225, 500, image=LV3, anchor=NW, state=HIDDEN)

               global LR1_aux, LR2_aux, LR3_aux
               LR1 = loadImg("LR.png")
               LR1_aux = C_car.create_image(600, 500, image=LR1, anchor=NW, state=HIDDEN)

               LR2 = loadImg("LR.png")
               LR2_aux = C_car.create_image(675, 500, image=LR2, anchor=NW, state=HIDDEN)

               LR3 = loadImg("LR.png")
               LR3_aux = C_car.create_image(750, 500, image=LR3, anchor=NW, state=HIDDEN)
              
               #Imagen para cuando el carro se mueve hacia la izquierda
               global L_arrow
               FL = loadImg("L.png")
               L_arrow = C_car.create_image(0, 0, image=FL, anchor=NW, state=HIDDEN)

               #Imagen para cuando el carro se mueve hacia la derecha
               global R_arrow
               FR = loadImg("R.png")
               R_arrow = C_car.create_image(0, 0, image=FR, anchor=NW, state=HIDDEN)
               
               #NIVEL DE BATERIA
               global Battery
               Battery = C_car.create_text(1108, 155, font=("Agency", 14), anchor=NW, fill="white", text="")

               #BOTONES
               #Botón para regresar a la ventana Test Drive y seleccionar otro piloto o bien para regresar a la
               #ventana principal
               Btn_back = Button(car, text="TERMINAR TEST", command=back, bg="#cb3234", fg="white")
               Btn_back.place(x=10, y=10)

               #Botón para la celebración del piloto
               Btn_back = Button(car, text="CELEBRACIÓN", command=celebration, bg="#cb3234", fg="white")
               Btn_back.place(x=1065, y=455)

               #Botón para el movimiento especial(Katarsys) del carro
               Btn_back = Button(car, text="MOV. ESPECIAL", command=special_movement, bg="#cb3234", fg="white")
               Btn_back.place(x=1065, y=480)

               #Botón para el movimiento especial(Katarsys) del carro
               Btn_back = Button(car, text="CIRCLE D", command=circle_right, bg="#cb3234", fg="white")
               Btn_back.place(x=1065, y=495)

               #Botón para el movimiento especial(Katarsys) del carro
               Btn_back = Button(car, text="CIRCLE L", command=circle_left, bg="#cb3234", fg="white")
               Btn_back.place(x=1065, y=510)

               #Botón para el movimiento especial(Katarsys) del carro
               Btn_back = Button(car, text="ZIG ZAG", command=zigzag, bg="#cb3234", fg="white")
               Btn_back.place(x=1065, y=525)

               #Botón para el movimiento especial(Katarsys) del carro
               Btn_back = Button(car, text="INFINITE", command=infinite, bg="#cb3234", fg="white")
               Btn_back.place(x=1065, y=550)

               time.sleep(100000)

           #Creando el cliente para NodeMCU
           myCar = NodeMCU()
           myCar.start()

           def get_log():
               #Descripción: Función que sirve para captar el comando enviado y recibido

               #Entradas: Ninguna
               #Salida: Captura de la respuesta del comando Sense para el nivel de batería en pantalla y el tiempo(día y noche)
               #Restricción: Ninguna 
               global Sense, Lista, Bat
               #Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
               indice = 0
               while(myCar.loop):
                   while(indice < len(myCar.log)):
                       #Captura del comando enviado al carro
                       mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
                       try:
                           #Captura del mensaje recibido 
                           mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
                           #Se almacena en una variable el mensaje recibido al enviar cualquier comando
                           Sense = mnsRecv
                           #Si el mensaje recibido tiene una longitud de 27, significa que ese mensaje corresponde
                           #a la respuesta del comando Sense que se envia cada dos segundos para no sobrecargar
                           #la comunicación con el carro
                           if len(Sense)>=27:
                               Bat = True
                               sense_aux(Sense)
                       except:
                           pass

                       indice+=1
                   time.sleep(0.200)
                   
           def sense():
               #Descripción: Función recursiva que cada dos segundos manda el comando Sense para estar constantemente
               #chequeando el estado del carro, el nivel de carga de la batería y el tiempo(día y noche)

               #Entrada:Ninguna
               #Salida: Comando Sense al NodeMCU
               #Restricción: Ninguna
               mns = "sense;"#Comando para ver chequear el nivel de bateria y el estado de sensor de luz
               myCar.send(mns)
               time.sleep(2)
               #Llamada recursiva
               return sense()

           def sense_aux(Sense):
               #Descripción: Función que dependiendo del valor de lectura del sensor de luz, pone una imagen representativa
               #en la interfaz del Drive Car

               #Entrada: Respuesta del comando sense
               #Salida: Cambio de imagen principal para la interfaz dependiendo del valor de lectura del sensor de luz
               #Restricción: Ninguna

               #Imágenes principales para la interfaz del Drive Car
               global Car_Background1, Car_Background2

               #Si el valor de lectura del sensor es uno, significa que es de día y por lo tanto en la interfaz se coloca
               #la imagen que represente que es de día
               if buscar(Sense)== "1":
                   C_car.itemconfig(Car_Background1, state=NORMAL)
                   C_car.itemconfig(Car_Background2, state=HIDDEN)
                   drive_car.update()

               #Si el valor de lectura del sensor es cero, significa que es de noche y por lo tanto en la interfaz se coloca
               #la imagen que represente que es de noche
               elif buscar(Sense) == "0":
                   C_car.itemconfig(Car_Background1, state=HIDDEN)
                   C_car.itemconfig(Car_Background2, state=NORMAL)
                   drive_car.update()

               else:
                   pass

           def buscar(Sense):
               #Descripción: Función encargada de buscar el valor de lectura(1 o 0) del sensor de luz

               #Entrada: Respuesta del comando Sense
               #Salida: 1 o 0 dependiendo del valor actual del sensor de luz
               #Restricción: Ninguna
               if Sense[-1] == "1":
                   return "1"

               elif Sense[-1] == "0":
                   return "0"

               else:
                   #Llamada recursiva
                   return buscar(Sense[:-1])

           def battery():
               #Descripción: Función que muestra en la interfaz del Drive Car el nivel de bateria actual del carro

               #Entrada: Ninguna
               #Salida: Porcentaje del nivel de batería en la interfaz de acuerdo al valor leido en la respuesta del
               #comando Sense y escritura del estado del carro en el txt de acuerdo del mismo nivel leido
               #Restricción: Ninguna
               
               #Variables globales para condicionar el nivel de batería sobre la interfaz 
               global Bat, Sense, Lista
               #Si el comando que ha recibido el NodeMCU es el del Sense, se realiza el chequeo del nivel de batería actual
               #del carro para ponerlo en la interfaz, se abre y se escribe en el txt el estado actual del carro de acuerdo
               #al mismo nivel de la batería
               if Bat == True:
                   #Se abre el txt para escribir el estado del carro(Disponible o Descargado) de acuerdo al nivel de batería
                   #actual del carro mientras se realiza el Drive Car
                   Car_state = open("Car state.txt","r+")
                   Car_state.seek(0)
                   try:
                       #Se llama a la función para obtener el nivel de batería actual del carro
                       L_Bat = level_bat(Sense[6:], Lista, "")
                       #Si el nivel de batería actual del carro es 0, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 0, en el txt se escribe que el estado actual del carro es Descargado
                       if L_Bat == "0":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Descargado")
                           Car_state.close()
                           
                       #Si el nivel de batería actual del carro es 10, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 10, en el txt se escribe que el estado actual del carro es Descargado
                       elif L_Bat == "10":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Descargado")
                           Car_state.close()
                           
                       #Si el nivel de batería actual del carro es 20, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 20, en el txt se escribe que el estado actual del carro es Descargado
                       elif L_Bat == "20":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Descargado")
                           Car_state.close()
                           
                       #Si el nivel de batería actual del carro es 30, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 30, en el txt se escribe que el estado actual del carro es Descargado
                       elif L_Bat == "30":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Descargado")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 40, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 0, en el txt se escribe que el estado actual del carro es Descargado
                       elif L_Bat == "40":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Descargado")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 50, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 50, en el txt se escribe que el estado actual del carro es Descargado
                       elif L_Bat == "50":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Descargado")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 60, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 60, en el txt se escribe que el estado actual del carro es Disponible
                       elif L_Bat == "60":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Disponible")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 70, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 70, en el txt se escribe que el estado actual del carro es Disponible
                       elif L_Bat == "70":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Disponible")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 80, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 80, en el txt se escribe que el estado actual del carro es Disponible
                       elif L_Bat == "80":
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Disponible")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 90, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 90, en el txt se escribe que el estado actual del carro es Disponible
                       elif L_Bat == "90":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
                           Car_state.write("Disponible")
                           Car_state.close()

                       #Si el nivel de batería actual del carro es 100, se pondrá ese mismo porcentaje en la interfaz del Drive Car
                       #Como el nivel de batería es 100, en el txt se escribe que el estado actual del carro es Disponible
                       elif L_Bat == "100":
                           print(L_Bat)
                           C_car.itemconfig(Battery, text=L_Bat + "%")
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
               #Llamada recursiva
               return battery()

           def level_bat(Sense, Lista, L_Bat):
               #Descripción: Función recursiva que recorre la respuesta del comando Sense en busca del nivel de batería que este mismo
               #retorna

               #Entradas: Respuesta del comando Sense, Lista para comparar strings numéricos(posibles niveles de batería)
               #y una variable para almacenar el nivel de batería del sensor
               #Salida: Variable con el nivel de bateria actual del carro
               #Restricción: Ninguna

               #Condición de finalización
               if Sense[0]==";":
                   return L_Bat

               #Si se encuentra un string numérico este forma parte del nivel de batería del carro y se almacena en la variable
               #anteriormente mencionada
               elif buscar_level(Sense[0],Lista)==True:
                   L_Bat = L_Bat + Sense[0]
                   return level_bat(Sense[1:], Lista, L_Bat)

               #Si no se encuentra ninguna string numérico, simplemente se vuelve a llamar a la función para analizar el siguiente
               #elemento de la respuesta almacenada en la variable Sense
               else:
                   return level_bat(Sense[1:], Lista, L_Bat)

           def buscar_level(Ele, Lista):
               #Descripción: Función recursiva encargada de encontrar strings numéricos pertenecientes al nivel de la batería que
               #contiene la variable Sense

               #Entradas: String de la variable Sense y lista de todos los posibles strings numéricos pertenecientes al nivel de la batería
               #Salida: True o False dependiendo si el String pertenece o no a uno de los strings numéricos que contiene la lista
               #Restriccioón: Ninguna

               #Condiciónn de finalización
               if Lista == []:
                   return False

               #Si el string específico de la variable sense está en la lista, se retorna True
               elif Ele == Lista[0]:
                   return True

               #Si el string específico de la variable sense no está en la lista, se retorna False
               else:
                   return buscar_level(Ele, Lista[1:])
                            
           def lights(event):
               #Descripción: Función encargada del encendido y apagado de las luces delanteras traseras y direccionales del carro
               #tanto la acción física sobre el carro como en la interfaz

               #Entrada: Tecla específica para cada luz
               #Salida: Encendido y apagado de las luces del carro
               #Restricción: Ninguna

               #Variables globales para el manejo del carro en la parte física y en la interfaz
               global Lfront, Lback, Lleft, Lright, Front_img, Back_img, Left_img, Right_img
               #Si se presiona la tecla f se podrán encender o apagar las luces frontales del carro, esa acción también se reflejaran
               #en la interfaz del Drive Car
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
                       
               #Si se presiona la tecla b se podrán encender o apagar las luces traseras del carro, esa acción también se reflejaran
               #en la interfaz del Drive Car 
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

               #Si se presiona la tecla l se podrá encender o apagar las luz direccional izquierda del carro, esa acción también se reflejará
               #en la interfaz del Drive Car
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

               #Si se presiona la tecla r se podrá encender o apagar las luz direccional izquierda del carro, esa acción también se reflejará
               #en la interfaz del Drive Car
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
               #Descripción: Función encargada de mover el carro hacia adelante tanto físicamente como en la interfaz

               #Entrada: Flecha hacia arriba del teclado
               #Salida: Movimiento del carro hacia adelante, imagén que refleja que el carro se está moviendo hacia adelante,
               #así como la actualización inmediata de la aceleración del carro en el PWM en la interfaz
               #Restricción: No se puede sobrepasar el PWM de 1023

               #Variables globales para el movimiento del carro
               global Forward, Back, L_PWM_aux, F_arrow, B_arrow, Stoped
               Back = -700
               C_car.itemconfig(F_arrow, state=NORMAL)
               C_car.itemconfig(B_arrow, state=HIDDEN)
               C_car.itemconfig(LR1_aux, state=HIDDEN)
               C_car.itemconfig(LR2_aux, state=HIDDEN)
               C_car.itemconfig(LR3_aux, state=HIDDEN)
               #Si el carro aún no alcanza el máximo valor del pwm permitido(1023) se aumenta en uno el valor del mismo, ese cambio se
               #se refleja en la aceleración del carro y en el pwm de la interfaz
               mns = "lb:0;"
               myCar.send(mns)
               if Forward <1023:
                   Forward+=1
                   if Forward <=800:
                       C_car.itemconfig(LV1_aux, state=NORMAL)
                   elif Forward <=900:
                       C_car.itemconfig(LV2_aux, state=NORMAL)
                   else:
                       C_car.itemconfig(LV3_aux, state=NORMAL)
                   mns = "pwm:" + str(Forward) + ";"
                   print(mns)
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Forward))
                   time.sleep(0.001)

               #Cuando el carro alcanza el valor máximo de pwm permitido, apesar de que el usuario siga presionando para acelerar, no se
               #se reflejará ningún cambio en la aceleración del carro ni en el pwm de la interfaz 
               else:
                   Forward = 1023
                   mns = "pwm:" + str(Forward) + ";"
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Forward))
                   time.sleep(0.001)

           def move_back(event):
               #Descripción: Función encargada de mover el carro hacia atras tanto físicamente como en la interfaz

               #Entrada: Flecha hacia abajo del teclado
               #Salida: Movimiento del carro hacia atras, imagén que refleja que el carro se está moviendo hacia atras,
               #así como la actualización inmediata de la aceleración del carro en el PWM en la interfaz
               #Restricción: No se puede sobrepasar el PWM de -1023

               #Variables globales para el movimiento del carro
               global Forward, Back, L_PWM_aux, F_arrow, B_arrow, Stoped
               Forward = 700
               C_car.itemconfig(F_arrow, state=HIDDEN)
               C_car.itemconfig(B_arrow, state=NORMAL)
               C_car.itemconfig(LV1_aux, state=HIDDEN)
               C_car.itemconfig(LV2_aux, state=HIDDEN)
               C_car.itemconfig(LV3_aux, state=HIDDEN)
               #Si el carro aún no alcanza el máximo valor del pwm permitido(-1023) se aumenta en uno el valor del mismo, ese cambio se
               #se refleja en la aceleración del carro y en el pwm de la interfaz
               mns = "lb:1;"
               myCar.send(mns)
               if Back>-1023:
                   Back-=1
                   if -800<=Back<=-700:
                       C_car.itemconfig(LR1_aux, state=NORMAL)
                   elif -900<Back<-800:
                       C_car.itemconfig(LR2_aux, state=NORMAL)
                   else:
                       C_car.itemconfig(LR3_aux, state=NORMAL)
                   mns = "pwm:" + str(Back) + ";"
                   print(mns)
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Back))
                   time.sleep(0.001)

               #Cuando el carro alcanza el valor máximo de pwm permitido, apesar de que el usuario siga presionando para acelerar, no se
               #se reflejará ningún cambio en la aceleración del carro ni en el pwm de la interfaz 
               else:
                   Back = -1023
                   mns = "pwm:" + str(Back) + ";"
                   myCar.send(mns)
                   C_car.itemconfig(L_PWM_aux, text=str(Back))
                   time.sleep(0.001)

           def stop(event):
               #Descripción: Función encargada de detener por completo el carro

               #Entrada: Tecla p de parar
               #Salida: El carro deja de moverse y desaparecen las direccionales y las flechas de movimiento hacia adelante y atras
               #del carro en la interfaz del Drive Car
               #Restricción: Ninguna

               #Variables globales para detener el movimiento del carro
               global Forward, Back, L_PWM_aux, F_arrow, B_arrow, L_arrow, R_arrow, Stoped
               #Se restablecen los valores inciales del movimiento del carro ya sea hacia adelante o hacia atras
               Forward = 700
               Back = -700
               Velocidad = 0
               #Desaparecen todas las imágenes de movimiento y luces en la interfaz del Drive Car 
               C_car.itemconfig(F_arrow, state=HIDDEN)
               C_car.itemconfig(B_arrow, state=HIDDEN)
               C_car.itemconfig(R_arrow, state=HIDDEN)
               C_car.itemconfig(L_arrow, state=HIDDEN)
               C_car.itemconfig(LR1_aux, state=HIDDEN)
               C_car.itemconfig(LR2_aux, state=HIDDEN)
               C_car.itemconfig(LR3_aux, state=HIDDEN)
               C_car.itemconfig(LV1_aux, state=HIDDEN)
               C_car.itemconfig(LV2_aux, state=HIDDEN)
               C_car.itemconfig(LV3_aux, state=HIDDEN)
               #Se manda el comando para detener por completo el carro
               mns = "pwm:" + str(Velocidad) + ";"
               myCar.send(mns)
               #Se pone en la interfaz un PWM igual cero indicando que el carro está completamente detenido
               C_car.itemconfig(L_PWM_aux, text=str(Velocidad))

           def move_left(event):
               #Descripción: Función encargada de mover el carro hacia la izquierda físicamente y que pone sobre
               #la interfaz un flecha indicando tal efecto

               #Entrada: Flecha hacia la izquierda del Teclado
               #Salida: Mvimiento del carro hacia la izquierda y flecha hacia la izquierda sobre la interfaz del Drive Car
               #Restricción: Ninguna
               global L_arrow, R_arrow
               C_car.itemconfig(R_arrow, state=HIDDEN)
               C_car.itemconfig(L_arrow, state=NORMAL)
               #Se inicia el Thread para encender y apagar la luz direccional izquierda para dar el efecto de que
               #se ha decidido girar hacia la izquierda
               p=Thread(target=move_left_aux,args=()).start()
               #Se envia el comando para girar el carro hacia la izquierda
               mns = "dir:-1;"
               myCar.send(mns)

           def move_left_aux():
               #Descripción: Función que enciende y apaga las luz direccional izquierda dando el efecto de que el piloto
               #ha decidido girar hacia la izquierda

               #Entrada: Ninguna
               #Salidas: Efecto de giro hacia la izquierda con la luz direccional
               #Restricción: Ninguna

               #Se encienden y apagan las luz direccional izquierda tres veces para lograr tal efecto
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
               #Descripción: Función encargada de mover el carro hacia la izquierda físicamente y que pone sobre
               #la interfaz un flecha indicando tal efecto

               #Entrada: Flecha hacia la derecha del Teclado
               #Salida: Mvimiento del carro hacia la derecha y flecha hacia la derecha sobre la interfaz del Drive Car
               #Restricción: Ninguna
               global L_arror, R_arrow
               C_car.itemconfig(R_arrow, state=NORMAL)
               C_car.itemconfig(L_arrow, state=HIDDEN)
               #Se inicia el Thread para encender y apagar la luz direccional derecha para dar el efecto de que
               #se ha decidido girar hacia la derecha
               p=Thread(target=move_right_aux,args=()).start()
               #Se envia el comando para girar el carro hacia la derecha
               mns = "dir:1;"
               myCar.send(mns)

           def move_right_aux():
               #Descripción: Función que enciende y apaga las luz direccional derecha dando el efecto de que el piloto
               #ha decidido girar hacia la derecha

               #Entrada: Ninguna
               #Salidas: Efecto de giro hacia la derecah con la luz direccional
               #Restricción: Ninguna

               #Se encienden y apagan las luz direccional derecha tres veces para lograr tal efecto
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
               #Descripción: Función para que el carro se mueva en linea recta

               #Entrada: Tecla "d" del Teclado
               #Salida: Movimiento recto del carro, desaparición de las flechas direccionales sobre la interfaz
               #Restricción: Ninguna

               #Desaparecen las luces direccionales
               C_car.itemconfig(R_arrow, state=HIDDEN)
               C_car.itemconfig(L_arrow, state=HIDDEN)
               #Se envia el comando para que el carro se mueva en línea recta
               mns = "dir:0;"
               myCar.send(mns)

           def special_movement():
               #Descripción: Función que realiza el comando especial creado en la primera parte del proyecto

               #Entrada: Ninguna
               #Salida: Movimiento especial(Katarsys) del carro
               #Restricción: Ninguna

               #Se envia el comando especial del carro al NodeMCU para que este lo ejecute
               mns = "katarsys:;"
               myCar.send(mns)

           def circle_right():
               #Descripción: Función que realiza el comando especial creado en la primera parte del proyecto

               #Entrada: Ninguna
               #Salida: Movimiento especial(Katarsys) del carro
               #Restricción: Ninguna

               #Se envia el comando especial del carro al NodeMCU para que este lo ejecute
               mns = "circle:1;"
               myCar.send(mns)

           def circle_left():
               #Descripción: Función que realiza el comando especial creado en la primera parte del proyecto

               #Entrada: Ninguna
               #Salida: Movimiento especial(Katarsys) del carro
               #Restricción: Ninguna

               #Se envia el comando especial del carro al NodeMCU para que este lo ejecute
               mns = "circle:-1;"
               myCar.send(mns)

           def infinite():
               #Descripción: Función que realiza el comando especial creado en la primera parte del proyecto

               #Entrada: Ninguna
               #Salida: Movimiento especial(Katarsys) del carro
               #Restricción: Ninguna

               #Se envia el comando especial del carro al NodeMCU para que este lo ejecute
               mns = "infinite:;"
               myCar.send(mns)

           def zigzag():
               #Descripción: Función que realiza el comando especial creado en la primera parte del proyecto

               #Entrada: Ninguna
               #Salida: Movimiento especial(Katarsys) del carro
               #Restricción: Ninguna

               #Se envia el comando especial del carro al NodeMCU para que este lo ejecute
               mns = "zigzag:;"
               myCar.send(mns)

           def celebration():
               #Descripción: Función que inicia el Thread para realizar la celebración característica del piloto seleccionado
               #por el usuario para realizar el Drive Car

               #Entrada: Ninguna
               #Salida: Inicio del Thread de celebración del piloto
               #Restricción: Ninguna

               #Se inicia el Thread para la celebración del piloto en el Drive Car
               p=Thread(target=celebration_aux,args=()).start()

           def celebration_aux():
               #Descripción: Función que de acuerdo a la selección del piloto que hizo el usario para poder realizar el
               #Drive Car, asocia la celebración específica de cada piloto, la celebración de cada piloto es única y se genera
               #completamente en Python

               #Entrada: Ninguna
               #Salida: Celebración de acuerdo al piloto que el usuario haya seleccionado
               #Restricción : Ninguna
        
               global Piloto
               #Si el piloto que el usuario seleccionó para realizar el Drive Car es el Piloto A, se habilita la celebración del mismo
               if Piloto[0:9]=="2019A.png":
                   print ("Celebración Piloto A")
                   #Luz izquierda encendida
                   myCar.send("lf:1;")
                   time.sleep(0.5)
                   #Luz izuierda apagada
                   myCar.send("lf:0;")
                   time.sleep(0.5)
                   #Luz izuierda encendida
                   myCar.send("lf:1;")
                   time.sleep(0.5)
                   #Luz izuierda apagada
                   myCar.send("lf:0;")
                   time.sleep(0.5)
                   #Movimiento hacia adelante por dos segundos
                   myCar.send("pwm:750;")
                   time.sleep(2)
                   #Movimiento hacia atras por dos segundos
                   myCar.send("pwm:-1000;")
                   time.sleep(2)
                   #El carro se detiene
                   myCar.send("pwm:0;")

               #Si el piloto que el usuario seleccionó para realizar el Drive Car es el Piloto A, se habilita la celebración del mismo
               else:
                   print("Celebración Piloto B")
                   #Luz direccional derecha encendida y movimiento hacia la derecha
                   myCar.send("lr:1;")
                   myCar.send("dir:1;")
                   time.sleep(2)
                   #Luz direccional derecha apagada, luz direccional izquierda encendida y movimiento hacia la izquierda
                   myCar.send("lr:0;")
                   myCar.send("ll:1;")
                   myCar.send("dir:-1;")
                   time.sleep(2)
                   #Luz direccional izquierda apagada, movimiento hacia adelante por dos segundos con giro hacia la derecha
                   myCar.send("ll:0;")
                   myCar.send("pwm:900;")
                   myCar.send("dir:1;")
                   time.sleep(2)
                   #Giro hacia la izquierda
                   myCar.send("dir:-1;")
                   time.sleep(2)
                   #Giro hacia la derecha
                   myCar.send("dir:1;")
                   time.sleep(2)
                   #Giro hacia la izquierda
                   myCar.send("dir:-1;")
                   time.sleep(2)
                   #El carro deja de moverse
                   myCar.send("pwm:0;")
                   
               
           def send (event):
               """                      Instituto Tecnológico de Costa Rica

                          Ingeniería en Computadores


                          
Curso: Introducción a la Programación
Grupo: 2
Profesor: Ing. Milton Villegas Lemus
Lenguaje: Python 3.7.1
Versión: v1.0
País de producción: Costa Rica
Fecha última modificación: 3/6/2019
Autor: Emanuel Antonio Marín Gutiérrez
Carné: 2019067500

Programa: send()
Descripción: Función encargada de enviar todos los comandos de luces, movimientos y estado del carro al NodeMCU para ser
#ejecutador por el mismo y actuar físicamente sobre el carro.

Entrada: Ninguna
Salida: Comandos para el encendido de las luces, el movimiento del carro y el estado del mismo
Restricciones: No olvidar que cada comando debe finalizar con punto y coma"""

               #Se obtiene el mensaje que se escribe en el Entry
               mns = str(E_Command.get())
               #Se valida que el comando este bien escrito
               if(len(mns)>0 and mns[-1] == ";"):
                   E_Command.delete(0, 'end')
                   #Se envia el comando al NodeMCU
                   myCar.send(mns)
               else:
                   messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

           def back():
               #Descripción: Función para regresar a la ventana del Test Drive

               #Entrada: Ninguna
               #Salida: Se vacía la variable que almacena el Piloto seleccionado por el usuario
               #Restricciones:
               global Piloto
               Piloto = ""
               car.destroy()#Se destruye la ventana del Drive Car
               test.destroy()#Se destruye la ventana del Test Drive
               test_drive()


           #TECLAS ASOCIADAS A LOS DIFERENTES COMANDOS DEL CARRO
           car.bind("<Up>", move_forward)
           car.bind("<Down>", move_back)
           car.bind("p", stop)
           car.bind("<Left>", move_left)
           car.bind("<Right>", move_right)
           car.bind("d", move_direct)
           car.bind("<Key>",lights)


           #Threads para la animación de la interfaz, para la respuesta de cada comando enviado al NodeMCU, para el
           #chequeo del nivel de la batería y el tiempo(día y noche) 
           p=Thread(target=intro,args=()).start()
           p = Thread(target=get_log).start()
           p = Thread(target=sense).start()
           p = Thread(target=battery).start()
           main.mainloop()

       def back():
           #Descripción: Función para retornar a la ventana principal de la interfaz

           #Entrada: Ninguna
           #Salida: Se retorna a la ventana principal
           #Restricción: Ninguna
           test.destroy()#Se destruye la ventana de Test Drive
           main.destroy()#Se destruye la ventana principal
           main_window()#Se vuelve a cargar la ventana principal de la interfaz


       #BOTONES
       #Botón para retornar a la ventana principal
       Btn_back = Button(test, text="ATRAS", command=back, bg="#cb3234", fg="white")
       Btn_back.place(x=10,y=595)

       #Botón para seleccionar a uno de los dos pilotos de la Temporada actual
       Btn_pilot = Button(test, text="Seleccionar Piloto", command=select_pilot, bg="#cb3234", fg="white")
       Btn_pilot.place(x=50,y=50)

       #Botón para iniciar el Drive Car
       Start=loadImg("S1.1.png")
       Btn_start = Button(C_test,command=drive_car, fg="black", bg="light blue")
       Btn_start.place(x=380,y=555)
       Btn_start.config(image=Start)
       
       main.mainloop()    

    print("Working")
    main.mainloop()

main_window()
