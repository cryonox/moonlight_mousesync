import yaml
import win32process
import ctypes
import ctypes.wintypes
import win32gui
import win32api
import win32process
import win32con
from pathlib import Path



class AttrDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except (KeyError, RecursionError):
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def dict2attrdict(dictionary):
    ret = AttrDict()
    for key, value in dictionary.items():
        if isinstance(value, dict):
            ret[key] = dict2attrdict(value)
        elif isinstance(value, list):
            ret[key] = []
            for v in value:
                if isinstance(v, dict):
                    ret[key].append(dict2attrdict(v))
                else:
                    ret[key].append(v)
                # ret[key] = dict2attrdict(value)
        else:
            ret[key] = value
    return ret


def load_config(fpath):
    with open(fpath, "r") as stream:
        try:
            c = dict2attrdict(yaml.safe_load(stream))
            return c
        except Exception as ex:
            print(ex)
            return None


def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow())
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
        proc_name = win32process.GetModuleFileNameEx(handle, 0)
        return Path(proc_name).name
    except Exception as ex:
        print(ex)


def tick():
    global timer_start
    timer_start = time.time()


def tock():
    print(f'timer = {time.time()-timer_start}')


def Win32API_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()


SystemParametersInfoA = ctypes.windll.user32.SystemParametersInfoA
SystemParametersInfoA.argtypes = [
    ctypes.wintypes.UINT, ctypes.wintypes.UINT, ctypes.wintypes.LPVOID, ctypes.wintypes.UINT]
SystemParametersInfoA.restype = ctypes.wintypes.BOOL
SystemParametersInfoA.errcheck = Win32API_errcheck


def restore_system_cursor():

    win32api.ShowCursor(True)
    SystemParametersInfoA(87, 0, None, 2)
