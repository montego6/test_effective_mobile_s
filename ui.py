from abc import ABC, abstractmethod
from typing import List, Tuple
from rich.table import Table
from rich.console import Console
import consts
from manager import add_entry_to_file, get_last_id, read_all_entries, write_all_entries
from matcher import EntryMatcher
from model import PhoneBookEntry


class UI:
    """
    Main UI class, that handles input and delegate
    work to specified Command class
    """
    def __init__(self) -> None:
        self.input: str = None
        self.command: Command = None

    def get_next_command(self) -> None:
        self.input = input(consts.UI_COMMAND_PROMPT)

    def command_handler(self) -> None:
        if self.input == consts.UI_COMMAND_SHOW:
            self.command = ShowCommand()
        elif self.input == consts.UI_COMMAND_ADD:
            self.command = AddCommand()
        elif self.input == consts.UI_COMMAND_EDIT:
            self.command = EditCommand()
        elif self.input == consts.UI_COMMAND_SEARCH:
            self.command = SearchCommand()
        elif self.input == consts.UI_COMMAND_QUIT:
            self.command = QuitCommand()
        else:
            self.command = NotFoundCommand()
        self.command.render()


class Command(ABC):
    """Abstract Base class for all commands"""
    @abstractmethod
    def render(self):
        pass


class QuitCommand(Command):
    """
    Command for quit
    """
    def render(self) -> None:
        pass


class NotFoundCommand(Command):
    """
    Not found command, in case of unexpected input
    """
    def render(self) -> None:
        print("Неправильный ввод команды")


class AddCommand(Command):
    """
    Command for adding new entries
    """
    def render(self) -> None:
        entry: PhoneBookEntry = PhoneBookEntry()
        for field in consts.ADD_ENTRY_PROMTS.keys():
            value: str = input(consts.ADD_ENTRY_PROMTS[field])
            setattr(entry, field, value)
            while not entry.validate_field(field):
                print("Неправильный формат, повторите ввод")
                value = input(consts.ADD_ENTRY_PROMTS[field])
                setattr(entry, field, value)
        setattr(entry, "id", str(get_last_id() + 1))
        add_entry_to_file(entry)
        print("Запись успешно добавлена")


class TableMixin:
    """
    Mixin that provides logic
    for rendering entries in a table
    """
    def render_table(self, entries_data: List[PhoneBookEntry]) -> None:
        console: Console = Console()
        table: Table = Table(*consts.TABLE_HEADER)
        for entry in entries_data:
            table.add_row(*entry.get_field_values())
        console.print(table)


class ShowCommand(Command, TableMixin):
    """
    Command that shows all entries with paging
    """
    def render(self) -> None:
        data: list[str] = read_all_entries()
        page: int = 1
        prompt: str = ""
        choice: str = None
        while choice != consts.UI_SHOW_COMMAND_EXIT:
            page_data: List[str] = data[(page - 1) * consts.PAGE_COUNT:page * consts.PAGE_COUNT]
            other_data: List[str] = data[page * consts.PAGE_COUNT:]
            if other_data:
                prompt += consts.UI_SHOW_COMMAND_PROMPT_NEXT_PAGE
                prompt += "\n"
            if page != 1:
                prompt += consts.UI_SHOW_COMMAND_PROMPT_PREV_PAGE
                prompt += "\n"
            prompt += consts.UI_SHOW_COMMAND_PROMPT_QUIT
            prompt += "\n"
            page_entries: List[PhoneBookEntry] = [PhoneBookEntry().from_string(line) for line in page_data]
            self.render_table(page_entries)
            choice = input(prompt)
            prompt = ""
            if choice == consts.UI_SHOW_COMMAND_NEXT_PAGE:
                if other_data:
                    page += 1
            elif choice == consts.UI_SHOW_COMMAND_PREV_PAGE:
                if page > 1:
                    page -= 1
            elif choice == consts.UI_SHOW_COMMAND_EXIT:
                pass
            else:
                print("Неправильный ввод команды")


class SearchCommand(Command, TableMixin):
    """
    Command for entries searching with multiple filters
    """
    def render(self) -> None:
        search_choices: str = input(consts.UI_SEARCH_ENTRIES_PROMPT)
        if len(search_choices) > 1:
            choices: List[str] = search_choices.split()
        else:
            choices: List[str] = [search_choices]

        for choice in choices:
            if choice not in consts.UI_FILTERS_MAPPING.keys():
                print("Неверно указан атрибут для поиска")
                break
        else:
            filters: List[Tuple[str, str]] = [
                (
                    consts.UI_FILTERS_MAPPING[choice],
                    input(consts.UI_SEARCH_ENTRIES_FILTER_PROMTS[choice]),
                )
                for choice in choices
            ]

            while (
                eq_contains_choice := input(consts.UI_SEARCH_ENTRIES_EQ_CONTAINS_PROMPT)
            ) not in ["1", "2"]:
                print("Выберите 1 или 2")
            eq_contains = True if eq_contains_choice == 1 else False

            while (
                and_or_choice := input(consts.UI_SEARCH_ENTRIES_AND_OR_PROMPT)
            ) not in ["1", "2"]:
                print("Выберите 1 или 2")
            and_or = True if and_or_choice == 1 else False

            raw_entries: list[str] = read_all_entries()
            all_entries: list[PhoneBookEntry] = [
                PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries
            ]
            filtered_entries: List[PhoneBookEntry] = [
                entry
                for entry in all_entries
                if EntryMatcher(entry).match(filters, eq_contains, and_or)
            ]
            self.render_table(filtered_entries)


class EditCommand(Command, TableMixin):
    """
    Command for entry editing
    """
    def render(self) -> None:
        id: str = input(consts.UI_EDIT_ENTRY_ID_PROMPT)
        raw_entries: list[str] = read_all_entries()
        all_entries: list[PhoneBookEntry] = [
            PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries
        ]
        entry_to_edit: PhoneBookEntry = None
        for entry in all_entries:
            if entry.id == id:
                entry_to_edit = entry
        if not entry_to_edit:
            print("Записи с таким id не существует")
        else:
            self.render_table([entry_to_edit])

            edit_choices: str = input(consts.UI_EDIT_ENTRY_PROMPT)
            if len(edit_choices) > 1:
                choices: List[str] = edit_choices.split()
            else:
                choices: List[str] = [edit_choices]

            for choice in choices:
                if choice not in consts.UI_EDIT_ENTRY_NEW_VALUE_PROMTS.keys():
                    print("Неверно указан номер атрибута")
                    break
            else:
                for choice in choices:
                    new_value: str = input(consts.UI_EDIT_ENTRY_NEW_VALUE_PROMTS[choice])
                    setattr(entry_to_edit, consts.UI_EDIT_MAPPING[choice], new_value)
                    while not entry_to_edit.validate_field(
                        consts.UI_EDIT_MAPPING[choice]
                    ):
                        print("Неправильный формат поля, введите снова")
                        new_value = input(consts.UI_EDIT_ENTRY_NEW_VALUE_PROMTS[choice])
                        setattr(
                            entry_to_edit, consts.UI_EDIT_MAPPING[choice], new_value
                        )
                print("Запись успешно отредактирована")
                write_all_entries(all_entries)
