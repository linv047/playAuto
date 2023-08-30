import pytest
from typing import Dict
from pages.ClientPortal.page_login_cpv2 import CPV2LoginPage
from pages.TMS.page_login import LoginPage


@pytest.fixture(scope="session", autouse=True)
def login_save_auth(browser, pytestconfig, environ) -> None:
    """登录，保存cookies"""
    context = browser.new_context(base_url=environ.base_url, no_viewport=True)
    context.grant_permissions(['geolocation'])
    page = context.new_page()
    #"""TMS login"""
    if environ.test_system == "TMS":
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(environ.username, environ.password)
        # 等待登录成功页面重定向
        page.wait_for_url("**dashboard", wait_until="networkidle")
    else:
        # """client portal login"""
        login_page = CPV2LoginPage(page)
        login_page.navigate()
        login_page.login(environ.username, environ.password)
        page.wait_for_url("**home", wait_until="networkidle")

    # 保存storage state 到指定的文件
    storage_path = pytestconfig.rootpath.joinpath("auth/state.json")
    context.storage_state(path=storage_path)
    context.close()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright, pytestconfig, global_map) -> Dict:  # noqa
    """
    添加context 上下文参数，默认每个页面加载cookies
    """
    return {
        "storage_state": pytestconfig.rootpath.joinpath("auth/state.json"),
        "no_viewport": True,
        "permissions": ['geolocation'],
        "base_url": global_map.get("base_url"),
        **browser_context_args,
    }


@pytest.fixture(scope="module")
def other_context(browser, environ, pytestconfig, other_login_save_auth):
    context = browser.new_context(
        base_url=environ.base_url,
        no_viewport=True,
        storage_state=pytestconfig.rootpath.joinpath("auth/state.json")
    )
    yield context
    context.close()


@pytest.fixture(scope="module")
def login_context(browser, pytestconfig, global_map):
    """
    登录页面单独创建独立的page对象
    避免全局先登录加载cookie，导致有些打开登录页直接跳到首页去了
    :return:
    """
    context = browser.new_context(base_url=global_map.get("base_url"), no_viewport=True)
    yield context
    context.close()
