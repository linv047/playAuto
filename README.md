# playAuto



## 介绍

该项目是以playwright框架为基础，pytest驱动管理组织测试用例，allure来显示输出测试报告，设计模式还是传统的PO设计模式的WEB UI自动化测试框架。

### 项目

- [ ] apiHelper: 物料接口，用于物料的准备和销毁，一般用于case前后的setup和teardown
- [ ] auth: 存放鉴权信息，如cookie，token等
- [ ] config: config.py 记录测试环境信息，如测试地址、账号密码等
- [ ] mocks: mock_api.py 记录用例中需要的mock的信息
- [ ] **pages**: 页面模块，其中page_base存放页面的公共组件和公共方法
- [ ] test_data: 测试数据文件，建议使用yaml或json文件
- [ ] **testcases**: 存放测试用例
- [ ] util: 公共工具方法，如读取文件、操作数据库和公共变量存取的GlobalMap
- [ ] venv python环境相关，其中python版本为3.8.10。依赖相关详见requirements.txt
