# coding=utf-8
import os
from jenkins import Jenkins
import requests
class JenkinsContest:

    def __init__(self):
        # jenkins的IP地址
        self.jenkins_url = "http://192.168.200.242:8080/"
        # jenkins用户名和密码
        self.server = Jenkins(self.jenkins_url, username='admin', password='a123456')
    def jenkins_content_info(self):
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        www = r"{}".format(project_dir)
        name = (www.split(":")[1].split("\\")[3])
        result_job = self.server.get_jobs()
        job_name = name
        job_url = self.server.get_job_info(job_name)['url']
        job_last_number = self.server.get_job_info(job_name)['lastBuild']['number']
        report_url = job_url + str(job_last_number) + '/allure'
        return result_job, job_name, job_url, job_last_number, report_url

class Send_DingTalk(JenkinsContest):

    def __init__(self):
        super().__init__()
        self.result_job,  self.job_name, self.job_url, self.job_last_number, self.report_url = self.jenkins_content_info()


    def push_message(self):
        content = {}
        file_path = os.path.dirname(os.getcwd()) + '/allure-report/export/prometheusData.txt'
        f = open(file_path)
        for line in f.readlines():
            launch_name = line.strip('\n').split(' ')[0]
            num = line.strip('\n').split(' ')[1]
            content.update({launch_name: num})
        f.close()
        passed_num = content['launch_status_passed']  # 通过数量
        failed_num = content['launch_status_failed']  # 失败数量
        broken_num = content['launch_status_broken']  # 阻塞数量
        skipped_num = content['launch_status_skipped']  # 跳过数量
        case_num = content['launch_retries_run']  # 总数量
        all_time = content['launch_time_duration']  # 持续时间
        minute_time = (float(all_time)/60000)
        minute_time1 = float(format(minute_time,'.1f'))
        if case_num == passed_num:
            status = '通过'
        else:
            status = '不稳定'
        """
        钉钉消息发送，通过webhook发送消息
        """
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=0bdac2b823a4f50746b26fc0c9925c58f1357e9b218bd101204bc03934b8b415"
        # 这里一定要注意！！！content:内容要包含钉钉的关键字，不然会一直报错不通过！！！
        # 这里一定要注意！！！content:内容要包含钉钉的关键字，不然会一直报错不通过！！！
        # 这里一定要注意！！！content:内容要包含钉钉的关键字，不然会一直报错不通过！！！!
				#测试阶段为钉钉关键字
        content = {
            "msgtype": "text",
            "text": {
                "content": "测试阶段UI自动化脚本执行结果：\n用例总数：" + case_num
                           + "\n通过用例：" + passed_num
                           + "\n失败用例：" + failed_num
                           + "\n阻塞用例：" + broken_num
                           + "\n跳过用例：" + skipped_num
                           + "\n执行状态：" + status
                           + "\n持续时间：%f" % (minute_time1) + "分钟"
                           + "\n构建地址：" + self.job_url
                           + "\n报告地址：" + self.report_url
            }
        }

        response = requests.post(url=webhook, json=content, verify=False)

        if response.json()['errmsg'] != "ok":
            return response.text

        return response

if __name__ == '__main__':
    Send_DingTalk().push_message()
