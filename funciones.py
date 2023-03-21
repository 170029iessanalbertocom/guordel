import random
import pygame as pg
from pygame import *
import keyboard
pg.mixer.init()

class juego:
    def __init__(self,pantalla):
        self.ventana=pantalla
        self.blanco=(255,255,255)
        self.negro=(0,0,0)
        self.verde=(189,236,182)
        self.amarillo=(253,253,150)
        self.grisclaro=(155,155,155)
        self.grisoscuro=(71,75,78)
        self.alfabeto="QWERTYUIOPASDFGHJKLÑZXCVBNM"
        self.intentos="QWERTYUIOPASDFGHJKLÑZXCVBNM123"
        self.posicionesintentos=(((145,25),(190,25),(235,25),(280,25),(325,25)),
                              ((145,95),(190,95),(235,95),(280,95),(325,95)),
                              ((145,165),(190,165),(235,165),(280,165),(325,165)),
                              ((145,235),(190,235),(235,235),(280,235),(325,235)),
                              ((145,305),(190,305),(235,305),(280,305),(325,305)),
                              ((145,375),(190,375),(235,375),(280,375),(325,375)))
        self.posicionesteclas=(((30,460),(75,460),(120,460),(165,460),(210,460),(255,460),(300,460),(345,460),(390,460),(435,460)),
                            ((30,520),(75,520),(120,520),(165,520),(210,520),(255,520),(300,520),(345,520),(390,520),(435,520)),
                            ((100,580),(145,580),(190,580),(235,580),(280,580),(325,580),(370,580)))
        self.diccionario=open("recursos/diccionario.txt","r",encoding='UTF-8')
        self.screen=pantalla
        self.listadicc=[]
        self.estadoactual=[0,0]
        self.tipoletra=("arial",36,(self.negro[0],self.negro[1],self.negro[2]),(self.grisclaro[0],self.grisclaro[1],self.grisclaro[2]))
        self.pintarescenario(self.tipoletra)
        self.palabraelegida=""
        self.listapalabras=self.palabras(5)
        self.palabrasecreta=random.choice(self.listapalabras)
        self.fallos=0
        self.perder=pg.image.load("recursos/has perdido.jpg")
        self.ganar=pg.image.load("recursos/has ganado.png")
        self.musicaperder=pg.mixer.Sound("recursos/musicafea.mp3")
        self.musicaganar=pg.mixer.Sound("recursos/musicabonita.mp3")
        self.sonidofallo=pg.mixer.Sound("recursos/fallo.wav")
        self.sonidonoexiste=pg.mixer.Sound("recursos/noexiste.mp3")

    def palabras(self,letras):
        for linea in self.diccionario:
            if (len(linea)==letras+1):
                self.listadicc.append(linea[0:letras])
        self.diccionario.close()
        return self.listadicc

    def pintartecla(self,posicion,color,letra,estilo):
        draw.rect(self.ventana,color,(posicion[0],posicion[1],40,40),20)
        draw.rect(self.ventana,self.negro,(posicion[0],posicion[1],40,40),1)
        self.fuente=pg.font.SysFont(estilo[0],estilo[1])
        self.texto=self.fuente.render(letra,True,self.negro)
        self.ventana.blit(self.texto,(posicion[0]+9,posicion[1]))

    def pintarintento(self,posicion,estilo):
        draw.rect(self.ventana,(estilo[3]),(posicion[0],posicion[1],40,40),20)
        draw.rect(self.ventana,(estilo[2]),(posicion[0],posicion[1],40,40),1)

    def pintarescenario(self,estilo):
        for letras in self.alfabeto:
            self.pintartecla(self.posicionesteclas[self.alfabeto.find(letras)//(10)][self.alfabeto.find(letras)%10],self.grisclaro,letras,(estilo[0],estilo[1]))
        for espacios in self.intentos:
            self.pintarintento(self.posicionesintentos[self.intentos.find(espacios)//(5)][self.intentos.find(espacios)%5],estilo)

    def bloquearteclado(self):
        for teclas in range(150):
            keyboard.block_key(teclas)

    def pulsartecla(self,tecla):
        if (tecla.key==pg.K_a) or (tecla.key==pg.K_b) or (tecla.key==pg.K_c) or (tecla.key==pg.K_d) or\
            (tecla.key==pg.K_e) or (tecla.key==pg.K_f) or (tecla.key==pg.K_g) or (tecla.key==pg.K_h) or\
            (tecla.key==pg.K_i) or (tecla.key==pg.K_j) or (tecla.key==pg.K_k) or (tecla.key==pg.K_l) or\
            (tecla.key==pg.K_m) or (tecla.key==pg.K_n) or (tecla.key==pg.K_o) or (tecla.key==pg.K_p) or\
            (tecla.key==pg.K_q) or (tecla.key==pg.K_r) or (tecla.key==pg.K_s) or (tecla.key==pg.K_t) or\
            (tecla.key==pg.K_u) or (tecla.key==pg.K_v) or (tecla.key==pg.K_w) or (tecla.key==pg.K_x) or\
            (tecla.key==pg.K_y) or (tecla.key==pg.K_z):
            if (tecla.unicode.upper() in self.alfabeto) and (self.estadoactual[1]<5):
                self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]],self.grisclaro,tecla.unicode.upper(),self.tipoletra)
                self.estadoactual[1]=self.estadoactual[1]+1
                self.palabraelegida=self.palabraelegida+tecla.unicode.upper()

        elif (tecla.key==pg.K_BACKSPACE) and (self.estadoactual[1]>0):
            self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]-1],self.grisclaro,"",self.tipoletra)
            self.estadoactual[1]=self.estadoactual[1]-1
            self.palabraelegida=self.palabraelegida[0:len(self.palabraelegida)-1]

        elif (tecla.key==pg.K_RETURN) and (self.estadoactual[1]==5):
            if self.palabraelegida in self.listapalabras:
                self.estadoactual[1]=0

                if self.palabraelegida[0] in self.palabrasecreta[0]:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]],self.verde,self.palabraelegida[0],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[0])//(10)][self.alfabeto.find(self.palabraelegida[0])%10],self.verde,self.palabraelegida[0],self.tipoletra)
                    self.fallos=self.fallos+1
                elif self.palabraelegida[0] in self.palabrasecreta:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]],self.amarillo,self.palabraelegida[0],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[0])//(10)][self.alfabeto.find(self.palabraelegida[0])%10],self.amarillo,self.palabraelegida[0],self.tipoletra)
                    self.fallos=self.fallos+1
                else:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]],self.grisoscuro,self.palabraelegida[0],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[0])//(10)][self.alfabeto.find(self.palabraelegida[0])%10],self.grisoscuro,self.palabraelegida[0],self.tipoletra)
                    self.fallos=self.fallos+1

                if self.palabraelegida[1] in self.palabrasecreta[1]:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+1],self.verde,self.palabraelegida[1],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[1])//(10)][self.alfabeto.find(self.palabraelegida[1])%10],self.verde,self.palabraelegida[1],self.tipoletra)
                elif self.palabraelegida[1] in self.palabrasecreta:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+1],self.amarillo,self.palabraelegida[1],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[1])//(10)][self.alfabeto.find(self.palabraelegida[1])%10],self.amarillo,self.palabraelegida[1],self.tipoletra)
                else:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+1],self.grisoscuro,self.palabraelegida[1],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[1])//(10)][self.alfabeto.find(self.palabraelegida[1])%10],self.grisoscuro,self.palabraelegida[1],self.tipoletra)

                if self.palabraelegida[2] in self.palabrasecreta[2]:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+2],self.verde,self.palabraelegida[2],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[2])//(10)][self.alfabeto.find(self.palabraelegida[2])%10],self.verde,self.palabraelegida[2],self.tipoletra)
                elif self.palabraelegida[2] in self.palabrasecreta:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+2],self.amarillo,self.palabraelegida[2],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[2])//(10)][self.alfabeto.find(self.palabraelegida[2])%10],self.amarillo,self.palabraelegida[2],self.tipoletra)
                else:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+2],self.grisoscuro,self.palabraelegida[2],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[2])//(10)][self.alfabeto.find(self.palabraelegida[2])%10],self.grisoscuro,self.palabraelegida[2],self.tipoletra)

                if self.palabraelegida[3] in self.palabrasecreta[3]:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+3],self.verde,self.palabraelegida[3],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[3])//(10)][self.alfabeto.find(self.palabraelegida[3])%10],self.verde,self.palabraelegida[3],self.tipoletra)
                elif self.palabraelegida[3] in self.palabrasecreta:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+3],self.amarillo,self.palabraelegida[3],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[3])//(10)][self.alfabeto.find(self.palabraelegida[3])%10],self.amarillo,self.palabraelegida[3],self.tipoletra)
                else:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+3],self.grisoscuro,self.palabraelegida[3],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[3])//(10)][self.alfabeto.find(self.palabraelegida[3])%10],self.grisoscuro,self.palabraelegida[3],self.tipoletra)

                if self.palabraelegida[4] in self.palabrasecreta[4]:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+4],self.verde,self.palabraelegida[4],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[4])//(10)][self.alfabeto.find(self.palabraelegida[4])%10],self.verde,self.palabraelegida[4],self.tipoletra)
                elif self.palabraelegida[4] in self.palabrasecreta:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+4],self.amarillo,self.palabraelegida[4],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[4])//(10)][self.alfabeto.find(self.palabraelegida[4])%10],self.amarillo,self.palabraelegida[4],self.tipoletra)
                else:
                    self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]+4],self.grisoscuro,self.palabraelegida[4],self.tipoletra)
                    self.pintartecla(self.posicionesteclas[self.alfabeto.find(self.palabraelegida[4])//(10)][self.alfabeto.find(self.palabraelegida[4])%10],self.grisoscuro,self.palabraelegida[4],self.tipoletra)

                if self.palabraelegida==self.palabrasecreta:
                    self.screen.blit(self.ganar,(0,0))
                    pg.mixer.Sound.play(self.musicaganar)
                    self.bloquearteclado()

                else:
                    self.palabraelegida=""
                    self.estadoactual[1]=0
                    self.estadoactual[0]=self.estadoactual[0]+1
                    if self.fallos>=4:
                        pg.mixer.Sound.play(self.sonidofallo)
                    if self.fallos==6:
                        self.screen.blit(self.perder,(0,0))
                        pg.mixer.Sound.play(self.musicaperder)
                        self.bloquearteclado()

            else:
                self.palabraelegida=""
                self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]-1],self.grisclaro,"",self.tipoletra)
                self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]-2],self.grisclaro,"",self.tipoletra)
                self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]-3],self.grisclaro,"",self.tipoletra)
                self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]-4],self.grisclaro,"",self.tipoletra)
                self.pintartecla(self.posicionesintentos[self.estadoactual[0]][self.estadoactual[1]-5],self.grisclaro,"",self.tipoletra)
                self.estadoactual[1]=self.estadoactual[1]-5
                self.palabraelegida=self.palabraelegida[0:len(self.palabraelegida)-5]
                pg.mixer.Sound.play(self.sonidonoexiste)