about ="""
Instituto Tecnológico de Costa Rica
Ingenieria en Computadores

Profesor: Milton Villegas Lemus
Taller de programación
Proyecto T-Rex Runner v2(Dragon Ball)

Autor: Emanuel Marin Gutiérrez
Carné: 2019067500

Lenguaje: Python 3.7.1
Fecha de emisión: 8/4/2019
Versión: 1.0.0"""

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
                        
#Función para cargar imágenes
#Código tomado de ejemplo de Santiago
def loadImg(name):
    ruta=os.path.join("imgs",name)
    imagen=PhotoImage(file=ruta)
    return imagen

#Variables globales
#Niveles
global select_level, level, difficulty
select_level=False
level="Level-1"
difficulty=5

#Altos puntajes
global player, contenido, points, game_time
player=""
contenido=""
points=-1

#Colisiones
global flag, c_posx, c_posy, obs1_posx, obs1_posy, obs2_posx, obs2_posy, obs3_posx, obs3_posy
flag=False
c_posx=85
c_posy=400
obs1_posx=890
obs1_posy=402
obs2_posx=890
obs2_posy=375
obs3_posx=890
obs3_posy=290

#           _____________________________________________________
#__________/ VENTANA PRINCIPAL

#Creación ventana principal y sus atributos
main = Tk()
main.title("Proyecto")
main.minsize(800,600)
main.resizable(width=NO,height=NO)

#Canvas de la ventana principal
C_main = Canvas(main, width=800, height=600, bg="white")
C_main.place(x=0, y=0)

#Fondo ventana principal 
#Código tomado como ejemplo de Santiago
Background = loadImg("Fondo1.gif")
Game_Background = Label(C_main,bg="white")
Game_Background.place(x=0, y=0)
Game_Background.config(image=Background)

#Label asociado a los botones de dificultad del juego
L_difficulty = Label(C_main, text="Dificultad:", font=("Agency FB",14), bg="light blue", fg="black")
L_difficulty.place(x=65, y=432)

#Label y entry para cargar el nombre en la ventana de juego
#Código tomado como ejemplo de Santiago
L_name = Label(C_main, text="Ingrese su nombre:", font=('Agency FB',14), bg="light blue", fg="black")
L_name.place(x=10, y=400)
E_name = Entry(C_main, width=20, font=('Agency FB',14), bg="white", fg="black")
E_name.place(x=135, y=400)

#Funciones Niveles de dficultad (cada una asociada a un botón)
#Si el usuario no selecciona ningún nivel de dificultad, el juego tomará como valor predetreminado 
#la dificultad del nivel 1
#Una vez seleccionado el nivel de dificultad no se podrá cambiar hasta despues de haber completado 
#al menos una partida
def easy():#Nivel 1
    global select_level, level, difficulty
    if select_level==False:
        level=level
        difficulty=difficulty
        select_level=True
    else:
        difficulty=difficulty

def medium():#Nivel 2
    global select_level, level, difficulty 
    if select_level==False:
        level="Level-2"
        difficulty=difficulty+5
        select_level=True
    else:
        difficulty=difficulty

def hard():#Nivel 3
    global select_level, level, difficulty
    if select_level==False:
        level="Level-3"
        difficulty=difficulty+10
        select_level=True
    else:
        difficulty=difficulty

#Funciones música de fondo, ambas asociadas a una imagen de reproducir o silenciar
#Código tomado como ejemplo de Santiago
def song_intro():#Codigo sugerido por Alejandro Vasquez, reproduce una canción indefinidamente
    winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)

def mute():
    winsound.PlaySound(None, winsound.SND_ASYNC)

#Funciones cierre de ventana
def confirm_exit1():
    if messagebox.askokcancel("Salir", "¿Estás seguro que quieres salir?"):
        main.destroy()

def confirm_exit2(event):
    if messagebox.askokcancel("Salir", "¿Estás seguro que quieres salir?"):
        main.destroy()

#Hilo de reproducción de música 
p=Thread(target=song_intro,args=()).start()

