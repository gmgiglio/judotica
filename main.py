import mouseCall
import cv2
from mouseCall import *



def direccion(color_grande,color_chico): 
    vec_grande = pos_objeto(color_grande)
    vec_chico = pos_objeto(color_chico)
    return [float(vec_chico[0]) - float(vec_grande[0]), float(vec_chico[1]) - float(vec_grande[1])]


def print_dir():
    vec_grande = pos_inicial()
    vec_chico = pos_inicial()
    color_grande = color_pos(vec_grande)
    color_chico = color_pos(vec_chico)

    while True:
        print direccion(color_grande,color_chico)

iniciar()

print_dir()

import tcp_client_robot_1_2015 as tcp

tcp.iniciar()
print '1'
print centro()

def avanzar(num):
    for i in range(num):
        tcp.enviarMensaje('w')
def retroceder(num):
    for i in range(num):
        tcp.enviarMensaje('s')

def derecha(num):
    for i in range(num):
        tcp.enviarMensaje('d')


