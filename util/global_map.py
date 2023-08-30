class GlobalMap:  # 跨文件全局变量

    map = {}

    def set(self, key, value):
        self.map[key] = value

    def get(self, key):
        return self.map[key]

    def delete(self, key):
        self.map.pop(key)

    def update(self,datas: dict):
        self.map.update(datas)