import time
from typing import Tuple, Any, Callable, Union, List

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


Locator = Tuple[By, str]
MAX_WAIT_S = 10
POLL_FREQUENCY_S = 0.1


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_in_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        input_box = self.browser.find_element_by_id("id-new-item")
        self.assertEqual(
            input_box.get_attribute("placeholder"),
            "Enter a to-do item",
        )
        input_box.send_keys("Buy ostrich plum")
        input_box.send_keys(Keys.ENTER)

        self.list_table_should_contain_row("1: Buy ostrich plum")

        input_box = self.browser.find_element_by_id("id-new-item")
        input_box.send_keys("Produce bead from ostrich plum")
        input_box.send_keys(Keys.ENTER)

        self.list_table_should_contain_row("1: Buy ostrich plum")
        self.list_table_should_contain_row("2: Produce bead from ostrich plum")

        # self.fail('Stop test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id("id-new-item")
        input_box.send_keys("Buy peacock plum")
        input_box.send_keys(Keys.ENTER)
        self.list_table_should_contain_row("1: Buy peacock plum")

        user_url = self.browser.current_url
        self.assertRegex(user_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Chrome(options=chrome_options)

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock plum', page_text)
        self.assertNotIn('Produce bead from ostrich plum', page_text)

        input_box = self.browser.find_element_by_id("id-new-item")
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        self.list_table_should_contain_row("1: Buy milk")

        new_user_url = self.browser.current_url
        self.assertRegex(new_user_url, '/lists/.+')
        self.assertNotEqual(new_user_url, user_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock plum', page_text)
        self.assertIn('Buy milk', page_text)

    def list_table_should_contain_row(self, row_text: str):
        self._wait_for_condition(
            EC.visibility_of_element_located, (By.ID, "id-list-table"), "isn't visible"
        )
        rows = self._wait_for_condition(
            EC.visibility_of_any_elements_located, (By.TAG_NAME, "tr"), "isn't visible"
        )
        self.assertIn(row_text, [row.text for row in rows])

    def _wait_for_condition(
        self,
        condition: Callable[[Locator], Any],
        locator: Locator,
        message: str,
        timeout: int = MAX_WAIT_S,
    ) -> Union[WebElement, List[WebElement]]:
        try:
            wait = self._wait(timeout=timeout)
            element = wait.until(condition(locator))
        except TimeoutException:
            result_message = f"Element with locator `{locator}` {message}"
            raise TimeoutException(result_message)
        return element

    def _wait(
        self, timeout: int = MAX_WAIT_S, poll_frequency: float = POLL_FREQUENCY_S
    ) -> WebDriverWait:
        return WebDriverWait(self.browser, timeout, poll_frequency)
