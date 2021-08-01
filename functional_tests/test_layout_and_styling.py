from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id("id-new-item")
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.list_table_should_contain_row("1: testing")
        input_box = self.browser.find_element_by_id("id-new-item")
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
