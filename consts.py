TEXTFILE_SEPARATOR = '|'

PAGE_COUNT = 5

UI_COMMAND_PROMPT = """
Выберите следующую комманду:
1 - Вывод записей справочника
2 - Добавление новой записи в справочник
3 - Редактирование записи в справочнике
4 - Поиск записи в справочнике
5 - Выход
"""

UI_SEARCH_ENTRIES_PROMPT = """
Выберите атрибуты для поиска(если несколько, то через пробел):
1 - id
2 - Имя
3 - Отчество
4 - Фамилия
5 - Место работы
6 - Рабочий телефон
7 - Личный телефон
"""

UI_SEARCH_ENTRIES_FILTER_PROMTS = {
    '1': "Введите id: ",
    '2': "Введите имя: ",
    '3': "Введите отчество: ",
    '4': "Введите фамилию: ",
    '5': "Введите место работы: ",
    '6': "Введите рабочий телефон: ",
    '7': "Введите мобильный телефон: ",
}

UI_FILTERS_MAPPING = {
    '1': 'id',
    '2': 'name',
    '3': 'second_name',
    '4': 'last_name',
    '5': 'employee',
    '6': 'work_phone',
    '7': 'mobile_phone'
}

UI_SEARCH_ENTRIES_EQ_CONTAINS_PROMPT = """
1 - Полное совпадение
2 - Частичное совпадение
"""

UI_SEARCH_ENTRIES_AND_OR_PROMPT = """
1 - Совпадение всех полей
2 - Совпадение любого поля
"""

UI_EDIT_ENTRY_ID_PROMPT = 'Введите id записи, которую хотите отредактировать: '

UI_EDIT_ENTRY_PROMPT = """
Выберите атрибуты для изменения(если несколько, то через пробел):
1 - Имя
2 - Отчество
3 - Фамилия
4 - Место работы
5 - Рабочий телефон
6 - Личный телефон
"""

UI_EDIT_ENTRY_NEW_VALUE_PROMTS = {
    '1': "Введите имя: ",
    '2': "Введите отчество: ",
    '3': "Введите фамилию: ",
    '4': "Введите место работы: ",
    '5': "Введите рабочий телефон: ",
    '6': "Введите мобильный телефон: ",
}

UI_EDIT_MAPPING = {
    '1': 'name',
    '2': 'second_name',
    '3': 'last_name',
    '4': 'employee',
    '5': 'work_phone',
    '6': 'mobile_phone'
}

UI_SHOW_COMMAND_PROMPT_NEXT_PAGE  = '1 - Следующая страница'
UI_SHOW_COMMAND_PROMPT_PREV_PAGE  = '2 - Предыдущая страница'
UI_SHOW_COMMAND_PROMPT_QUIT  = '9 - Выход в основное меню'


ADD_ENTRY_PROMTS = {
    'name': "Введите имя: ",
    'second_name': "Введите отчество: ",
    'last_name': "Введите фамилию: ",
    'employee': "Введите место работы: ",
    'work_phone': "Введите рабочий телефон: ",
    'mobile_phone': "Введите мобильный телефон: ",
}

TABLE_HEADER = ['id', 'Имя', 'Отчество', 'Фамилия', 'Место работы', 'Рабочий телефон', 'Личный телефон']

UI_COMMAND_SHOW = '1'
UI_COMMAND_ADD = '2'
UI_COMMAND_EDIT = '3'
UI_COMMAND_SEARCH = '4'
UI_COMMAND_QUIT = '5'

UI_SHOW_COMMAND_NEXT_PAGE = '1'
UI_SHOW_COMMAND_PREV_PAGE = '2'
UI_SHOW_COMMAND_EXIT = '9'