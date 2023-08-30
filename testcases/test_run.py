import datetime

import pytest
from playwright.sync_api import expect

from pages.TMS.page_new_shipment import NewShipmentPage


class TestRun:

    @pytest.fixture(autouse=True)
    def start_for_each(self, page, global_map, environ, context):

        # sql = "SELECT * FROM tms_order WHERE tms_order_pro = '1001121967'"
        # self.db_tool = DBTool(environ.database_info)
        # self.db_tool.execute_sql(sql)

        self.page_new_shipment = NewShipmentPage(page)
        self.page_new_shipment.navigate()
        # self.page_dispatch = DispatchPage(page)

    def test_order(self):
        print("run.....")
        self.page_shipment = self.page_new_shipment.add_order("STAR", "SEVEN")
        self.page_shipment.btn_epro.click()
        pro_num = self.page_shipment.get_pro_number()
        print(f"run.....{pro_num}")
        self.page_shipment.btn_update_order.click()
        expect(self.page_shipment.page.get_by_text("order updated")).to_be_visible()
        expect(self.page_shipment.page.get_by_text("success")).to_be_visible()
        print("run.....")


    def test_dispatch_pick_up(self):

        self.page_dispatch.navigate()

        self.page_dispatch.select_dispatch.select_option("New Dispatch")
        self.page_dispatch.input_dispatch_start_date.fill((datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
        self.page_dispatch.page.keyboard.press('Enter')
        self.page_dispatch.select_driver_company.select_option("CoFreight")
        self.page_dispatch.noy_msg.wait_for(state="hidden")
        self.page_dispatch.input_direct_pickup_pro.fill("1001121970")
        self.page_dispatch.page.keyboard.press('Enter')
        self.page_dispatch.select_driver.select_option(index=5)
        self.page_dispatch.select_CTRL.select_option("BPK")
        self.page_dispatch.btn_dispatch.click()
        print("hello")





