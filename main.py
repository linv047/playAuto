import pytest

"""参数化： 单参数"""
search_list = ['appium','selenium','pytest']

@pytest.mark.parametrize('name',search_list)
def test_search(name):
    print(name)





"""参数化： 多参数"""
test_data = [
    ["admin","test1"],
    ["user","test2"],
    ["userb",""]
]
@pytest.mark.parametrize("username,password", test_data)
def test_login(username,password):
    print(username,password)


