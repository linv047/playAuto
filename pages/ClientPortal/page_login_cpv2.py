import allure
from playwright.sync_api import Page

"""client portal login page"""


class CPV2LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.input_username = page.locator("input[name='userName']")
        self.input_password = page.locator("input[name='passWord']")
        self.btn_log_in = page.get_by_role("button", name="Log in")

        self.input_order = page.get_by_placeholder("Enter shipment reference")
        self.btn_track = page.locator("//button[text()='Track']")

    def navigate(self):
        self.page.goto("/#/login", wait_until="load")

    def login(self, username, password):
        with allure.step(f"用户登录-{username}"):
            self.input_username.fill(username)
            self.input_password.fill(password)
            self.btn_log_in.click()

    def track_order(self, order_id):
        self.input_order.fill(order_id)
        self.btn_track.click()
