from playwright.sync_api import Page

from pages.page_base import BasePage


class DispatchPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.select_dispatch = page.locator("#input_dispatch_id")
        self.input_dispatch_start_date = page.locator("#input_dispatch_start_date")
        self.select_driver_company = page.locator("#input_driver_company")
        self.select_driver = page.locator("#input_driver_id")
        self.select_CTRL = page.locator("#input_warehouse_id")
        self.noy_msg = page.get_by_text("Displaying drivers working")
        self.btn_dispatch = page.locator("#btn_dispatch")
        self.select_stage = page.locator("#input_stage")

        self.input_direct_pickup_pro = page.locator("#input_direct_pickup_pro")

        self.trip_msg = page.locator("//a[contains(text(),'Trip #')]")
        self.tip_dispatch_successful = page.get_by_text("DISPATCH SUCCESSFUL")

    def navigate(self):
        # self.page.goto("/dashboard_tms_dispatch.php", wait_until="networkidle")
        self.page.goto("/dashboard_tms_dispatch.php")

