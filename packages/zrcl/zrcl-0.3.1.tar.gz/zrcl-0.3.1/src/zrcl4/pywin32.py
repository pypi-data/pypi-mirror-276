def get_pid_from_hwnd(hwnd):
    """Get the process ID given the handle of a window."""
    if not isinstance(hwnd, int):
        import pygetwindow as gw

        assert isinstance(hwnd, gw.Win32Window)
        hwnd = hwnd._hWnd

    try:
        import win32process

        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception as e:
        print(f"Error: {e}")
        return None
