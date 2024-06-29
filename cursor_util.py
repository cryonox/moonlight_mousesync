import win32con

from win32gui import LoadCursor, GetCursorInfo
import win32gui


class Cursor(object):
    @classmethod
    def from_name(cls, cursor_name):
        if cursor_name in DEFAULT_CURSORS:
            return DEFAULT_CURSORS[cursor_name]
        return DEFAULT_CURSORS['ARROW']

    @classmethod
    def from_handle(cls, handle):
        for k,v in DEFAULT_CURSORS.items():
            if v.handle == handle:
                return k
        return 'ARROW'
    @classmethod
    def load_custom(cls,type):
        ret = Cursor()
        handle = win32gui.LoadImage(0, "cursors/empty.cur", win32con.IMAGE_CURSOR, 
                                    32, 32, win32con.LR_LOADFROMFILE)
        ret.type = type
        ret.handle = handle
        return ret
    
    def __init__(self, cursor_type=None, handle=None):
        if handle is None and cursor_type is not None:
            handle = LoadCursor(0, cursor_type)
        self.type = cursor_type
        self.handle = handle



DEFAULT_CURSORS = {'APPSTARTING': Cursor(win32con.IDC_APPSTARTING),
                   'ARROW': Cursor(win32con.IDC_ARROW),
                   'CROSS': Cursor(win32con.IDC_CROSS),
                   'HAND': Cursor(win32con.IDC_HAND),
                   'HELP': Cursor(win32con.IDC_HELP),
                   'IBEAM': Cursor(win32con.IDC_IBEAM),
                   'ICON': Cursor(win32con.IDC_ICON),
                   'NO': Cursor(win32con.IDC_NO),
                   'SIZE': Cursor(win32con.IDC_SIZE),
                   'SIZEALL': Cursor(win32con.IDC_SIZEALL),
                   'SIZENESW': Cursor(win32con.IDC_SIZENESW),
                   'SIZENS': Cursor(win32con.IDC_SIZENS),
                   'SIZENWSE': Cursor(win32con.IDC_SIZENWSE),
                   'SIZEWE': Cursor(win32con.IDC_SIZEWE),
                   'UPARROW': Cursor(win32con.IDC_UPARROW),
                   'WAIT': Cursor(win32con.IDC_WAIT)}


def get_current_cursor():
    curr_cursor_handle = GetCursorInfo()[1]
    return Cursor.from_handle(curr_cursor_handle)
