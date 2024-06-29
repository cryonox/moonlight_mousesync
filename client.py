import atexit
import util
import socket
import cursor_util
import threading
import time
import ctypes
import win32con
import win32api

atexit.register(util.restore_system_cursor)
C = util.load_config('config.yaml')

server_cursor = None
should_change = False
should_continue = True


def log(msg):
    if C.should_log:
        print(msg)


def cursor_func():
    global server_cursor, should_change
    while should_continue:
        time.sleep(0.01)
        pname = util.active_window_process_name()
        if pname != "Moonlight.exe":
            util.restore_system_cursor()
            continue
        if should_change:
            log('Changing cursor!')
            log(server_cursor.type)
            util.restore_system_cursor()
            log(ctypes.windll.user32.SetSystemCursor(
                server_cursor.handle, win32con.IDC_ARROW))
            should_change = False
    log('exiting cursor')


def sync_func():

    global server_cursor, should_continue, should_change
    HOST = C.serverip
    PORT = C.port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.settimeout(1.0)
        s.connect((HOST, PORT))
        while should_continue:
            try:
                data = s.recv(1024)
                cur = data.decode('utf-8')
                log(f"Received {cur}")
                if cur == 'IBEAM' and C.ibeam_mode !='normal':
                    server_cursor = cursor_util.Cursor.load_custom(C.ibeam_mode)
                else:
                    server_cursor = cursor_util.DEFAULT_CURSORS[cur]
                should_change = True
            except socket.timeout as ex:
                pass
        log('exiting sync')


cursor_t = threading.Thread(target=cursor_func, args=())
sync_t = threading.Thread(target=sync_func, args=())
cursor_t.start()
sync_t.start()

while should_continue:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
should_continue = False
cursor_t.join()
sync_t.join()
