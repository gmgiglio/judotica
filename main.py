import mouseCall
import cv2
from mouseCall import *

#pos_arco_propio = pos_inicial()

#print 'Posicion de su arco: '+str(pos_arco_propio) 

#pos_arco_rival = pos_inicial()

#print 'Posicion del arco rival: '+str(pos_arco_rival)

#vec = pos_inicial()
#color = color_pos(vec)
#iniciar()
#while True:
 #   vec = pos_objeto(color)
  #  print vec
   # if cv2.waitKey(10) == 27:
    #    capture.release()
     #   break

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
