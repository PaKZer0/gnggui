from gui.gtkgui import run_gui
from migrator import run_migrations

if __name__ == '__main__':
    run_migrations()
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    run_gui()
