import os
import allure
from faker import Faker
from playwright.sync_api import Page, Locator
from util.do_log import Logger


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.log = Logger().get_log()

    # 通过文本内容获取按钮
    def all_button(self, text, nth=-1) -> Locator:
        button = self.page.locator("button").filter(has_text=text)
        return button.locator('visible=true').nth(nth)

    def all_notification(self, msg, nth=-1) -> Locator:

        notification = self.page.locator(".ant-notification-notice-message")
        return notification.filter(has_text=msg).locator('visible=true').nth(nth)

    # 输入框
    def input_content(self, name, value):
        name1 = name + '：'
        self.page.get_by_label(name1).click()
        self.page.get_by_label(name1).clear()
        self.page.get_by_label(name1).fill(value)

    # 下拉选择框
    def select_content(self, name, value):
        if isinstance(name, str):
            # name1 = name + ': '
            self.page.get_by_label(name).click()
            self.page.get_by_text(value, exact=True).click()
        elif isinstance(name, Locator):
            name.click()
            self.page.locator("label").filter(has_text=value).nth(-1).click()
        else:
            raise Exception("未支持类型")

    # 下拉搜索框
    def search_content(self, name, value):
        name1 = name + '：'
        self.page.get_by_label(name1).click()
        self. page.get_by_role("textbox", name="搜索...").fill(value)
        self. page.locator("span").filter(has_text=value).nth(1).click()

    # 时间输入框 name1:开始时间底纹，name2:结束时间底纹，不同的时间输入框底纹不通
    def search_time(self, name1, name2, starttime, endtime):
        self.page.get_by_placeholder(name1).click()
        self.page.get_by_placeholder(name1).fill(starttime)
        self.page.get_by_placeholder(name2).click()
        self.page.get_by_placeholder(name2).fill(endtime)
        self.page.get_by_placeholder(name2).press("Enter")

    # 点击tab页面
    def switch_tab(self, value):
        self.page.get_by_role("tab", name=value).click()

    def screenshot_to_allure_report(self, file_name=""):
        if file_name == "":
            file_name = f"screenshot-{str(Faker().random_number(digits=10))}.png"
        file_name = file_name if file_name.endswith("png") else f"{file_name}.png"
        file_path = f"{os.path.abspath(os.path.dirname(os.path.dirname(__file__)))}/log/{file_name}"
        self.page.screenshot(path=file_path)
        allure.attach.file(file_path, name=file_name, attachment_type=allure.attachment_type.PNG)
