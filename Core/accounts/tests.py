from django.test import TestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTestCase(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_log_in_as_admin(self):
        self.get_url('http://localhost:8000/')
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ml-3"))
        )
        element.click()
        self.fill_input_by_name('username', 'admin@gmail.com')
        self.fill_input_by_name('password', '123')
        self.click_button()

    def get_url(self, url):
        self.driver.get(url)

    def click_button(self):
        button = self.driver.find_element(value='button')
        button.click()

    def fill_input_by_name(self, name, text):
        input_element = self.driver.find_element(by=By.NAME, value=name)
        input_element.send_keys(text)
