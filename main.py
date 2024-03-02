from interface import gui
from first_time_setup import first_time_setup
from config_manager import get_value


def main():
    """Checks if first_time_setup is set to True in ini file, then opens GUI."""
    setup = get_value('VALUES', 'first_time_setup')
    if setup:
        first_time_setup()
        gui()
    else:
        gui()


if __name__ == '__main__':
    main()
