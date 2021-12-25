import win32api
import win32gui
import win32con


def get_screen_size() -> tuple:
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


def get_app_rect(hwnd: int) -> tuple:
    hr = win32gui.GetWindowRect(hwnd)
    return tuple((
        hr[0],
        hr[1],
        hr[2] - hr[0],
        hr[3] - hr[1]
    ))


def resize_app(hwnd: int, rect: tuple) -> None:
    win32gui.MoveWindow(hwnd, *rect, True)
