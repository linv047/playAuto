class Config:
    """多套环境的公共配置"""
    version = "v1.0"


class TestConfig(Config):
    """TMS staging环境"""
    test_system = "TMS"
    base_url = 'https://staging.freightapp.com'
    username = 'victor.lin@unisco.com'
    password = 'pz5Nw100'
    database_info = {
        "host": "staging.freightapp.com",
        "port": 3306,
        "user": "tms_staging_master_user",
        "password": "M@B2w!uo",
        "database": "tms_staging_master"
    }
    # test_data_path = "uat"  # 连接数据的库名


class UATConfig(Config):
    """client portal 测试环境"""
    test_system = "client portal"
    base_url = 'https://shipstage.unisco.com/v2'
    username = 'seven.xiao898@teml.net'
    password = 'Seven123'
    database_info = {
        "host": "39.98.86.68",
        "port": 443,
        "user": "app_e_grayrel",
        "password": "Jkx29Kx7xk24sc",
        "database": "ecrp_autotest"
    }
    # test_data_path = "uat_data"


# 环境关系映射，方便切换多环境配置
env = {
    "uat": UATConfig,
    "test": TestConfig
}
