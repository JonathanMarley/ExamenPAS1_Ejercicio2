import socket
import threading


def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"Mensaje recibido: {mensaje}")
        except:
            print("Conexión cerrada por el servidor")
            break


def cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(('localhost', 5060))

    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(cliente_socket,))
    hilo_recibir.start()

    while True:
        mensaje = input("Ingrese mensaje: ")
        if mensaje.lower() == 'salir':
            cliente_socket.close()
            break
        cliente_socket.send(mensaje.encode('utf-8'))


if __name__ == "__main__":
    cliente()
