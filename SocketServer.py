import socket
import threading

# Lista para almacenar conexiones de clientes
clientes = []
lock = threading.Lock()

# Función para manejar la conexión de cada cliente
def manejar_cliente(conexion, direccion):
    print(f"Cliente conectado: {direccion}")
    with lock:
        clientes.append(conexion)
    try:
        while True:
            mensaje = conexion.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"Mensaje recibido de {direccion}: {mensaje}")
            broadcast(mensaje, conexion)
    except:
        pass
    finally:
        print(f"Cliente desconectado: {direccion}")
        with lock:
            clientes.remove(conexion)
        conexion.close()
        broadcast(f"Cliente {direccion} se ha desconectado", conexion)

# Función para retransmitir mensajes a todos los clientes conectados
def broadcast(mensaje, conexion_excluida):
    with lock:
        for cliente in clientes:
            if cliente != conexion_excluida:
                try:
                    cliente.send(mensaje.encode('utf-8'))
                except:
                    cliente.close()
                    clientes.remove(cliente)

# Configuración del servidor
def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5060))
    server_socket.listen(5)
    print("Servidor activo para recibir mensajes")

    while True:
        conexion, direccion = server_socket.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
        hilo_cliente.start()

if __name__ == "__main__":
    servidor()