#           _____________________________________________________
#__________/ VENTANA JUEGO
def game_window(player_name):
    #Esconder ventana principal
    main.withdraw()
    #Ventana de Juego y sus atributos
    game=Toplevel()
    game.title("Dragon Ball")
    game.minsize(800,500)
    game.resizable(width=NO, height=NO)

    #Canvas de la ventana de juego
    c_game = Canvas(game, width=800, height=500, bg="#c7fefa")
    c_game.place(x=0,y=0)
    c_game.pack()

    #Label de tiempo
    L_time = Label(c_game, text="Time: "+"00.00", font=("Agency FB",16), fg="black", bg="#c7fefa")
    L_time.place(x=10,y=46)

    global player
    player=player_name
    #Se define como global ya que se utilizará en la ventana de altos puntajes
    #Label de nombre
    L_name = Label(c_game, text="Player: "+ player_name ,font=("Agency FB",18), fg="black", bg="#c7fefa")
    L_name.place(x=10,y=10)

    global points
    #Se define como global ya que su valor cambiará de acuerdo al tiempo transcurrido y los obstáculos esquivados
    #Label de puntaje obtenido
    L_score = Label(c_game, text="Score: "+"0", font=("Agency FB",16), fg="black", bg="#c7fefa")
    L_score.place(x=10,y=78)
    L_score.config(text="Score: "+str(points))

    global level
    #Label de Nivel, especifica el nivel en pantalla
    L_level = Label(c_game, text=level, font=("Agency FB",16), fg="black", bg="#c7fefa")
    L_level.place(x=756, y=10)
  	
    #Imágenes
    Fondo_juego = PhotoImage(file="C:\\Users\\Emanuel\\Desktop\\Proyecto 1\\imgs\\Edicion Fondos.gif")
    Fondo = c_game.create_image(0,0, anchor=NW, image=Fondo_juego)

    Character = PhotoImage(file="Goku_up.png")
    P_Goku = c_game.create_image(35,400, anchor=NW, image=Character)
    
    #Código tomado como ejemplo de Santiago
    Obstaculo1=loadImg("Obs1.png")
    Obs1=Label(c_game, bg="light blue")
    Obs1.place(x=890,y=402)
    Obs1.config(image=Obstaculo1)

    Obstaculo2=loadImg("Obs2.png")
    Obs2=Label(c_game, bg="#c7fefa")
    Obs2.place(x=890,y=385)
    Obs2.config(image=Obstaculo2)

    Obstaculo3=loadImg("Obs3.png")
    Obs3=Label(c_game, bg="light blue")
    Obs3.place(x=890, y=350)
    Obs3.config(image=Obstaculo3)

    #Movimiento del fondo
    def move_background(Fondo,x,y):
        if move_background_aux(Fondo,x,y)==True:
            return move_background(Fondo,x,y)

    def move_background_aux(Fondo,x,y):
        global flag
        if x>=-4800:
            if flag==False:
                c_game.move(Fondo,-difficulty,0)
                game.update()
                time.sleep(0.01)
                return move_background_aux(Fondo,x-difficulty,y)
            else: 
               print("parar")
        else:
            return True

    #Función de tiempo
    def tiempo(L_score,cs,ds,us):
        global flag, points, game_time
        if flag==False:
            if us<10:
                L_time.config(text="Time: "+"0"+str(cs)+":"+str(ds)+str(us))
                points=points+1#Se suma un punto por cada segundo que trascurra
                L_score.config(text="Score: "+str(points))#El puntaje sumado se muestra en pantalla
                game_time=str(cs)+":"+str(ds)+str(us)
                game.update()
                time.sleep(1)
                return tiempo(L_score,cs,ds,us+1)
            else:
                if ds<5:
                    us=0
                    ds=ds+1
                    L_time.config(text="Time: "+"0"+str(cs)+":"+str(ds)+str(us))
                    points=points+1
                    L_score.config(text="Score: "+str(points))
                    game_time=str(cs)+":"+str(ds)+str(us)
                    game.update()
                    time.sleep(1)
                    return tiempo(L_score,cs,ds,us+1)
                else:
                    us=0
                    ds=0
                    cs=cs+1
                    L_time.config(text="Time: ""0"+str(cs)+":"+str(ds)+str(us))
                    points=points+1
                    L_score.config(text="Score: "+str(points))
                    game_time=str(cs)+":"+str(ds)+str(us)
                    game.update()
                    time.sleep(1)
                    return tiempo(L_score,cs,ds,us+1)
        else:
            L_score.config(text="Score: "+str(points))
            

    #Hilo para saltar
    def start(event):#Tecla asociada al salto (flecha arriba) 
    	return start_jump(P_Goku,35,400) 

    def start_jump(P_Goku,x,y):
        p=Thread(target=move_up, args=(P_Goku,x,y,)).start()

    def move_up(P_Goku,x,y):
        global c_posx, c_posy
        if y==200:
            c_posy=y
            return move_down(P_Goku,x,y)
        else:
            x=x
            y=y-5
            c_posx=x
            c_posy=y
            c_game.move(P_Goku,0,-5)
            game.update()
            time.sleep(0.001)
            return move_up(P_Goku,x,y)

    def move_down(P_Goku,x,y):
        global c_posx, c_posy
        if y==400:
        	print ("Fin") 
        else:
            x=x
            y=y+5
            c_posx=x
            c_posy=y
            c_game.move(P_Goku,0,5)
            game.update()
            time.sleep(0.001)
            return move_down(P_Goku,x,y)

    def start2(event2):#Tecla asociada al salto (flecha abajo)
        Character2 = PhotoImage(file="Goku_down.png")
        P_Goku2 = c_game.create_image(35,420, anchor=NW, image=Character2)
        counter=0
        return start_flight(P_Goku,P_Goku2,35,420,counter)

    def start_flight(P_Goku,P_Goku2,x,y,counter):
        p=Thread(target=start_flight_aux(P_Goku,P_Goku2,x,y,counter),args=()).start()

    def start_flight_aux(P_Goku,P_Goku2,x,y,counter):
        if counter==75:
            c_game.move(P_Goku,7500,0)
            c_game.move(P_Goku2,-100,420)
        else:
            c_game.move(P_Goku,-100,0)
            c_game.move(P_Goku2,0,0)
            game.update()
            time.sleep(0.01)
            return start_flight_aux(P_Goku,P_Goku2,x,y,counter+1)

    #Obstáculos  
    #Código sugerido por Alejandro Vasquez     
    def obstacles():#Función para la aparición aleatoria de obstaculos
        global flag
        if flag==False:
            posy=[290,350,370]
            Obstacle_1 = Thread(target=move_obs1_aux,args=(Obs1,890,402,))
            Obstacle_2 = Thread(target=move_obs2_aux,args=(Obs2,890,385,))
            Obstacle_3 = Thread(target=move_obs3_aux,args=(Obs3,890,random.choice(posy)))
            List_obstacles = [Obstacle_1, Obstacle_2, Obstacle_3]
            random.choice(List_obstacles).start()
            time.sleep(random.randint(5,8))
            return obstacles()
        else:
            print("No more obstaculos")

    #Movimiento y detección de colisión de cada obstáculo
    def move_obs1_aux(Obs1,x,y):#Función que mueve al primer obstáculo
        global points, obs1_posx, obs1_posy, flag, select_level, difficulty, player
        if x==-200:
            obs1_posx=x
            points=points+2
            L_score.config(text="Score: "+str(points))
            print("Fin Nave")
        else:
            x=x-5
            y=y
            obs1_posx=x
            obs1_posy=y
            Obs1.place(x=x, y=y)
            if colision_obs1(obs1_posx, obs1_posy)==True:
                print("Colision Obs1")
                writetext=True
                puntos20(writetext)
                flag = True
                winsound.PlaySound(None, winsound.SND_ASYNC)
                yesno = messagebox.askyesno("Confirmar", "¿Quieres jugar de nuevo?")
                if(yesno):
                    winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
                    Obs1.place(x=890,y=402)
                    flag = False
                    points = -1
                    Thread(target=move_background, args=(Fondo,0,0,)).start()
                    Thread(target=tiempo, args=(L_score,0,0,0,)).start()
                else:
                    winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
                    select_level = False
                    difficulty = 5
                    flag = False
                    points = -1
                    player=""
                    game.destroy()
                    main.deiconify()      
            else:
                flag = False
                game.update()
                time.sleep(0.01)
                return move_obs1_aux(Obs1,x-5,y)

    def move_obs2_aux(Obs2,x,y):#Función que mueve al segundo obstáculo
        global points, obs2_posx, obs2_posy, flag, select_level, difficulty, player
        if x==-300:
            points = points+3
            L_score.config(text="Score: " + str(points))
            print("Fin Nave")
        else:
            x=x-5
            y=y
            obs2_posx=x
            obs2_poosy=y
            Obs2.place(x=x, y=y)
            if colision_obs2(obs2_posx, obs2_posy)==True:
                print("Colision Obs2")
                writetext=True
                puntos20(writetext)
                flag = True
                winsound.PlaySound(None, winsound.SND_ASYNC)
                yesno = messagebox.askyesno("Confirmar", "¿Quieres jugar de nuevo?")
                if(yesno):
                    winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
                    Obs2.place(x=890, y=375)
                    flag = False
                    points = -1
                    Thread(target=move_background, args=(Fondo,0,0,)).start()
                    Thread(target=tiempo, args=(L_score,0,0,0,)).start()
                else:
                    winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
                    select_level = False
                    difficulty = 5
                    flag = False
                    points = -1
                    player=""
                    game.destroy()
                    main.deiconify()
            else:
                flag = False
                game.update()
                time.sleep(0.01)
                return move_obs2_aux(Obs2,x-5,y)

    def move_obs3_aux(Obs3,x,y):#Función que mueve al tercer obstáculo
        global points, obs3_posx, obs3_posy, flag, select_level, difficulty, player
        try:
	        if x==-400:
	            points = points+5
	            L_score.config(text="Score: "+str(points))
	            print("Fin Nave")
	        else:
	            x=x-5
	            y=y
	            obs3_posx=x
	            obs3_posy=y
	            Obs3.place(x=x,y=y)
	            if y!=290:
	                if colision_obs3(obs3_posx,obs3_posy)==True:
	                    print("Colision Obs3")
	                    writetext=True
	                    puntos20(writetext)
	                    flag = True
	                    winsound.PlaySound(None, winsound.SND_ASYNC)
	                    yesno = messagebox.askyesno("Confirmar", "¿Quieres jugar de nuevo?")
	                    if(yesno):
	                        winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
	                        Obs3.place(x=890, y=290)
	                        flag = False
	                        points = -1
	                        Thread(target=move_background, args=(Fondo,0,0,)).start()
	                        Thread(target=tiempo, args=(L_score,0,0,0,)).start()                    
	                    else:
	                        winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
	                        select_level = False
	                        difficulty = 5
	                        flag = False
	                        points = -1
	                        player=""
	                        game.destroy()
	                        main.deiconify()
	                else:
	                    flag=False
	                    game.update()
	                    time.sleep(0.01)
	                    return move_obs3_aux(Obs3,x-5,y)
	            else:
	                if colision_obs33(obs3_posx,obs3_posy)==True:
	                    print("Colision Obs3")
	                    writetext=True
	                    puntos20(writetext)
	                    winsound.PlaySound(None, winsound.SND_ASYNC)
	                    flag = True
	                    yesno = messagebox.askyesno("Confirmar", "¿Quieres jugar de nuevo?")
	                    if(yesno):
	                        winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
	                        Obs3.place(x=890, y=290)
	                        flag = False
	                        points = -1
	                        Thread(target=move_background, args=(Fondo,0,0,)).start()
	                        Thread(target=tiempo, args=(L_score,0,0,0,)).start()                    
	                    else:
	                        winsound.PlaySound("Intro", winsound.SND_LOOP + winsound.SND_ASYNC)
	                        select_level = False
	                        difficulty=5
	                        flag = False
	                        points = -1
	                        player=""
	                        game.destroy()
	                        main.deiconify()
	                else:
	                    flag = False
	                    game.update()
	                    time.sleep(0.01)
	                    return move_obs3_aux(Obs3,x-5,y)
        except:
            pass

    #Función de colisión primer obstáculo
    def colision_obs1(obs1_posx,obs1_posy):
        global c_posx, c_posy

        if 35<=obs1_posx<=100 and obs1_posy>c_posy and c_posy>=350:
            return True

        elif 35<=obs1_posx<=100 and obs1_posy>c_posy and 200<=c_posy>=312:
            return False 

    #Función de colisión segundo obstáculo
    def colision_obs2(obs2_posx,obs2_posy):
        global c_posx, c_posy 
            
        if 35<=obs2_posx<=100:
            if obs2_posx>=c_posx:
                if obs2_posy>c_posy and c_posy<=312:
                    return False
                elif obs2_posy>c_posy and obs2_posx!=c_posx:
                    return False
                else:
                    return True
            elif obs2_posx<c_posx:
                if obs2_posy>c_posy and c_posy<=312:
                    return False
                elif obs2_posy>c_posy and obs2_posx!=c_posx:
                    return False
                else:
                    return True
        else:
            return False

    #Función de colisión tercer obstáculo(los que pueden ser saltados)       
    def colision_obs3(obs3_posx,obs3_posy):
        global c_posx, c_posy
        if 35<=obs3_posx<=100:
            if obs3_posx>=c_posx:
                if obs3_posy>c_posy and c_posy<=312:
                    return False
                elif obs3_posy>c_posy and obs2_posx!=c_posx:
                    return False
                else:
                    return True
            elif obs3_posx<c_posx:
                if obs3_posy>c_posy and c_posy<=312:
                    return False
                elif obs3_posy>c_posy and obs3_posx!=c_posx:
                    return False
                else:
                    return True
        else:
            return False

    #Función de colisión tercer obstáculo(solo se puede esquivar volando)
    def colision_obs33(obs3_posx,obs3_posy):
        global c_posx, c_posy
        if 35<=obs3_posx<=100:
            if c_posy>obs3_posy:
                return False
            elif c_posy<obs3_posy:
                return True
        else:
            return False
 
    def back1():
        game.destroy()
        main.deiconify()
        
    def puntos20(writetext):
        global playe, game_time, points, contenido
        if writetext==True:
            print("Escritura")
            puntuation=open("Highscores.txt","a+")
            Lista=[player,game_time,str(points)]
            puntuation.write(str(Lista))
            puntuation.write("\n")
            writetext=False
        else:
            print("I can´t do it")
            
    
    Btn_back1 = Button(c_game,text="Salir",command=back1,fg="black",bg="#3090C7")
    Btn_back1.place(x=750,y=450)

    Music=loadImg("Music.png")
    Btn_song = Button(c_game,command=song_intro,fg="black",bg="light blue")
    Btn_song.place(x=770,y=42)
    Btn_song.config(image=Music)

    Mute=loadImg("Mute.png")
    Btn_mute=Button(c_game,command=mute,fg="black",bg="light blue")
    Btn_mute.place(x=770,y=71)
    Btn_mute.config(image=Mute)

    Thread(target=move_background, args=(Fondo,0,0,)).start()
    Thread(target=tiempo, args=(L_score,0,0,0,)).start()
    game.bind("<Up>", start)
    game.bind("<Down>", start2)
    Thread(target=obstacles, args=()).start()
    main.mainloop()

