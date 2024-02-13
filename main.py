import consts
from ui import UI


if __name__ == '__main__':
    ui = UI()
    while ui.command != consts.UI_COMMAND_QUIT:
        ui.get_next_command()
        ui.command_handler()