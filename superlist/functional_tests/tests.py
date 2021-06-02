import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_in_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id-new-item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item',
        )
        input_box.send_keys('Buy ostrich plum')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)  # ToDo: REMOVE THIS SHIT IN FUTURE!!!

        self.list_table_should_contain_row('1: Buy ostrich plum')

        input_box = self.browser.find_element_by_id('id-new-item')
        input_box.send_keys('Produce bead from ostrich plum')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)  # ToDo: REMOVE THIS SHIT IN FUTURE!!!

        self.list_table_should_contain_row('1: Buy ostrich plum')
        self.list_table_should_contain_row('2: Produce bead from ostrich plum')

        # self.fail('Stop test!')

    def list_table_should_contain_row(self, row_text: str):
        table = self.browser.find_element_by_id('id-list-table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
