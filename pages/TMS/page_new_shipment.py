import re

from pages.page_base import BasePage
from playwright.sync_api import Page, expect

from pages.TMS.page_shipment import ShipmentPage


class NewShipmentPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.input_shipper_search = page.locator("#input_pickup_id1")
        self.input_consignee_search = page.locator("#input_consignee_id1")
        self.input_content = page.locator("#input_manifest_content1_1")
        self.input_pallet = page.locator("#input_manifest_pallet1_1")
        self.input_space = page.locator("#input_manifest_space1_1")
        self.input_piece = page.locator("#input_manifest_piece1_1")
        self.input_weight = page.locator("#input_manifest_weight1_1")
        self.select_class = page.locator("#input_manifest_class1_1")
        self.input_bill_to = page.locator("#input_billto_id1")
        self.text_quote_amount = page.locator("#input_consignee_quote_amount1")
        self.btn_sv_rt = page.locator("#btn_rate_shipment_new1")
        self.btn_add_order = page.get_by_text('ADD ORDER')

        self.options = page.locator("//*[contains(@style,'display: block')] >> .ui-menu-item")

    def navigate(self):
        self.page.goto("/dashboard_tms_order.php", wait_until="networkidle")

    def add_order(self, shipper, consignee) -> ShipmentPage:
        self.input_shipper_search.fill(shipper)
        expect(self.options.last).to_be_visible()
        self.options.nth(5).click()
        self.input_consignee_search.fill(consignee)
        expect(self.options.last).to_be_visible()
        self.options.nth(5).click()
        self.input_content.fill("Books")
        self.input_piece.fill("2")
        self.input_pallet.fill("2")
        self.input_space.fill("2")
        self.input_weight.fill("2")
        self.select_class.select_option("50")
        self.input_bill_to.fill("seven test")
        expect(self.options.last).to_be_visible()
        self.options.nth(-1).click()
        self.btn_sv_rt.click()
        expect(self.text_quote_amount).to_have_attribute("rate_amount", re.compile(r'.*?'), timeout=60000)
        with self.page.expect_popup() as popup_info:
            self.btn_add_order.click()
        new_page = popup_info.value
        new_page.wait_for_load_state()
        self.page = new_page
        return ShipmentPage(new_page)
