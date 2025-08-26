# Цитатник

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

**Цитатник** — веб-приложение для публикации, просмотра и оценки цитат. Пользователи могут:

- Смотреть случайную цитату
- Лайкать и дизлайкать цитаты
- Добавлять новые цитаты
- Просматривать топ-10 цитат

---

## Быстрый старт локально

1. Клонируйте репозиторий:

```
git clone https://github.com/Dxndigiden/solution_quotes.git
```

2. Перейдите в папку проекта:

```
cd solution_quotes/solution_quotes_project
```

3. Создайте и активируйте виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate
```

4. Установите зависимости:

```
pip install -r requirements.txt
```

5. Создайте файл `.env` в корне проекта пример `.env.example`:

```
# Окружение
DJANGO_ENV=development или production
# Секретный ключ Django (замени на свой)
SECRET_KEY=supersecretkey_dev
# Разрешённые хосты для dev
DJANGO_ALLOWED_HOSTS=localhost
# Часовой пояс
TIME_ZONE

# SQLite для разработки (остановлился на ней тк Postgres платно для деплоя)
SQLITE_NAME=db.sqlite3

# Для перехода на PostgreSQL
POSTGRES_USER=пользователь_бд
POSTGRES_PASSWORD=пароль_бд
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

6. Примените миграции и соберите статику:

```
python manage.py migrate
python manage.py collectstatic --no-input
```

7. Запустите сервер:

```
python manage.py runserver
```

---

## Доступ

Приложение доступно онлайн: [тык](https://dxndigiden.pythonanywhere.com/)

---

## Автор

Автор: [Dxndigiden](https://github.com/dxndigiden)

