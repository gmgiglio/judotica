
from ciclo2 import Objeto
import numpy as np
import tcp_client_robot_1_2015 as tcp

# tcp.iniciarConexion()


class Robot:

    def __init__(self,objGrande,objChico):
        self.objGrande = objChico
        self.objChico = objChico


    def direccion(self):

        return [int(self.objChico.pos[0]) - int(self.objGrande.pos[0]), int(self.objChico.pos[1]) - int(self.objGrande.pos[1])]



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
