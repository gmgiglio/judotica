import socket


def iniciar():
    TCP_IP = '192.168.0.138'
    TCP_PORT = 2000
    BUFFER_SIZE = 20
    MESSAGE = "Listo"
    PASS = "G01"
    CONNECTED = False

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    while True:

	data = s.recv(BUFFER_SIZE)
	print "received data:", data

	if data == "PASS?":
		s.send(PASS)

	elif data == "AOK":
		CONNECTED = True
		break

	else:
		CONNECTED = False
		break



def cerrar():
    s.close()
    quit()

def enviarMensaje(mensaje):

	s.send(mensaje)
	print "meensajeenviado"