#           ____________________________
#__________/Función del botón juego
def empezar_juego():
    #Obtener el nombre de un entry
    nombre = str(E_name.get())
    game_window(nombre)

#           _____________________________________________________
#__________/ VENTANA DESCRIPCIÓN
def w_description():
    #Esconder la ventana principal sin destruirla
    main.withdraw()
    #Ventana 
    Description=Toplevel()
    Description.title("About of")
    Description.minsize(700,550)
    Description.resizable(width=NO,height=NO)

    C_Description=Canvas(Description, width=700, height=550, bg="white")
    C_Description.place(x=0,y=0)

    Author_image=loadImg("creador.gif")
    Author_Description=Label(C_Description, image=Author_image, bg="white")
    Author_Description.photo=Author_image
    Author_Description.place(x=30,y=10)

    L_Informacion=Label(C_Description, text=about, font=("Agency FB",14), fg="black", bg="white")
    L_Informacion.place(x=10,y=164)

    def change_background():
        Lista_backgrounds=["FondoD.gif","Fondo2.gif","Fondo3.gif","Fondo4.gif","Fondo5.gif","Fondo6.gif","Fondo7.gif"]
        BG=random.choice(Lista_backgrounds)
        return background(BG)

    def background(BG):
        BackgroundD=loadImg(BG)
        Background_Description=Label(C_Description, bg="white")
        Background_Description.place(x=250,y=100)
        Background_Description.config(image=BackgroundD)
        time.sleep(2)
        return change_background()

    def back2():
        pt=Thread(target=change_background,args=())
        stop_thread()
        Description.quit()
        main.deiconify()

    def stop_thread():
        pt=Thread(target=change_background,args=())
        
    def confirm_exit3():
        if messagebox.askokcancel("Salir", "¿Estás seguro que quieres salir?"):
            Description.destroy()
            main.deiconify()


    Btn_back2 = Button(C_Description,text="Atras",command=back2,bg="#3090C7",fg="BLACK")
    Btn_back2.place(x=10,y=520)

    pt=Thread(target=change_background,args=()).start()
    Description.protocol('WM_DELETE_WINDOW', confirm_exit3)
    main.mainloop()

