from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id-new-item').send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item"
            )
        )
        self.browser.find_element_by_id('id-new-item').send_keys('Buy milk')
        self.browser.find_element_by_id('id-new-item').send_keys(Keys.ENTER)
        self.list_table_should_contain_row('1: Buy milk')

        self.browser.find_element_by_id('id-new-item').send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item"
            )
        )

        self.browser.find_element_by_id('id-new-item').send_keys('Make tea')
        self.browser.find_element_by_id('id-new-item').send_keys(Keys.ENTER)
        self.list_table_should_contain_row('1: Buy milk')
        self.list_table_should_contain_row('2: Make tea')