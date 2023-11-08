import pandas as pd
from selenium.webdriver.remote.webelement import WebElement


def print_full_dataframe(dataframe) -> None:
    r"""
    Print all dataframe fields.
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(dataframe)


def is_text_in_xpath(text: str, xpath: WebElement) -> bool:
    r"""
    Find if desired text is present in the provided XPATH.
    """
    if text in xpath.text:
        return True
    else:
        return False
