# Бот для добавления сайтов в базу данных

Этот проект представляет собой Telegram-бота, который позволяет пользователям
загружать Excel-файлы с данными о сайтах и сохранять данные в базу данных SQLite.

---

## Основные функции

1. **Загрузка Excel-файлов**:
    - Пользователь загружает файл с колонками: `title`, `url`, `xpath`.
    - Бот проверяет файл на корректность и сохраняет данные в базу данных.
2. **Вывод содержимого файла**:
    - Бот открывает файл с помощью библиотеки `pandas` и выводит его содержимое
      пользователю.
3. **Сохранение данных**:
    - Данные из файла сохраняются в локальную базу данных SQLite.

---

## Дополнительная функциональность

1. **Парсинг цен**:
    - Бот использует XPath для извлечения цен с указанных сайтов.
    - Учитывает возможность наличия пробелов, символов валют и других
      нечисловых символов.
2. **Средняя цена**:
    - Бот вычисляет среднюю цену зюзюблика по всем сайтам и выводит её
      пользователю.

---

## Технологии

- **Python 3.12**
- **aiogram**: Для работы с Telegram API.
- **pandas**: Для обработки Excel-файлов.
- **aiosqlite**: Для работы с базой данных SQLite.
- **aiohttp**: Для выполнения HTTP-запросов (опционально, для парсинга).
- **lxml**: Для парсинга HTML с использованием XPath.

---

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/HapppyEnd/excel_bot.git
   cd excel_bot
   ```
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
   ```
3. Создайте файл .env в корне проекта и добавьте туда токен вашего бота:
    ```bash
    BOT_TOKEN=ваш-токен
    ```
4. Запустите бота:

    ```bash
    python main.py
   ```
---
## Запуск с Docker
1. Убедитесь, что у вас установлен `Docker` и `Docker Compose`.

2. Соберите и запустите контейнер:

   ```bash
   docker-compose up --build
   ```

---

## Использование

1. Запуск бота:

   Отправьте команду `/start` в Telegram.
   Бот отправит 2 кнопки:
    - **Загрузить файл**: Для загрузки Excel-файла.
    - **Средняя цена**: Для вычисления средней цены зюзюблика.

2. Загрузка файла:

   Нажмите кнопку `Загрузить файл`.
   Отправьте Excel-файл с колонками: `title`, `url`, `xpath`.

3. Проверка файла:

   Бот проверит файл на корректность и выведет его содержимое.

4. Сохранение данных:

   Если файл корректен, бот сохранит данные в базу данных.

5. Средняя цена:

   Нажмите кнопку `Средняя цена`.
   Бот вычислит среднюю цену зюзюблика по всем сайтам и выведет её
   пользователю.

---

## Пример файла Excel

| title        | url                        | xpath                 |
|--------------|----------------------------|-----------------------|
| Example Site | https://example.com        | //div[@class='price'] |
| Another Site | https://anotherexample.com | //span[@id='price']   |

