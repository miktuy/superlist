import os
from typing import Tuple, Any, Callable, Union, List

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.chrome_options import chrome_options

Locator = Tuple[By, str]
MAX_WAIT_S = 10
POLL_FREQUENCY_S = 0.1


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(options=chrome_options)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

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
