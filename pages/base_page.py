from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import allure


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(type(self).__name__)

    @allure.step('Выполнен переход по ссылке: {url}')
    def open(self, url):
        self.logger.info(f'Выполнен переход по ссылке: {url}')
        self.browser.get(url)

    @allure.step('Проверка наличия заголовка страницы "{title}" с таймаутом "{timeout}"')
    def check_title(self, title, timeout):
        self.logger.info(f'Проверка наличия заголовка страницы "{title}" с таймаутом {timeout} сек.')
        try:
            wait = WebDriverWait(driver=self.browser, timeout=timeout)
            wait.until(EC.title_is(title=title))
        except TimeoutException:
            self.logger.info('Заголовок не был найден')
            raise TimeoutError("Не дождались заголовка страницы")

    @allure.step('Ожидание отображения элемента "{what}" с таймаутом {timeout} сек.')
    def waiting_for_element_present(self, how, what, timeout=2):
        self.logger.info(f'Ожидание отображения эелемента "{what}" с таймаутом {timeout} сек.')
        try:
            wait = WebDriverWait(driver=self.browser, timeout=timeout)
            wait.until(EC.visibility_of_element_located((how, what)))
        except TimeoutException:
            raise TimeoutError(f"Элемент не был найден в течение {timeout} секунд(-ы)")

    @allure.step('Ожидание скрытия текста "{text}" с таймаутом {timeout} сек.')
    def waiting_for_text_not_present(self, how, what, text, timeout=2):
        self.logger.info(f'Ожидание скрытия текста "{text}" с таймаутом "{timeout}"')
        try:
            wait = WebDriverWait(driver=self.browser, timeout=timeout)
            wait.until_not(EC.text_to_be_present_in_element((how, what), text))
        except TimeoutException:
            raise TimeoutError(f"Текст отображался в течение {timeout} секунд(-ы)")

    @allure.step('Ожидание кликабельности элемента "{what}" с таймаутом {timeout} сек.')
    def waiting_for_element_to_be_clickable(self, how, what, timeout=2):
        self.logger.info(f'Ожидание кликабельности элемента "{what}" с таймаутом "{timeout}"')
        try:
            wait = WebDriverWait(driver=self.browser, timeout=timeout)
            wait.until(EC.element_to_be_clickable((how, what)))
        except TimeoutException:
            raise TimeoutError(f"Элемент был не кликабелен в течение {timeout} секунд(-ы)")

    @allure.step('Ожидание отображения текста "{text}" с таймаутом {timeout} сек.')
    def waiting_for_text_present(self, how, what, text, timeout=2):
        self.logger.info(f'Ожидание отображения текста "{text}" с таймаутом "{timeout}"')
        try:
            wait = WebDriverWait(driver=self.browser, timeout=timeout)
            wait.until(EC.text_to_be_present_in_element((how, what), text))
        except TimeoutException:
            raise TimeoutError(f"Текст не был найден в течение {timeout} секунд(-ы)")

    @allure.step('Клик по элементу "{what}"')
    def click_to_element(self, how, what):
        self.logger.info(f'Выполнен клик по элементу: "{what}"')
        self.waiting_for_element_to_be_clickable(how, what)
        self.browser.find_element(how, what).click()

    @allure.step('Ввод текста "{text}"')
    def enter_text(self, how, what, text):
        self.logger.info(f'Выполнен ввод текста: "{text}"')
        self.waiting_for_element_present(how, what)
        self.browser.find_element(how, what).send_keys(text)
