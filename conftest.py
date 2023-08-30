from pytest import Item
import os
from typing import Any, Dict, Generator, List, Union

import allure
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Error,
    Page,
)
from pytest_playwright.pytest_playwright import _build_artifact_test_folder
from slugify import slugify

from config.config import *
from util.global_map import GlobalMap


@pytest.fixture(scope="session")
def environ(request) -> Union[TestConfig, UATConfig, UATConfig]:
    """Return a env"""
    config = request.config
    env_name = config.getoption("--env") or config.getini("env")
    if env_name is not None:
        return env.get(env_name)

def pytest_addoption(parser):  # noqa
    """添加 env 配置"""
    parser.addini('env', default=None, help='run environment by test or uat ...')
    parser.addoption(
        "--env", action="store", default=None, help="run environment by test or uat ..."
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args) -> Dict:
    """窗口最大化"""
    return {
        "args": ['--start-maximized'],
        **browser_type_launch_args,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright, pytestconfig) -> Dict:
    """窗口最大化"""
    return {
        "no_viewport": True,
        "viewport": {'width': 1920, 'height': 1080},
        "record_video_size": {"width": 1920, "height": 1080},
        **browser_context_args,
    }

def pytest_runtest_call(item: Item):  # noqa
    # 动态添加测试类的 allure.feature()
    if item.parent._obj.__doc__:  # noqa
        allure.dynamic.feature(item.parent._obj.__doc__) # noqa
    # 动态添加测试用例的title 标题 allure.title()
    if item.function.__doc__: # noqa
        allure.dynamic.title(item.function.__doc__) # noqa


@pytest.fixture(scope="session", autouse=True)
def global_map(environ):
    global_map = GlobalMap()
    for key in dir(environ):
        if not key.startswith("__"):
            value = getattr(environ, key)
            if isinstance(value, tuple):
                value = value[0]
            global_map.set(key, value)
    yield global_map


@pytest.fixture
def context(
    browser: Browser,
    browser_context_args: Dict,
    pytestconfig: Any,
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    pages: List[Page] = []
    context = browser.new_context(**browser_context_args)
    context.on("page", lambda page: pages.append(page))

    tracing_option = pytestconfig.getoption("--tracing")
    capture_trace = tracing_option in ["on", "retain-on-failure"]
    if capture_trace:
        context.tracing.start(
            title=slugify(request.node.nodeid),
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    yield context

    # If requst.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True

    if capture_trace:
        retain_trace = tracing_option == "on" or (
            failed and tracing_option == "retain-on-failure"
        )
        if retain_trace:
            trace_path = _build_artifact_test_folder(pytestconfig, request, "trace.zip")
            context.tracing.stop(path=trace_path)
        else:
            context.tracing.stop()

    screenshot_option = pytestconfig.getoption("--screenshot")
    capture_screenshot = screenshot_option == "on" or (
        failed and screenshot_option == "only-on-failure"
    )
    if capture_screenshot:
        for index, page in enumerate(pages):
            human_readable_status = "failed" if failed else "finished"
            screenshot_path = _build_artifact_test_folder(
                pytestconfig, request, f"test-{human_readable_status}-{index+1}.png"
            )
            try:
                page.screenshot(timeout=5000, path=screenshot_path)
                # --------- 把截图放入allure报告 以下代码新增 --------------
                allure.attach.file(screenshot_path,
                                   name=f"{request.node.name}-{human_readable_status}-{index + 1}",
                                   attachment_type=allure.attachment_type.PNG
                                   )
                # --------- 把截图放入allure报告 --------------
            except Error:
                pass

    context.close()

    video_option = pytestconfig.getoption("--video")
    preserve_video = video_option == "on" or (
        failed and video_option == "retain-on-failure"
    )
    if preserve_video:
        for page in pages:
            video = page.video
            if not video:
                continue
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                file_path = _build_artifact_test_folder(pytestconfig, request, file_name)
                video.save_as(
                    path=file_path
                )
                # 放入视频
                allure.attach.file(file_path, name=f"{request.node.name}-{human_readable_status}-{index + 1}",
                attachment_type = allure.attachment_type.WEBM)
            except Error:
                # Silent catch empty videos.
                pass