import json
import os
import jsonpath
import yaml




class UtilTool:


    @classmethod
    def get_cookie_from_file(cls) -> str:
        file_path = cls.get_path("/auth/state.json")
        with open(file_path, 'r') as f:
            data = json.loads(f.read())
        session_value = jsonpath.jsonpath(data, "$.cookies[?(@.name=='SESSION')].value")[0]
        token_value = jsonpath.jsonpath(data, "$.cookies[?(@.name=='token')].value")[0]
        return f"SESSION={session_value};token={token_value}"

# #   通过配置文件，获取配置信息，包括环境信息
#     @classmethod
#     def get_configure_from_file(cls, config_file_name="config"):
#         file_path = cls.get_path(f"/config/{config_file_name}.yaml")
#         with open(file_path, 'r', encoding="utf-8") as f:
#             data = yaml.safe_load(f)
#             return data



#   获取 环境对应下的测试数据
    @classmethod
    def get_data_from_file(cls, file_name: str):
        # path = GlobalMap().map.get("test_data_path")
        # if None == path:
        #     path = 'test'
        # file_path = cls.get_path(f"/test_data/{path}/{file_name}.yaml")
        file_path = cls.get_path(f"/test_data/{file_name}.yaml")
        with open(file_path, 'r', encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data

    @classmethod
    def get_path(cls, path) -> str:
        if path[0] != "/":
            path = f"/{path}"
        return f"{os.path.abspath(os.path.dirname(os.path.dirname(__file__)))}{path}"

    @classmethod
    def read_yaml(cls, filename):
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(project_dir, "test_data")
        filename1 = f"{filename}.yaml"
        cls.file = os.path.join(data_path, filename1)
        with open(cls.file, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data

    @classmethod
    def get_data_by_yaml(cls, filename , term ,name):
        data = cls.read_yaml(filename)
        city_data = data.get(term, None)
        datas = city_data.get(name)
        return datas

    # @classmethod
    # def execute_sql(cls, sql, dbinfo):
    #     connect = pymysql.connect(**dbinfo)
    #     cursor = connect.cursor()
    #     cursor.execute(sql)  # 执行SQL
    #     record = cursor.fetchone()  # 查询记录
    #     connect.commit()
    #     cursor.close()
    #     connect.close()
    #     return record

