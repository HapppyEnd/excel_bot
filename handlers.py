import pandas as pd
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import fetch_data, insert_data
from parsing import parse_price

router = Router()


@router.message(Command("start"))
async def start(message: Message) -> None:
    """
        Handles the /start command and displays a welcome message with
        inline buttons.

        Parameters:
            message (Message): The message object from the user.
        Returns:
            None
        """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Загрузить файл", callback_data="start"),
        InlineKeyboardButton(text="Средняя цена", callback_data="average")
    )

    await message.answer(
        "Здравствуйте! Выберите действие:",
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(lambda query: query.data in ["start", "average"])
async def handle_inline_buttons(query: types.CallbackQuery) -> None:
    """
     Handles inline button clicks.

     Parameters:
         query (CallbackQuery): Callback query object from inline button
     Returns:
         None
     """
    if query.data == "start":
        await query.message.answer(
            "Отправьте Excel-файл с данными о сайтах.")
    elif query.data == "average":
        await average_price(query.message)
    await query.answer()


@router.message(
    lambda message: message.document and message.document.file_name.endswith(
        (".xlsx", ".xls")))
async def handle_file(message: Message) -> None:
    """
    Processes the uploaded Excel file, validates its content,
    and saves the data to the database.

    Parameters:
        message (Message): Message object containing the uploaded file.
    Returns:
        None
    """
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    await message.bot.download_file(file_path, "data.xlsx")

    try:
        df = pd.read_excel("data.xlsx")

        required_columns = {"title", "url", "xpath"}
        if not required_columns.issubset(df.columns):
            await message.answer(
                "Файл должен содержать столбцы: title, url, xpath."
            )
            return

        if df[["title", "url", "xpath"]].isnull().any().any():
            await message.answer(
                "Файл содержит пустые значения в столбцах title, url или "
                "xpath.")
            return

        if df["url"].duplicated().any():
            await message.answer("Файл содержит дубликаты в столбце url.")
            return

        formatted_data = "Содержимое файла:\n\n"
        for _, row in df.iterrows():
            formatted_data += (
                f"<b>Название:</b> {row['title']}\n"
                f"<b>Ссылка:</b> {row['url']}\n"
                f"<b>XPath:</b> <code>{row['xpath']}</code>\n\n"
            )

        await message.answer(formatted_data, parse_mode="HTML")
        await insert_data(df.to_dict("records"))
        await message.answer("Данные успешно сохранены в базу данных.")

    except pd.errors.EmptyDataError:
        await message.answer("Файл пуст или не содержит данных.")
    except pd.errors.ParserError:
        await message.answer("Файл не является корректным Excel-файлом.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке файла: {e}")


@router.message(lambda message: message.document)
async def handle_unsupported_file(message: Message) -> None:
    """
     Handles unsupported file formats that are not Excel files.

     Parameters:
         message (Message): Message object containing the uploaded file.
     Returns:
         None
     """
    if not message.document.file_name.endswith((".xlsx", ".xls")):
        await message.answer(
            "Поддерживаются только файлы в формате Excel (.xlsx или .xls).")


@router.message(Command("average"))
async def average_price(message: Message) -> None:
    """
    Calculates the average price based on data fetched from the database
    and parsed from websites.

    Parameters:
        message (Message): Message object from the user.
    Returns:
        None
    """
    sites = await fetch_data()

    if not sites:
        await message.answer("В базе данных нет сайтов.")
        return

    results = []
    errors = []

    for site in sites:
        title, url, xpath = site[1], site[2], site[3]
        price, error = await parse_price(url, xpath)
        if error:
            errors.append(error)
        elif price:
            results.append((title, price))

    if errors:
        await message.answer("Ошибки при парсинге:\n" + "\n".join(errors))

    if results:
        avg_price = sum(price for _, price in results) / len(results)
        await message.answer(
            f"Средняя цена зюзюблика: {avg_price:.2f} руб.")
    else:
        await message.answer("Не удалось получить цены.")
