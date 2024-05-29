import typing
import screeninfo
import pygetwindow as gw


def get_screen_dimensions(monitor_index=0):
    monitors = screeninfo.get_monitors()
    if monitor_index < 0 or monitor_index >= len(monitors):
        raise ValueError("Invalid monitor index")
    monitor = monitors[monitor_index]
    # Return both dimensions and the position of the monitor
    return (monitor.width, monitor.height, monitor.x, monitor.y)


def get_wnds_monitor(wnd: gw.Window):
    """Determine which monitor a window is currently on based on its position"""
    # (left, top, width, height)
    # wnd midpoint = (left + width / 2, top + height / 2)
    midpoint = (wnd.left + wnd.width / 2, wnd.top + wnd.height / 2)
    for monitor in screeninfo.get_monitors():
        if (
            monitor.x <= midpoint[0] < monitor.x + monitor.width
            and monitor.y <= midpoint[1] < monitor.y + monitor.height
        ):
            return monitor
    return None


def get_primary_monitor():
    for monitor in screeninfo.get_monitors():
        if monitor.is_primary:
            return monitor

    raise ValueError("No primary monitor found")


def wnd_on_monitor(wnd: gw.Window):
    monitor = get_wnds_monitor(wnd)
    assert monitor
    return monitor


def wnd_to_monitor(
    wnd: gw.Window,
    monitor: typing.Union[screeninfo.Monitor, int] = None,
    coord: typing.Tuple[int, int] = None,
):
    if monitor is None:
        monitor = get_primary_monitor()

    if isinstance(monitor, int):
        monitor = screeninfo.get_monitors()[monitor]

    if coord is None:
        coord = (monitor.x, monitor.y)

    wnd.move(coord[0], coord[1])


def wnd_to_primary(wnd: gw.Window = None):
    if wnd is None:
        wnd = gw.getActiveWindow()
    wnd_to_monitor(wnd, get_primary_monitor())
