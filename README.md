## Тестовое задание для компании Effective Mobile

## Задание
Создать консольное приложение, с помощью которого можно вести телефонную книгу: добавлять новые записи в справочник, выводить все записи на экран, искать по записям, редактировать записи. Телефонная книга должна быть в текстовом формате.

## Решение
С помощью dataclass-а создана модель записи справочника, созданы методы модели для валидации данных с помощью регулярных выражений, преобразования модели в строку для последующей записи в текстовый файл, создания модели из записей в текстовом файле. Разработан консольный интерфейс, чтобы выводить данные в виде таблицы использована вспомогательная библиотека Rich

## UI

### 1
Вывод всех записей справочника постранично. 

1 - Следующая страница

2 - Предыдущая страница

9 - Выход в основное меню

### 2
Добавление новой записи в справочник. По порядку будут запрошены все атрибуты(имя, телефон и т.д.). Если введенное значение не проходит валидацию регулярным выражением, выскочит ошибка неправильного ввода и будет предложено ввести новое значение

### 3
Редактирование записи в справочнике. Сначала запрашивается id записи, которую будем редактировать. Если запись найдена, то нужно будет ввести атрибуты, которые хотим отредактировать, можно ввести несколько атрибутов через пробел. Затем для атрибутов необходимо будет ввести новые значения, которые так же валидируются регулярным выражением

### 4
Поиск записи в справочнике. Сначала выбираем атрибуты, по которым будет производитьс поиск(можно ввести несколько значений через пробел), потом указываем значения для этих атрибутов. Затем нужно ввести параметры поиска: полное совпадение или частичное, совпадение всех фильтров или любого выбранного.

### 5
Выход

## Запус приложения
Сначала в корне проекта создадим виртуальное окружение и активируем его:
```
python3 -m venv venv
source venv/bin/activate
```
Затем установим все зависимости проекта, отдав следующую команду:
```
pip install -r requirements.txt
```
Запускаем приложение
```
python3 main.py
```