#           ________________________________
#__________/Ventana Altos Puntajes
def high_scores():
    #Esconder ventana principal sin destruirla
    main.withdraw()
    #Ventana Altos Puntajes
    scores = Toplevel()
    scores.title("High Scores")
    scores.minsize(500,500)
    scores.resizable(width=NO, height=NO)

    C_scores = Canvas(scores, width=500, height=500, bg="white")
    C_scores.place(x=0, y=0)

    S_background=loadImg("Highscores.gif")
    Scores_background=Label(C_scores, image=S_background, bg="white")
    Scores_background.photo=S_background
    Scores_background.place(x=0,y=0)   

    L_puntuation = Label(C_scores, text="HISTORIAL DE JUEGO", font=("Agency FB", 20), fg="black", bg="white")
    L_puntuation.place(x=285, y=25)

    L_puntuation = Label(C_scores, text="NAME", font=("Agency FB", 14), fg="black", bg="orange")
    L_puntuation.place(x=300, y=70)

    L_puntuation = Label(C_scores, text="TIME", font=("Agency FB", 14), fg="black", bg="orange")
    L_puntuation.place(x=365, y=70)

    L_puntuation = Label(C_scores, text="POINTS", font=("Agency FB", 14), fg="black", bg="orange")
    L_puntuation.place(x=410, y=70)
    
    L_puntuation = Label(C_scores, text="", font=("Agency FB", 20), fg="black", bg="white")
    L_puntuation.place(x=270, y=100)

    puntuation=open("Highscores.txt","r")
    if puntuation.mode=="r":
        contenido=puntuation.read()
        L_puntuation.config(text=contenido)

    def back3():
        scores.destroy()
        main.deiconify()
      
    Btn_back3 = Button(C_scores, text='Atras', command=back3, bg='light blue', fg='black')
    Btn_back3.place(x=10,y=460)

    main.mainloop()
    
