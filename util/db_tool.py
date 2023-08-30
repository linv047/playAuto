import pymysql


class DBTool:

    def __init__(self, db_info: dict):
        self.connect = pymysql.connect(**db_info)

    def execute_sql(self, sql) -> list:
        self.connect.connect()
        cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)   # 以map键值对的方式返回
        cursor.execute(sql)  # 执行SQL
        record = cursor.fetchone()  #  只返回第一条查询记录
        # recordall = cursor.fetchall() #  返回所有查询记录
        self.connect.commit()
        cursor.close()
        self.connect.close()
        return record