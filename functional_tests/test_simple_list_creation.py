from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from functional_tests.chrome_options import chrome_options


class NewVisitorTest(FunctionalTest):

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
