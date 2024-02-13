import consts

if __name__ == '__main__':
    ui = UI()
    while ui.next_command != consts.UI_COMMAND_QUIT:
        ui.get_next_command()
