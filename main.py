from funciones import *

pg.init()
ventana=pg.display.set_mode((515,747))
fondo=pg.image.load("recursos/fondo.jpg")
logo=pg.image.load("recursos/polloptero.png")
pg.display.set_icon(logo)
ventana.blit(fondo,(0,0))
blanco=(255,255,255)
negro=(0,0,0)
verde=(189,236,182)
amarillo=(253,253,150)
gris=(155,155,155)
pg.display.set_caption("Adivinar la palabra")

nuevojuego=juego(ventana)
jugando=True
while jugando:

    for event in pg.event.get():
        if event.type==pg.QUIT:
            jugando=False

        if event.type==pg.KEYDOWN:
            nuevojuego.pulsartecla(event)

    pg.display.flip()
pg.quit()