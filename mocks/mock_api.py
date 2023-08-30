import json
"""
/**** 模拟编辑VIP体系返回修改成功结果***/
"""

mock_edit_grade_success = {
    "url": "**/vip/graderule/saveOrUpdate",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({"success": "true", "code": "null", "msg": "编辑成功", "result": "null"})
    )
}

mock_21_grades = {
    "url": "**/vip/graderule/getGradeRuleTable",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({
            "success": "true",
            "code": "null",
            "msg": "null",
            "result": {
                "draw": 0,
                "data": [
                    {
                        "viewId": "200000328",
                        "viewName": "【UI】自动化B体系",
                        "createTime": "2023-07-12 14:47:04",
                        "hierarchy": "6",
                        "isSingleShopView": "false",
                        "ruleName": "【UI】自动化VIPB",
                        "gradeStatus": 1,
                        "id": "82",
                        "isPaidMember": "false",
                        "allowSubGrade": 1
                    },
                    {
                        "viewId": "200000327",
                        "viewName": "【UI】自动化A体系",
                        "createTime": "2023-07-12 14:15:24",
                        "hierarchy": "6",
                        "isSingleShopView": "false",
                        "ruleName": "【UI】自动化VIPA",
                        "gradeStatus": 1,
                        "id": "80",
                        "isPaidMember": "false",
                        "allowSubGrade": 1
                    },
                    {
                        "viewId": "200000329",
                        "viewName": "南讯测试单店",
                        "createTime": "2023-07-12 11:47:01",
                        "hierarchy": "6",
                        "isSingleShopView": "true",
                        "ruleName": "淘宝VIP体系",
                        "gradeStatus": 0,
                        "id": "79",
                        "isPaidMember": "false",
                        "allowSubGrade": 0
                    },
                    {
                        "viewId": "200000294",
                        "viewName": "最伙小程序",
                        "createTime": "2023-01-03 14:45:07",
                        "hierarchy": "6",
                        "isSingleShopView": "false",
                        "ruleName": "最伙小程序",
                        "gradeStatus": 1,
                        "id": "8",
                        "isPaidMember": "false",
                        "allowSubGrade": 0
                    }
                ],
                "recordsTotal": "24",
                "recordsFiltered": "4",
                "ext": "null"
            }
        })
    )
}