
import mouseCall as cam
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

cam.iniciar()


import tcp_client_robot_1_2015 as tcp

# tcp.iniciarConexion()

class Objeto:

    def localizar(self):
        pos = cam.elegirPosicion()
        self.color = cam.color_pos(pos)
        print pos

    def pos(self):
        return cam.pos_objeto(self.color)


class Robot(Objeto):

    def iniciar(self):
        self.localizar()
        pos = cam.elegirPosicion()
        self.colorChico = cam.color_pos(pos)
        print pos


    def direccion(self):
        posChico = cam.pos_objeto(self.colorChico)
        posGrande = self.pos()
        return [int(posChico[0]) - int(posGrande[0]), int(posChico[1]) - int(posGrande[1])]



class Jigoro(Robot):

    razonGiro = 0.4 # 22,9183 grados
    razonAvanzar = 1

    def avanzar(self,num):
        for i in range(num):
            tcp.enviarMensaje('s')
    def retroceder(num):
        for i in range(num):
            tcp.enviarMensaje('w')

    def girarDerecha(self,angulo):
        n = int(self.razonGiro * angulo)
        for i in range(n):
            tcp.enviarMensaje('d')

    def girarIzquierda(self,angulo):
        n = int(self.razonGiro * angulo)
        for i in range(n):
            tcp.enviarMensaje('a')


    def calibrarGiro(self):
        giros = []
        for i in range(5):
            dir = self.direccion()
            angulo1 = np.arctan2(dir[0],dir[1])
            self.girarIzquierda(i)
            dir = self.direccion()
            angulo2 = np.arctan2(dir[0],dir[1])
            giros.append((angulo2 - angulo1)/i)
        for i in range(5):
            dir = self.direccion()
            angulo1 = np.arctan2(dir[0],dir[1])
            self.girarDerecha(i)
            dir = self.direccion()
            angulo2 = np.arctan2(dir[0],dir[1])
            giros.append((angulo2 - angulo1)/i)
        razonGiro = np.mean(giros)



