import re
import time
import jsonpath

import allure
import pytest
from playwright.sync_api import expect
from apiHelper.api_grade_rule import GradeRuleApi
from mocks import mock_api
from pages.vipSystem.page_grade_rule import GradeRulePage
from util.db_tool import DBTool
from util.util import UtilTool


class TestVIPSystem:
    """VIP体系"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, page, global_map, environ):
        with allure.step("--导航到VIP体系列表页面--"):
            self.page_vip_list = GradeRulePage(page)
            self.page_vip_list.navigate()
            self.page_vip_list.page.wait_for_load_state("networkidle")
        self.db_tool = DBTool(environ.database_info)
        self.global_map = global_map
        # self.search_data_single = UtilTool.get_data_from_file("gradeRule")["VIP体系名称"][0]
        self.search_data_single = "自动化VIPA"
        self.new_name = f"UI自动化{str(time.time_ns())[9:15:]}"
        self.api_client = GradeRuleApi()
        yield
        sql_set_grade_delete = f"delete from kd_grade_rule where rule_name like 'UI自动化%' and view_id in (select view_id from yun_view where view_name like '【UI】自动化C%')"
        self.db_tool.execute_sql(sql_set_grade_delete)

    @pytest.fixture()
    def create_grade(self):
        self.api_client.create(self.new_name)
        self.page_vip_list.page.reload()
        yield

    @pytest.fixture()
    def create_grown_mode_grade(self):
        self.api_client.create(self.new_name, 2)
        self.page_vip_list.page.reload()
        yield

    @pytest.fixture()
    def create_grade_grow(self):
        self.api_client.create(self.new_name, rule_type=2)
        yield


    @pytest.fixture()
    def after_delete(self):
        yield
        sql1 = f"delete from kd_grade_rule_detail where view_id=(select view_id from kd_grade_rule where rule_name = '{self.new_name}')"
        self.db_tool.execute_sql(sql1)
        sql2 = f"delete from kd_grade_rule where rule_name = '{self.new_name}'"
        self.db_tool.execute_sql(sql2)


    @pytest.mark.parametrize('search_data',  UtilTool.get_data_from_file("gradeRule")["搜索VIP体系名称"])
    def test_search(self, search_data):
        """验证列表简单搜索功能：VIP体系名称"""
        with allure.step(f"搜索-{search_data}"):
            self.page_vip_list.search_input.fill(search_data)
            self.page_vip_list.search_btn.click()
        with allure.step(f"校验有出现{search_data}"):
            self.page_vip_list.screenshot_to_allure_report()
            expect(self.page_vip_list.no_data).not_to_be_visible()
            assert self.page_vip_list.get_list_total_num > 0

    def test_detail(self):
        """验证列表进入详情页面功能"""
        with allure.step(f"点击进入-{self.search_data_single}详情"):
            self.page_vip_list.search_input.fill(self.search_data_single)
            self.page_vip_list.search_btn.click()
            expect(self.page_vip_list.no_data).not_to_be_visible()
            # 截获返回response
            with self.page_vip_list.page.expect_response("**/graderule/getGradeRule?id=**") as response:
                self.page_vip_list.click_detail_btn_by_name(self.search_data_single)
                assert response.value.ok
                response.value.json()

        with allure.step("点击【下一步】【返回】"):
            self.page_vip_list.btn_next_step.click()
            expect(self.page_vip_list.btn_previous_step).to_be_visible()
            expect(self.page_vip_list.btn_save).to_be_disabled()
            self.page_vip_list.screenshot_to_allure_report("下一步.png")
            self.page_vip_list.btn_back.click()
            expect(self.page_vip_list.btn_save).not_to_be_visible()
            expect(self.page_vip_list.add_btn).to_be_visible()
            self.page_vip_list.screenshot_to_allure_report("返回.png")


    def test_edit(self):
        """验证编辑功能"""
        with allure.step(f"搜索进入{self.search_data_single}页面"):
            self.page_vip_list.search_input.fill(self.search_data_single)
            self.page_vip_list.search_btn.click()
            self.page_vip_list.click_edit_btn_by_name(self.search_data_single)
        with allure.step("编辑"):
            self.page_vip_list.input_name.fill(f"{self.search_data_single}{str(time.time_ns())[9:14:]}")
            self.page_vip_list.btn_next_step.click()
            self.page_vip_list.page.route(**mock_api.mock_edit_grade_success)
            self.page_vip_list.btn_save.click()
        with allure.step("校验编辑成功"):
            expect(self.page_vip_list.tip_edit_successful).to_be_visible()


    def test_start_stop_status(self, create_grade, after_delete):
        """验证VIP体系开启/关闭功能"""
        with allure.step(f"搜索进入{self.search_data_single}页面"):
            self.page_vip_list.search_input.fill(self.search_data_single)
            self.page_vip_list.search_btn.click()
        with allure.step(f"判断当前体系状态为开启"):
            self.page_vip_list.page.wait_for_timeout(2000)
            assert self.page_vip_list.switch_status.is_checked()
            self.page_vip_list.screenshot_to_allure_report("初始状态")
        with allure.step("关闭"):
            self.page_vip_list.switch_status.click()
            self.page_vip_list.btn_confirm.click()
            expect(self.page_vip_list.tip_stop).to_be_visible()
            self.page_vip_list.tip_stop.wait_for(state="hidden")
        with allure.step("开启"):
            self.page_vip_list.switch_status.click()
            self.page_vip_list.btn_confirm.click()
            expect(self.page_vip_list.tip_start).to_be_visible()


    def test_single_store(self):
        """验证列表-单店体系可操作权限"""
        with allure.step("校验单店无编辑权限"):
            assert self.page_vip_list.get_edit_btn_by_name("单店").count() == 0

    def test_omnichannel(self):
        """验证列表-全渠道VIP体系可操作权限"""
        with allure.step("校验全渠道VIP体系有编辑权限"):
            self.page_vip_list.click_edit_btn_by_name(self.search_data_single)
            expect(self.page_vip_list.page).to_have_url(re.compile(r'.*/Edit'))
        with allure.step("校验有保存权限"):
            self.page_vip_list.btn_next_step.click()
            assert self.page_vip_list.btn_save.is_enabled()

    def test_add_mix_mode(self, after_delete):
        """验证新增混合VIP规则功能"""
        self.page_vip_list.add_btn.click()
        with allure.step("基础设置"):
            self.page_vip_list.input_name.fill(self.new_name)
            self.page_vip_list.check_view.click()
            self.page_vip_list.get_option_by_name("自动化C2体系").click()
            self.page_vip_list.chk_mix_mode.check()
            self.page_vip_list.input_start_date.type("2023/06/29 00:00:00")
            self.page_vip_list.btn_confirm.click()
            self.page_vip_list.get_collapse_by_name("基础设置").click()
        with allure.step("升降级设置:开启"):
            self.page_vip_list.chk_allow_sub_grade.check()
            self.page_vip_list.get_collapse_by_name("升降级设置").click()
        with allure.step("排除规则：不设置"):
            # 不设置排除规则
            self.page_vip_list.get_collapse_by_name("排除规则").click()
        with allure.step("规则设置：开启设置VIP1"):
            self.page_vip_list.chk_1vip_status.check()
            self.page_vip_list.input_1vip_rule_value.fill("10")
            self.page_vip_list.input_1vip_holdrule_value.fill("1")
            self.page_vip_list.get_collapse_by_name("规则设置").click()
        with allure.step("默认等级设置：VIP1"):
            self.page_vip_list.chk_default_grade.click()
            self.page_vip_list.get_option_by_name("VIP1").click()
            self.page_vip_list.btn_next_step.click()
            self.page_vip_list.btn_save.click()
        with allure.step("校验创建成功"):
            expect(self.page_vip_list.tip_add_successful2).to_be_visible()
            expect(self.page_vip_list.get_grade_by_name(self.new_name)).to_be_visible()


    def test_add_grow_mode(self, after_delete):
        """验证新增成长值模式VIP规则功能"""
        self.page_vip_list.add_btn.click()
        with allure.step("基础设置"):
            self.page_vip_list.input_name.fill(self.new_name)
            self.page_vip_list.check_view.click()
            self.page_vip_list.get_option_by_name("自动化C3").click()
            self.page_vip_list.chk_grow_mode.check()
            self.page_vip_list.check_integral_account.click()
            self.page_vip_list.get_option_by_name("自动化C3成长值").click()
        with allure.step("升降级设置"):
            self.page_vip_list.get_collapse_by_name("升降级设置").click()
        with allure.step("规则设置"):
            self.page_vip_list.chk_1vip_status.check()
            self.page_vip_list.input_1vip_rule_value.fill("1")
        self.page_vip_list.btn_next_step.click()
        with allure.step("VIP权益设置"):
            self.page_vip_list.chk_vip1_detail_status.check()
            self.page_vip_list.vip1_detail_discount.fill("9")
        self.page_vip_list.btn_save.click()
        with allure.step("校验新建成功"):
            expect(self.page_vip_list.tip_add_successful2).to_be_visible()
            expect(self.page_vip_list.get_grade_by_name(self.new_name)).to_be_visible()


    def test_update_mix_mode(self, create_grade, after_delete):
        """验证编辑混合行为规则"""
        with allure.step(f"搜索进入{self.new_name}编辑页面"):
            self.page_vip_list.search_input.fill(self.new_name)
            self.page_vip_list.search_btn.click()
            self.page_vip_list.click_edit_btn_by_name(self.new_name)
            self.page_vip_list.input_grade_days.fill("200")
            self.page_vip_list.get_collapse_by_name("基础设置").click()
        with allure.step("编辑：开启升降级设置"): ### $.result.gradeRule.allow_sub_grade == 1
            self.page_vip_list.chk_allow_sub_grade.check()
            self.page_vip_list.get_collapse_by_name("升降级设置").click()
            self.page_vip_list.get_collapse_by_name("排除规则").click()
        with allure.step("编辑：开启VIP2"):
            self.page_vip_list.input_1vip_rule_value.fill("10")
            self.page_vip_list.input_1vip_holdrule_value.fill("1")
            self.page_vip_list.chk_2vip_status.check()
            self.page_vip_list.input_2vip_rule_value.fill("100")
            self.page_vip_list.input_2vip_holdrule_value.fill("10")
            self.page_vip_list.get_collapse_by_name("规则设置").click()
        with allure.step("编辑：默认等级设置为VIP2"): # $.result.gradeRule.register_default_grade ==2
            self.page_vip_list.chk_default_grade.click()
            self.page_vip_list.get_option_by_name("VIP2").click()
            self.page_vip_list.btn_next_step.click()
        with allure.step("编辑：设置VIP2折扣 8折"): # $.result.gradeRuleDetailList[1].grade_benefit_json
            self.page_vip_list.chk_vip2_detail_status.check()
            self.page_vip_list.vip2_detail_discount.fill("8")
            self.page_vip_list.btn_save.click()
        with allure.step("校验编辑成功"):
            expect(self.page_vip_list.tip_edit_successful).to_be_visible()
        with allure.step("校验编辑成功保存数据"):
            # 截获返回response
            with self.page_vip_list.page.expect_response("**/graderule/getGradeRule?id=**") as response:
                self.page_vip_list.click_detail_btn_by_name(self.new_name)
                response_json = response.value.json()
                value0 = jsonpath.jsonpath(response_json, "$.result.gradeRule.days_between")
                value1 = jsonpath.jsonpath(response_json, "$.result.gradeRule.allow_sub_grade")
                value2 = jsonpath.jsonpath(response_json, "$.result.gradeRule.register_default_grade")
                grade_benefit_json = eval(str(jsonpath.jsonpath(response_json, "$.result.gradeRuleDetailList[1].grade_benefit_json")[0]).replace("true", "True").replace("false", "False"))
                value3 = jsonpath.jsonpath(grade_benefit_json, "$.discount")
                value4 = jsonpath.jsonpath(grade_benefit_json, "$.discountEnable")
                assert value0[0] == 200, "校验基础设置-数据范围-累计天数"
                assert value1[0] == 1, "校验升降级开启"
                assert value2[0] == 2, "校验默认等级为2"
                assert value3[0] == "8" and value4[0], "校验权益开启VIP2，8折"

    def test_update_grown_mode(self, create_grown_mode_grade, after_delete):
        """验证编辑成长值模式规则"""
        with allure.step(f"搜索进入{self.new_name}编辑页面"):
            self.page_vip_list.search_input.fill(self.new_name)
            self.page_vip_list.search_btn.click()
            self.page_vip_list.click_edit_btn_by_name(self.new_name)
        with allure.step("编辑升降级设置:开启"): #$.result.gradeRule.allow_sub_grade ==1
            self.page_vip_list.radio_allow_sub_grade.check()
        with allure.step("编辑规则设置:开启VIP2"): #$.result.gradeRuleDetailList[1].is_enable ==1
            self.page_vip_list.input_1vip_rule_value.fill("2")
            self.page_vip_list.input_1vip_holdrule_value.fill("1")
            self.page_vip_list.chk_2vip_status.check()
            self.page_vip_list.input_2vip_rule_value.fill("4")
            self.page_vip_list.input_2vip_holdrule_value.fill("3")
        self.page_vip_list.btn_next_step.click()
        with allure.step("编辑规则设置:开启VIP2,8折"): # $.result.gradeRuleDetailList[1].grade_benefit_json
            self.page_vip_list.chk_vip2_detail_status.check()
            self.page_vip_list.vip2_detail_discount.fill("8")
        self.page_vip_list.btn_save.click()
        with allure.step("校验编辑成功"):
            expect(self.page_vip_list.tip_edit_successful).to_be_visible()
        with allure.step("校验编辑成功保存数据"):
            # 截获返回response
            with self.page_vip_list.page.expect_response("**/graderule/getGradeRule?id=**") as response:
                self.page_vip_list.click_detail_btn_by_name(self.new_name)
                response_json = response.value.json()
                value1 = jsonpath.jsonpath(response_json, "$.result.gradeRule.allow_sub_grade")
                value2 = jsonpath.jsonpath(response_json, "$.result.gradeRuleDetailList[1].is_enable")
                grade_benefit_json = eval(str(
                    jsonpath.jsonpath(response_json, "$.result.gradeRuleDetailList[1].grade_benefit_json")[0]).replace(
                    "true", "True").replace("false", "False"))
                value3 = jsonpath.jsonpath(grade_benefit_json, "$.discount")
                value4 = jsonpath.jsonpath(grade_benefit_json, "$.discountEnable")
                assert value1[0] == 1, "校验升降级设置:开启"
                assert value2[0] == 1, "校验规则设置:开启VIP2"
                assert value3[0] == "8" and value4[0], "校验权益开启VIP2，8折"
