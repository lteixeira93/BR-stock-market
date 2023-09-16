import warnings

from WebDriver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # TODO: Add try catch, multithreading, UT
    stock_web_driver = WebDriver()
    stock_web_driver.get_stocks_table()


if __name__ == "__main__":
    main()
