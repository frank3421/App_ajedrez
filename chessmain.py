import pygame as p
import chessengine

WIDTH=HEIGHT=512

DIMENSION=8
#tamaño del cuadrado en el tablero
SQ_SIZE=HEIGHT//DIMENSION

MAX_FPS=15

IMAGES={}
p.init()
def loadimages():
    IMAGES["wp"]=p.transform.scale(p.image.load("imagenes/wp.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["bp"]=p.transform.scale(p.image.load("imagenes/bp.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["bR"]=p.transform.scale(p.image.load("imagenes/bR.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["bB"]=p.transform.scale(p.image.load("imagenes/bB.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["bN"]=p.transform.scale(p.image.load("imagenes/bN.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["bQ"]=p.transform.scale(p.image.load("imagenes/bQ.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["bK"]=p.transform.scale(p.image.load("imagenes/bK.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["wR"]=p.transform.scale(p.image.load("imagenes/wR.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["wB"]=p.transform.scale(p.image.load("imagenes/wB.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["wN"]=p.transform.scale(p.image.load("imagenes/wN.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["wQ"]=p.transform.scale(p.image.load("imagenes/wQ.png"), (SQ_SIZE,SQ_SIZE))
    IMAGES["wK"]=p.transform.scale(p.image.load("imagenes/wK.png"), (SQ_SIZE,SQ_SIZE))
#Agrega al diccionario las llaves que permiten acceder a las imagenes
loadimages()

def main():

    #Se despliega la ventana estableciendo el ancho y el largo definido anteriormente
    ventana=p.display.set_mode((WIDTH,HEIGHT))
    #Permite acceder al tiempo desde que se inicio el programa hasta el presente
    reloj=p.time.Clock()
    #Se crea la variable gs que permite acceder al estado del juego
    gs=chessengine.estadojuego()
    movimientosvalidos=gs.movimientosvalidos()
    movimientohecho=False
    running=True
    #Se guarda el valor x e y al clickear una determinada casilla
    casilla_seleccionada=()
    #Se guarda las coordenandas de los clicks del jugador como 2-tuplas en la lista
    lista_clicks_jugador=[]
    while running==True:
        for esc in p.event.get():
            #Permite cerrar la ventana al clickear en el boton cerrar ventana
            if esc.type== p.QUIT:
                running=False
            elif esc.type==p.MOUSEBUTTONDOWN:
                #se obtendra la posicion del lugar en el que se clickeo, lo entrega en forma de 2-tupla en
                #eje x y eje y
                localizacion = p.mouse.get_pos()
                #se obtiene el valor x e y de la variable localizacion y se divide por el tamaño del cuadrado
                #para obtener un valor entero del 0 al 8 en el eje x e y que indique la posicion del cuadrado
                (col,fil)=(localizacion[0]//SQ_SIZE,localizacion[1]//SQ_SIZE)
                #Nos ponemos en el caso en el que el jugador selecciona la misma casilla.   En este caso,
                #se eliminan las coordenadas previamente obtenidas en mi casilla_seleccionada y se vacia la 
                #lista de clicks
                if casilla_seleccionada==(fil,col): 
                    casilla_seleccionada=()
                    lista_clicks_jugador=[]
                #En caso contrario, se guarda las coordenadas en mi variable casilla_seleccionada y 
                #se añade las coordenadas de esta variable a la lista_clicks_jugador
                else:
                    casilla_seleccionada=(fil,col)
                    lista_clicks_jugador+=[casilla_seleccionada]
                #en caso de que se hayan hecho los dos clicks necesarios para mover una pieza y no se haya
                #clickeado en la misma casilla
                if len(lista_clicks_jugador)==2:
                    #se ocupa la clase movimiento para luego ser ocupada en hacermovimiento que permite
                    #realizr el movimiento
                    movimiento=chessengine.movimiento(lista_clicks_jugador[0],lista_clicks_jugador[1],gs.tablero)
                    #Se modifica el tablero moviendo la pieza y eliminando otra pieza en caso de que la 
                    #casilla final tenga una pieza
                    if movimiento in movimientosvalidos:
                        print(movimiento.obtenernotacionajedrez())
                        gs.hacermovimiento(movimiento)
                        movimientohecho=True
                        casilla_seleccionada=()
                        lista_clicks_jugador=[]
                    else:
                        lista_clicks_jugador=[casilla_seleccionada]
            #En caso de se presionada alguna tecla
            elif esc.type==p.KEYDOWN:
                #Si se presiona la tecla h, el tablaro se modifica deshaciendo el ultimo movimiento
                if esc.key==p.K_h:
                    #se ocupa la clase deshacermovimiento
                    gs.deshacermovimiento()
                    movimientohecho=True
                elif esc.key==p.K_ESCAPE:
                    running=False
        if movimientohecho==True:
            movimientosvalidos=gs.movimientosvalidos()
            movimientohecho=False
        #inicializa la funcion que permitira dibujar en la ventana el tablero junto con las piezas en sus
        #respectivas posiciones
        dibujarestadodejuego(ventana,gs)
        reloj.tick(MAX_FPS)
        #permite realizar los cambios que se realizan en la ventana
        p.display.flip()

def dibujarestadodejuego(ventana,gs):
    dibujartablero(ventana)
    dibujarpiezas(ventana,gs.tablero)
#se encarga de dibujar el tablero
def dibujartablero(ventana):
    colores=[p.Color("white"),p.Color("brown")]
    for i in range(0,8):
            for k in range(0,8):
                #se van alternando los colores blanco y cafe y se establece sus dimensiones con p.draw.rect
                color=colores[((i+k)%2)]

                
                p.draw.rect(ventana,color,p.Rect(i*SQ_SIZE,k*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    
#se encangar de dibujar las piezas en el tablero
def dibujarpiezas(ventana,tablero):
    for fila in range(0,8):
        for columna in range(0,8):
            pieza=tablero[columna][fila]
            #permite cargar las piezas solo en aquellas casillas donde sale la llave perteneciente a cada una
            if pieza!="--":
                #genera en el tablero las piezas 
                ventana.blit(IMAGES[pieza],p.Rect(fila*SQ_SIZE,columna*SQ_SIZE,SQ_SIZE,SQ_SIZE))


main()







