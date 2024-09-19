


import numpy as np

class estadojuego():
    def __init__(self):
        #Va a representar el estado del trablero a medida que se va desarrollando el juego
        self.tablero=np.array([["bR","bN","bB","bQ","bK","bB","bN","bR"]
                             ,["bp","bp","bp","bp","bp","bp","bp","bp"]
                             ,["--","--","--","--","--","--","--","--"],
                              ["--","--","--","--","--","--","--","--"],
                              ["--","--","--","--","--","--","--","--"],
                              ["--","--","--","--","--","--","--","--"],
                              ["wp","wp","wp","wp","wp","wp","wp","wp"],
                              ["wR","wN","wB","wQ","wK","wB","wN","wR"]])
        #determina si es el turno de las blancas o las negras
        self.whitemove=True
        #Guarda el historial de jugadas
        self.movelog=[]
        self.posicionreyblanco=[7,4]
        self.posicionreynegro=[0,4]
    #Actualiza el tablero dependiendo de la informacion proporcionada por la clase movimiento
    def hacermovimiento(self,movimiento):
        #se deja vacia la posicion en la que estaba la pieza movida
        self.tablero[movimiento.ini_fil][movimiento.ini_col]="--"
        #Se coloca la pieza en la casilla destino 
        self.tablero[movimiento.fin_fil][movimiento.fin_col]=movimiento.piezamovida
        #se añade al historial de jugadas el movimiento en cuestion
        self.movelog.append(movimiento)
        #Cambia el turno
        self.whitemove=not self.whitemove
        if movimiento.piezamovida=="wK":
            self.posicionreyblanco=(movimiento.fin_fil,movimiento.fin_col)
        if movimiento.piezamovida=="wB":
            self.posicionreynegro=(movimiento.fin_fil,movimiento.fin_col)
    #Permite deshacer un movimiento
    def deshacermovimiento(self):
        #Evita que se genere un error en caso de no haberse realizado un movimiento previo
        if len(self.movelog)!=0:
            #Se quita de la lista el ultimo movimiento y se rescatan sus datos al guardarlos en la variable
            #movimiento
            movimiento=self.movelog.pop()
            #se modifica el tablero a como estaba previo al movimiento ocupando la clase movimiento extraida
            #de la lista movelog
            self.tablero[movimiento.ini_fil][movimiento.ini_col]=movimiento.piezamovida
            self.tablero[movimiento.fin_fil][movimiento.fin_col]=movimiento.piezacapturada
            #se cambia el turno
            self.whitemove=not self.whitemove
            if movimiento.piezamovida=="wK":
                self.posicionreyblanco=(movimiento.ini_fil,movimiento.ini_col)
            if movimiento.piezamovida=="wB":
                self.posicionreynegro=(movimiento.ini_fil,movimiento.ini_col)
    #Lo que hara esta funcion sera obtener todas los posibles movimientos de una pieza de acuerdo a 
    #la logica de movimiento de cada una 
    
    def funcion1(self):
        movimientos=[]
        for f in range(8):
            for c in range(8):
                color=self.tablero[f][c][0]
                if (color=="w" and self.whitemove==True) or (color=="b" and not self.whitemove):
                    pieza=self.tablero[f][c][1]
                    if pieza=="p":
                        self.obtenermovimientospeon(f,c,movimientos)
                    elif pieza=="R":
                        self.obtenermovimientostorre(f,c,movimientos)
                    elif pieza=="N":
                        self.obtenermovimientoscaballo(f,c,movimientos)
                    elif pieza=="B":
                        self.obtenermovimientosalfil(f,c,movimientos)
                    elif pieza=="Q":
                        self.obtenermovimientosreina(f,c,movimientos)
                    elif pieza=="K":
                        self.obtenermovimientosrey(f,c,movimientos)
        return movimientos
    def movimientosvalidos(self):
        
        movimientos=self.funcion1()
        #for i in range(len(movimientos)-1,-1,-1):
         #   self.hacermovimiento(movimientos[i])
          #  self.whitemove=not self.whitemove
           # if self.enjaque()==True:
            #    movimientos.remove(movimientos[i])
            #self.whitemove=not self.whitemove
            #self.deshacermovimiento()
        return movimientos
    def enjaque(self):
        if self.whitemove:      
            return self.casillabajoataque(self.posicionreyblanco[0],self.posicionreyblanco[1])
        else:
            return self.casillabajoataque(self.posicionreynegro[0],self.posicionreynegro[1])
            
    def casillabajoataque(self,f,c):
        self.whitemove=not self.whitemove
        movimientosoponente=self.funcion1()
        self.whitemove=not self.whitemove
        for movimiento in movimientosoponente:
            if movimiento.fin_fil==f and movimiento.fin_col==c:
                return True
        return False

    def obtenermovimientospeon(self,f,c,movimientos):
        if self.whitemove==True:
            if self.tablero[f-1][c]=="--":
                movimientos.append(movimiento((f,c),(f-1,c),self.tablero))
                if f==6 and self.tablero[f-2][c]=="--":
                    movimientos.append(movimiento((f,c),(f-2,c),self.tablero))
            if c-1>=0:
                if self.tablero[f-1][c-1][0]=="b":
                    movimientos.append(movimiento((f,c),(f-1,c-1),self.tablero))
            if c+1<=7:
                if self.tablero[f-1][c+1][0]=="b":
                    movimientos.append(movimiento((f,c),(f-1,c+1),self.tablero))

        else:
            if self.tablero[f+1][c]=="--":
                movimientos.append(movimiento((f,c),(f+1,c),self.tablero))
                if f==1 and self.tablero[f+2][c]=="--":
                    movimientos.append(movimiento((f,c),(f+2,c),self.tablero))
            if c-1>=0:
                if self.tablero[f+1][c-1][0]=="w":
                    movimientos.append(movimiento((f,c),(f+1,c-1),self.tablero))
            if c+1<=7:
                if self.tablero[f+1][c+1][0]=="w":
                    movimientos.append(movimiento((f,c),(f+1,c+1),self.tablero))


    def obtenermovimientostorre(self, f, c, movimientos):
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        opposing_color = "b" if self.whitemove else "w"
        
        for direccion in direcciones:
            variablef = f + direccion[0]
            variablec = c + direccion[1]

            while 0 <= variablef <= 7 and 0 <= variablec <= 7:
                cell_contents = self.tablero[variablef][variablec][0]
                if cell_contents == "-":
                    movimientos.append(movimiento((f,c), (variablef, variablec), self.tablero))
                    variablef += direccion[0]
                    variablec += direccion[1]
                elif cell_contents == opposing_color:
                    movimientos.append(movimiento((f,c), (variablef, variablec), self.tablero))
                    break
                else:
                    break

    def obtenermovimientoscaballo(self,f,c,movimientos):
        posibles_movimientos=[[f+2,c-1],[f+2,c+1],[f-2,c-1],[f-2,c+1],
                              [f-1,c+2],[f+1,c+2],[f-1,c-2],[f+1,c-2]]
        if self.whitemove==True:
            for k in posibles_movimientos:
                if 0<=k[0]<=7 and 0<=k[1]<=7 and self.tablero[k[0]][k[1]][0]!="w":
                    movimientos.append(movimiento((f,c),(k[0],k[1]),self.tablero))
        else:
            for k in posibles_movimientos:
                if 0<=k[0]<=7 and 0<=k[1]<=7 and self.tablero[k[0]][k[1]][0]!="b":
                    movimientos.append(movimiento((f,c),(k[0],k[1]),self.tablero))


    def obtenermovimientosalfil(self,f,c,movimientos):
        piece = 'w' if self.whitemove else 'b'
        opponent = 'b' if piece == 'w' else 'w'

        for df, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                nf, nc = f + i * df, c + i * dc
                if nf < 0 or nf > 7 or nc < 0 or nc > 7:
                    break

                if self.tablero[nf][nc][0] == "-":
                    movimientos.append(movimiento((f,c),(nf,nc),self.tablero))
                elif self.tablero[nf][nc][0] == piece:
                    break
                elif self.tablero[nf][nc][0] == opponent:
                    movimientos.append(movimiento((f,c),(nf,nc),self.tablero))
                    break



            
    def obtenermovimientosreina(self,f,c,movimientos):
        self.obtenermovimientosalfil(f,c,movimientos)
        self.obtenermovimientostorre(f,c,movimientos)
    def obtenermovimientosrey(self,f,c,movimientos):
        posibles_movimientos=[[f+1,c],[f-1,c],[f,c-1],[f,c+1],
                              [f+1,c+1],[f-1,c-1],[f+1,c-1],[f-1,c+1]]
        if self.whitemove==True:
            for k in posibles_movimientos:
                if 0<=k[0]<=7 and 0<=k[1]<=7 and self.tablero[k[0]][k[1]][0]!="w":
                    movimientos.append(movimiento((f,c),(k[0],k[1]),self.tablero))
        else:
            for k in posibles_movimientos:
                if 0<=k[0]<=7 and 0<=k[1]<=7 and self.tablero[k[0]][k[1]][0]!="b":
                    movimientos.append(movimiento((f,c),(k[0],k[1]),self.tablero))
        

