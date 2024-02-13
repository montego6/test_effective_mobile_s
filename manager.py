import consts
import os
from model import PhoneBookEntry

def get_last_id() -> int:
    """
    Get id of last entry in a file. If file is empty return 0
    """
    if not os.path.getsize('phonebook.txt'):
        return 0
    with open('phonebook.txt', "r") as file:
        for line in file:
            pass
        last_line = line
    return int(last_line.split(consts.TEXTFILE_SEPARATOR)[0])


def add_entry_to_file(entry: PhoneBookEntry) -> None:
    """
    Add one entry to the end of a phonebook file
    """
    with open('phonebook.txt', "a") as file:
        file.write(entry.to_string())