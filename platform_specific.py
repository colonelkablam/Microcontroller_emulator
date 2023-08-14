def set_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        print("DPI awareness set to 1")
    except:
        print("DPI awareness unchanged")
        pass


from platform import system
def set_icon():
    platformD = system()
    if platformD == 'Darwin':
        return './assets/chip_mac.icns'

    elif platformD == 'Windows':
        return './assets/chip_windows.ico'

    else:
        return None
        print("not mac or widows OS")