#           ____________________________
#__________/Botones de VENTANA PRINCIPAL
Btn_info= Button (C_main,text="ABOUT",command=w_description,fg="black",bg="light blue")
Btn_info.place(x=745,y=5)

Btn_scores= Button (C_main,text="SCORES",command=high_scores,fg="black",bg="light blue")
Btn_scores.place(x=742,y=32)

Btn_hilos = Button(C_main,text="Jugar",command=empezar_juego,fg="black",bg="#2E8B57")
Btn_hilos.place(x=302,y=400)

Btn_Level1 = Button(C_main,text="Fácil",command=easy,fg="black",bg="#2E8B57")
Btn_Level1.place(x=148,y=432)

Btn_Level2 = Button(C_main,text="Medio",command=medium,fg="black",bg="#2E8B57")
Btn_Level2.place(x=193,y=432)

Btn_Level3 = Button(C_main,text="Difícil",command=hard,fg="black",bg="#2E8B57")
Btn_Level3.place(x=248,y=432)
                 
Music=loadImg("Music.png")
Btn_song1 = Button(C_main,command=song_intro,fg="black",bg="light blue")
Btn_song1.place(x=765,y=59)
Btn_song1.config(image=Music)

Mute=loadImg("Mute.png")
Btn_mute=Button(C_main,command=mute,fg="black",bg="light blue")
Btn_mute.place(x=765,y=89)
Btn_mute.config(image=Mute)

main.protocol('WM_DELETE_WINDOW', confirm_exit1)
main.bind("<Escape>", confirm_exit2)
main.mainloop()
