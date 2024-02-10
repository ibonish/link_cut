# Сервис для укорачивания ссылок

## Технологический стек

- Python 3.9
- **Веб-фреймворк:** Flask
- SQLAlchemy
- Flask-Migrate

## Начало работы

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ibonish/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В корневой директории создать файл .env и наполнить его:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Настроить базу данных:

```
flask db upgrade
```

Запустить проект командой:

```
flask run
```

## Возможности 

* Генерация коротких ссылок и связь их с исходными длинными ссылками
* Переадресация на исходный адрес при обращении к коротким ссылкам

## API 

* `/api/id/` — POST-запрос на создание новой короткой ссылки
* `/api/id/<short_id>/` — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.


Автор:

- [Скрябина Ольга](https://github.com/ibonish)