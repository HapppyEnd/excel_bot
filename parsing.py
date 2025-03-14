from typing import Optional

import aiohttp
from lxml import html


async def parse_price(url: str, xpath: str) -> tuple[
    Optional[int], Optional[str]]:
    """
    Parses the price from a website using the provided XPath.

    Parameters:
        url (str): URL of the website to parse.
        xpath (str): XPath expression to locate the price element.
    Returns:
        tuple: Tuple containing:
            - int: Parsed price as integer, or `None` if parsing fails.
            - str: Error message if parsing fails, or `None` if success.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.text()
                tree = html.fromstring(content)

                price_elements = tree.xpath(xpath)
                if not price_elements:
                    return (
                        None,
                        f"Элемент с XPath {xpath} не найден на странице {url}")

                price_text = price_elements[0].strip()
                price = "".join([char for char in price_text if
                                 char.isdigit()])
                return int(price), None
        except Exception as e:
            return None, f"Ошибка при парсинге {url}: {e}"
