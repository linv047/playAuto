from playwright.sync_api import Page

from pages.page_base import BasePage


class ShipmentPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.btn_epro = page.locator("[id^='btn_epro'] >> visible=true")
        self.btn_update_order = page.get_by_text("update order")
        self.input_pro_number = page.locator("[id^='input_consignee_pro'] >> visible=true")

    def get_pro_number(self) -> str:
        value = self.input_pro_number.input_value()
        if value != "":
            return value
        else:
            self.page.wait_for_timeout(2000)
            return self.input_pro_number.input_value()
