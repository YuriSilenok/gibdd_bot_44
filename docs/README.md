### Первичное развертывание

- `py -3.8 -m venv .venv`
- `.venv\Scripts\activate`
- `pip install -e .`
- создать файл `.env` c содержимым: `TOKEN="токен телеграм бота"`
- `py -m database.models`

### Очистка БД

- удалить файл `sqlite.db`
- `py -m database.models`

### Запуск

- `py main.py`
