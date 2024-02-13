from abc import ABC, ABCMeta, abstractmethod
import consts
from manager import add_entry_to_file, get_last_id
from model import PhoneBookEntry

class UI:
    def __init__(self) -> None:
        self.input = None
        self.command = None
    
    def get_next_command(self):
        self.input = int(input(consts.UI_COMMAND_PROMPT))

    def command_handler(self):
        
        if self.input == 2:
            self.command = AddCommand()
        self.command.render()


class Command(ABC):
    @abstractmethod
    def render(self):
        pass


class AddCommand(Command):
    def render(self):
        entry = PhoneBookEntry()
        for field in consts.ADD_ENTRY_PROMTS.keys():
            value = input(consts.ADD_ENTRY_PROMTS[field])
            setattr(entry, field, value)
            while not entry.validate_field(field):
                print('Invalid format, try again')
                value = input(consts.ADD_ENTRY_PROMTS[field])
                setattr(entry, field, value)
        setattr(entry, 'id', str(get_last_id() + 1))
        add_entry_to_file(entry)