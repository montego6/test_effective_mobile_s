from abc import ABC, ABCMeta, abstractmethod
import consts
from manager import add_entry_to_file, get_last_id, read_all_entries
from matcher import EntryMatcher
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
        elif self.input == 4:
            self.command = SearchCommand()
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


class TableMixin:
    def render_table(self, entries_data):
        console = Console()
        table: Table = Table(*consts.TABLE_HEADER)
        for entry in entries_data:
            table.add_row(*entry.get_field_values())
        console.print(table)


class ShowCommand(Command, TableMixin):
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
            page_entries = [PhoneBookEntry().from_string(line) for line in page_data]
            self.render_table(page_entries)
            choice = int(input(prompt))
            prompt = ''
            if choice == 1:
                if other_data:
                    page += 1
            elif choice == 2:
                if page > 1:
                    page -= 1

    


class SearchCommand(Command, TableMixin):
    def render(self):
        search_choices = input(consts.UI_SEARCH_ENTRIES_PROMPT)
        if len(search_choices) > 1:
            choices = search_choices.split(' ')
        else:
            choices = [search_choices]

        filters = [(consts.UI_FILTERS_MAPPING[choice], input(consts.UI_SEARCH_ENTRIES_FILTER_PROMTS[choice])) for choice in choices]

        while (eq_contains_choice := input(consts.UI_SEARCH_ENTRIES_EQ_CONTAINS_PROMPT)) not in ['1', '2']:
            print('Выберите 1 или 2')
        eq_contains = True if eq_contains_choice == 1 else False

        while (and_or_choice := input(consts.UI_SEARCH_ENTRIES_AND_OR_PROMPT)) not in ['1', '2']:
            print('Выберите 1 или 2')
        and_or = True if and_or_choice == 1 else False

        raw_entries: list[str] = read_all_entries()
        all_entries: list[PhoneBookEntry] = [
        PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries
        ]
        filtered_entries =  [
        entry
        for entry in all_entries
        if EntryMatcher(entry).match(filters, eq_contains, and_or)
    ]
        self.render_table(filtered_entries)