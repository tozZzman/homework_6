import os
import sys
import pytest
from selenium import webdriver
import logging
import allure

sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))), '..')))

from pages.login_page import LogingPage
from pages.locators import ProductsPageLocators, HomePageLocators
from pages.product_page import ProductPage

logging.basicConfig(level=logging.INFO, filename='../logs/log.log', format='%(levelname)s %(asctime)s %(message)s')


def pytest_addoption(parser):
    parser.addoption('--browser',
                     action='store',
                     help='Browser selection flag',
                     choices=['chrome', 'firefox', 'opera'],
                     default='chrome')
    parser.addoption('--url',
                     action='store',
                     help='Flag for selecting url',
                     default='https://demo.opencart.com/')
    parser.addoption('--executor',
                     action='store',
                     help='Flag for selecting host',
                     default='192.168.31.110')
    parser.addoption('--bversion',
                     action='store',
                     help='Flag for selecting version browser',
                     default='90')
    parser.addoption('--vnc',
                     action='store_true',
                     help='Flag for vnc connection',
                     default=True)
    parser.addoption('--video',
                     action='store_true',
                     help='Flag for video recording',
                     default=False)


@pytest.fixture(scope='function')
def browser(request):
    bwr = request.config.getoption('--browser')
    logger = logging.getLogger('BrowserLogger')
    executor = request.config.getoption('--executor')
    version = request.config.getoption('--bversion')
    vnc = request.config.getoption('--vnc')
    video = request.config.getoption('--video')

    logger.info(f'====== Запущен тест {request.node.name} ======')

    if executor == 'local':
        if bwr == 'chrome':
            caps = {'goog.chromeOptions': {}}
            driver = webdriver.Chrome(desired_capabilities=caps)
        elif bwr == 'firefox':
            driver = webdriver.Firefox()
        elif bwr == 'opera':
            driver = webdriver.Opera()
        else:
            raise ValueError(f"Driver not suported: {bwr}")
    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        caps = {
            'browserName': bwr,
            'browserVersion': version,
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": video
            }
        }

        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps
        )
        # driver.maximize_window()

    def fin():
        driver.quit()
        logger.info('====== Тест завершен ======')

    request.addfinalizer(fin)

    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode):
                if 'browser' in item.fixturenames:
                    web_driver = item.funcargs['browser']
                else:
                    print('Fail to take screen-shot')
                    return
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))


@pytest.fixture(scope='function')
def url(request):
    return request.config.getoption('--url')


@pytest.fixture(scope='function')
def admin(browser, request):
    client = LogingPage(browser)
    client.admin_authorization()

    request.addfinalizer(client.logout)


@pytest.fixture(scope='function')
def add_product(browser, admin):
    client = LogingPage(browser)
    client.click_to_element(*HomePageLocators.CATALOG)
    client.click_to_element(*HomePageLocators.PRODUCTS)
    client = ProductPage(browser)
    client.add_product(name=ProductsPageLocators.PRODUCT, meta='test', model='test')
    client.check_the_product_on_the_list(name=ProductsPageLocators.PRODUCT)
