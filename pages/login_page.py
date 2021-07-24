from .base_page import BasePage
from .locators import LoginAdminPageLocators, PagePaths, HomePageLocators
import allure


class LogingPage(BasePage):
    @allure.step('Авторизация администратора')
    def admin_authorization(self):
        self.logger.info('Авторизация администратора')
        self.open(url=PagePaths.LOGIN_ADMIN)
        self.check_form()
        self.enter_text(*LoginAdminPageLocators.LOGIN_ADMIN, text=LoginAdminPageLocators.TEXT_LOGIN)
        self.enter_text(*LoginAdminPageLocators.PASSWORD_ADMIN, text=LoginAdminPageLocators.TEXT_PASSWORD)
        self.click_to_element(*LoginAdminPageLocators.BUTTON_LOGIN)
        assert self.browser.find_element(*HomePageLocators.USER_PROFILE).get_attribute('alt') == 'John Doe', \
            'Не найдено имя авторизованного админа'

    @allure.step('Проверка формы авторизации')
    def check_form(self):
        self.logger.info('Проверка формы авторизации')
        self.waiting_for_element_present(*LoginAdminPageLocators.LOGIN_ADMIN)
        self.waiting_for_element_present(*LoginAdminPageLocators.PASSWORD_ADMIN)
        self.waiting_for_element_present(*LoginAdminPageLocators.BUTTON_LOGIN)

    @allure.step('Выход пользователя')
    def logout(self):
        self.logger.info('Выход пользователя')
        self.click_to_element(*HomePageLocators.LOGOUT_BUTTON)
