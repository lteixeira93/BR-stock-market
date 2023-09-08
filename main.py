from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import chrome, Keys


class stock_web_driver():
    def __init__(self):
        pass

    def driver_parser(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)

        with driver:
            driver.get("https://shorturl.at/hrGHQ")

            # time.sleep(5)

            print(driver.title)
            download_button = driver.find_element(By.ID, "botao_arquivo")
            # download_button.click()
            download_button.send_keys(Keys.ENTER)
            print("Button Clicked")

def main():
    stock_web_driver.driver_parser()


if __name__ == "__main__":
    main()
