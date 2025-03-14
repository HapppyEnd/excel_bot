import aiosqlite


async def create_table() -> None:
    """
    Creates the 'sites' table in the database if it does not exist.

    The table has the following columns:
        - id: INTEGER (Primary Key, Auto Increment)
        - title: TEXT (Not Null)
        - url: TEXT (Not Null)
        - xpath: TEXT (Not Null)

    Returns:
        None
    """

    async with aiosqlite.connect("sites.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        xpath TEXT NOT NULL)""")
        await conn.commit()


async def insert_data(data: list[dict[str, str]]) -> None:
    """
    Inserts data into the 'sites' table.

    Parameters:
        data (list of dict): List of dictionaries:
            - title (str): Title of the site.
            - url (str): URL of the site.
            - xpath (str): XPath expression for the price element.
    Returns:
        None
    """
    async with aiosqlite.connect("sites.db") as conn:
        cursor = await conn.cursor()
        for row in data:
            await cursor.execute("""
            INSERT INTO sites (title, url, xpath)
            VALUES (?, ?, ?)
            """, (row["title"], row["url"], row["xpath"]))
        await conn.commit()


async def fetch_data() -> list[tuple[int, str, str, str]]:
    """
    Fetches all data from the 'sites' table.

    Returns:
        list of tuples:
        Each tuple contains:
            - id (int): Unique identifier of the site.
            - title (str): Title of the site.
            - url (str): URL of the site.
            - xpath (str): XPath expression for the price element.
    """
    async with aiosqlite.connect("sites.db") as conn:
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM sites")
        return await cursor.fetchall()