class movimiento():
    #Va a permitir transformar desde la notacion del ajedrez a la notacion inicial en la fila
    pata={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    #Permite transformar desde la notacion inical a la notacion del ajedrez en la fila
    # .items permite generar una 2 tupla con la llave y el valor indexado a esa llave y luego se
    #hace un recorrido con un ciclo for a pata.items generando los valores k,v que crean el nuevo diccionario
    #pero los valores como llaves y las llaves como valores
    tapa={v:k for k,v in pata.items()}
    #Permite transformar desde la notacion de ajedrez a la notacion inicial en la columna
    hilo={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    #Permite transformar desde la notacion inicial a la notacion del ajedrwz
    lohi={v:k for k,v in hilo.items()}
    def __init__(self,cas_ini,cas_fin,tablero):
        #Guarda las coordenadas x e y iniciales
        self.ini_fil=cas_ini[0]
        self.ini_col=cas_ini[1]
        #guardas las coordenadas finales x e y
        self.fin_fil=cas_fin[0]
        self.fin_col=cas_fin[1]
        #La casilla se actualiza con la pieza que se movio 
        self.piezamovida=tablero[self.ini_fil][self.ini_col]
        self.piezacapturada=tablero[self.fin_fil][self.fin_col]
        self.IDmovimiento=self.ini_fil*1000+self.ini_col*100+self.fin_fil*10+self.fin_col*1
        
    def __eq__(self,otro):
        if isinstance(otro,movimiento):
            return self.IDmovimiento==otro.IDmovimiento
        else: return False


    def obtenernotacionajedrez(self):
        return self.obtenernotacioninicial(self.ini_fil,self.ini_col)+self.obtenernotacioninicial(self.fin_fil,self.fin_col)


    def obtenernotacioninicial(self,x,y):
        return self.lohi[y]+self.tapa[x]


