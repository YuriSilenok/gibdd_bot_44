### Первичное развертывание приложения

py -3.8 -m venv .venv
.venv\Scripts\activate
pip install -e .
py -m database.models

### Очистка БД

удалить файл sqlite.db
py -m database.models

### Запуск

py main.py
