from pages.product_page import ProductPage
from pages.locators import HomePageLocators, ProductsPageLocators
from pages.login_page import LogingPage
import allure


@allure.title('Добавление нового продукта под админом')
def test_adding_a_product_under_admin(browser, admin):
    client = LogingPage(browser)
    client.click_to_element(*HomePageLocators.CATALOG)
    client.click_to_element(*HomePageLocators.PRODUCTS)
    client = ProductPage(browser)
    client.add_product(name=ProductsPageLocators.PRODUCT, meta='test', model='test')
    client.check_the_product_on_the_list(name=ProductsPageLocators.PRODUCT)


@allure.title('Удаление продукта под админом')
def test_remove_a_product_under_admin(browser, add_product):
    client = ProductPage(browser)
    client.remove_products(name=ProductsPageLocators.PRODUCT)
    client.check_the_product_not_on_the_list(name=ProductsPageLocators.PRODUCT)
