from abc import ABC, ABCMeta, abstractmethod
import consts
from manager import add_entry_to_file, get_last_id, read_all_entries
from model import PhoneBookEntry
from rich.table import Table
from rich.console import Console

class UI:
    def __init__(self) -> None:
        self.input = None
        self.command = None
    
    def get_next_command(self):
        self.input = int(input(consts.UI_COMMAND_PROMPT))

    def command_handler(self):
        if self.input == 1:
            self.command = ShowCommand()
        elif self.input == 2:
            self.command = AddCommand()
        elif self.input == 5:
            self.command = QuitCommand()
        self.command.render()


class Command(ABC):
    @abstractmethod
    def render(self):
        pass


class QuitCommand(Command):
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


class ShowCommand(Command):
    def render(self):
        console = Console()
        data: list[str] = read_all_entries()
        page = 1
        prompt = ''
        choice = None
        while choice != 9:
            page_data = data[(page-1)*consts.PAGE_COUNT:page*consts.PAGE_COUNT]
            other_data = data[page*consts.PAGE_COUNT:]
            if other_data:
                prompt += consts.UI_SHOW_COMMAND_PROMPT_NEXT_PAGE
                prompt += '\n'
            if page != 1:
                prompt += consts.UI_SHOW_COMMAND_PROMPT_PREV_PAGE
                prompt += '\n'
            prompt += consts.UI_SHOW_COMMAND_PROMPT_QUIT
            prompt += '\n'
            self.render_table(page_data, console)
            choice = int(input(prompt))
            prompt = ''
            if choice == 1:
                if other_data:
                    page += 1
            elif choice == 2:
                if page > 1:
                    page -= 1

    def render_table(self, entries_data, console):
        table: Table = Table(*consts.TABLE_HEADER)
        for line in entries_data:
            entry: PhoneBookEntry = PhoneBookEntry().from_string(line)
            table.add_row(*entry.get_field_values())
        console.print(table)