### Предварительные требования

Что вам нужно установить для запуска проекта:

- Python (версия указана в файле `pyproject.toml`)
- [Poetry](https://python-poetry.org/docs/#installation)

### Установка

Шаги по установке и настройке вашего локального окружения:

1. Клонируйте репозиторий:

    ```bash
    git clone git@github.com:ragimov700/EduPlatform.git
    cd EduPlatform
    ```

2. Установите зависимости с помощью Poetry:

    ```bash
    poetry install
    ```

3. Создайте и активируйте виртуальное окружение с помощью Poetry:

    ```bash
    poetry shell
    ```

4. Настройте базу данных:

    ```bash
    cd backend
    python manage.py migrate
    ```

5. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

Теперь вы можете перейти по адресу `http://127.0.0.1:8000/` в вашем браузере и увидеть работающий проект.
