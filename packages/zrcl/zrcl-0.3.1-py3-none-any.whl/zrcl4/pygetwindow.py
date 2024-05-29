import os
import platform
from time import sleep
import pygetwindow as gw
import typing
from .screeninfo import get_screen_dimensions


def activate_wnd(wnd: gw.Window):
    try:
        if wnd.isActive:
            return
        wnd.activate()
    except gw.PyGetWindowException:
        pass


def get_window_pos(wnd: gw.Window) -> typing.Tuple[float, float, float, float]:
    return (wnd.left, wnd.top, wnd.width, wnd.height)


def grid_orientation(
    wnds: typing.List[gw.Window],
    row: int,
    col: int,
    maxwidth: float | None = None,
    maxheight: float | None = None,
    minwidth: float | None = None,
    minheight: float | None = None,
    monitor: int = 0,
    sleepTime: float = 0.2,
):

    screen_width, screen_height, monitor_x, monitor_y = get_screen_dimensions(
        monitor_index=monitor
    )
    num_windows = len(wnds)
    if num_windows == 0 or row == 0 or col == 0:
        return  # Early return if invalid input

    window_width = screen_width // col
    window_height = screen_height // row

    # Apply max and min dimensions
    if maxwidth is not None:
        window_width = min(window_width, maxwidth)
    if maxheight is not None:
        window_height = min(window_height, maxheight)
    if minwidth is not None:
        window_width = max(window_width, minwidth)
    if minheight is not None:
        window_height = max(window_height, minheight)

    for index, window_instance in enumerate(wnds):
        window_instance: gw.Win32Window
        new_x = (index % col) * window_width + monitor_x
        new_y = (index // col) * window_height + monitor_y

        activate_wnd(window_instance)
        window_instance.resizeTo(window_width, window_height)
        window_instance.moveTo(new_x, new_y)

        if index == row * col - 1:
            break

        sleep(sleepTime)


def get_process_wnds(processname: str) -> typing.List[gw.Window]:
    if not platform.system() == "Windows":
        raise NotImplementedError

    procs = []
    import psutil

    for proc in psutil.process_iter():
        if proc.name().startswith(processname):
            procs.append(proc)

    procIds = [proc.pid for proc in procs]
    import win32process

    wnds = []
    for wnd in gw.getAllWindows():
        wnd: gw.Win32Window

        _, winpid = win32process.GetWindowThreadProcessId(wnd._hWnd)

        if winpid in procIds:
            wnds.append(wnd)
    return wnds


def get_visible_process_wnds(processname: str):
    return [
        wnd for wnd in get_process_wnds(processname) if wnd.height > 0 and wnd.width > 0
    ]


def refetch_wnd(wnd: gw.Window) -> gw.Window:
    candidates = gw.getWindowsWithTitle(wnd.title)
    if len(candidates) == 1:
        return candidates[0]

    for candidate in candidates:
        if platform.system() == "Windows":
            if candidate._hWnd == wnd._hWnd:
                return candidate
        else:
            return candidate
