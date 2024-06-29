import socket
import threading
import time
import cursor_util
import util


def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")
    cur = None
    try:
        while True:
            if cur != cursor_util.get_current_cursor():
                cur = cursor_util.get_current_cursor()
                client_socket.sendall(str(cur).encode('utf-8'))
            time.sleep(0.1)
        print(f"Connection from {addr} closed.")
    except Exception as ex:
        print(ex)
    finally:
        client_socket.close()


def main():
    c = util.load_config('config.yaml')
    host = c.listenaddress
    port = c.port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.settimeout(1.0)
    print(f"Server listening on {host}:{port}")
    while True:
        try:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, addr))
            client_thread.start()
        except KeyboardInterrupt:
            print("Server interrupted. Closing...")
            break
        except socket.timeout as e:
            pass


if __name__ == "__main__":
    main()
