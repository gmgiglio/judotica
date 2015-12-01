
import Camara as cam
import numpy as np

"""
pos_arco_propio = pos_inicial()

print 'Posicion de su arco: '+str(pos_arco_propio)

pos_arco_rival = pos_inicial()

print 'Posicion del arco rival: '+str(pos_arco_rival)

vec = pos_inicial()
color = color_pos(vec)
iniciar()
while True:
    vec = pos_objeto(color)
    print vec
    if cv2.waitKey(10) == 27:
        capture.release()
        break

"""

cam.iniciarCaptura()


import tcp_client_robot_1_2015 as tcp

tcp.iniciarConexion()

class Objeto:

    def localizar(self):
        self.color = cam.color_pos(cam.elegirPosicion('has click sobre el objeto'))

    def pos(self):
        return cam.pos_objeto(self.color)


class Robot(Objeto):

    def iniciar(self):
        self.localizar()
        self.colorChico = cam.color_pos(cam.elegirPosicion('has click sobre el circulo chico'))


    def direccion(self):
        posChico = cam.pos_objeto(self.colorChico)
        posGrande = self.pos()
        return [int(posChico[0]) - int(posGrande[0]), int(posChico[1]) - int(posGrande[1])]



class Jigoro(Robot):

    razonGiro = 0.4 # 22,9183 grados
    razonAvanzar = 1

    def vel(self, x , y):
        x + 128
        y + 128
        tcp.enviarMensaje(bytes(x))
        tcp.enviarMensaje(bytes(y))

