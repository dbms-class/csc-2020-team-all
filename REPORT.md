# Журнал

---

## 19.11.2020

**Senior**: Даниил Орешников
**Junior**: Ильяс Ишбаев

### Цели

- реализовать метод `get_price(country_id, week, max_price?, bed_count?)`

### Выполненные задачи

Основные
- реализован метод `get_price(country_id, week, max_price?, bed_count?)`
    - поля `apartment_id` и `apartment_name` заменены на `id` и `name` для консистентности с методами прошлой недели

Дополнительные
- `porject0` убран из ветки
- изменена верстка страницы [static.py](project8/static.py)

---

## 12.11.2020

**Senior**: Данил Дегтерев
**Junior**: Даниил Орешников

### Цели

- реализовать метод `countries()`
- реализовать метод `update_price(apartment_id, week, price)`
- реализовать метод `apartments(country_id?)`

### Выполненные задачи

Основные:
- реализован метод `countries()`
- реализован метод `update_price(apartment_id, week, price)`
- реализован метод `apartments(country_id?)`

Дополнительные:
- реализован метод `fill()` для запуска в db скрипта [project8.sql](project8/project8.sql)
- реализован метод `drop(table_name)` для `DROP TABLE`