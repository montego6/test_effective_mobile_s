import consts

class UI:
    def __init__(self) -> None:
        self.command = None
    
    def get_next_command(self):
        self.command = int(input(consts.UI_COMMAND_PROMPT))