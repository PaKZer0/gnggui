from gui.gtkgui import run_gui

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    run_gui()
