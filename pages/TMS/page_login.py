import allure
from playwright.sync_api import Page

"""TMS login page"""


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.input_username = page.locator("#input_username")
        self.input_password = page.locator("#input_password")
        self.btn_sign_in = page.get_by_role("button", name="Sign In")

    def navigate(self):
        self.page.goto("", wait_until="networkidle")

    def login(self, username, password):
        with allure.step(f"用户登录-{username}"):
            self.input_username.fill(username)
            self.input_password.fill(password)
            self.btn_sign_in.click()
