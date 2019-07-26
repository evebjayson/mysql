import pymysql
import datetime
from logger import Log



class SynchronizeData():
    def __init__(self):
        # self.time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%SZ')
        # self.ssh = paramiko.SSHClient()
        self.log = Log()
        self.db = pymysql.connect(host="172.16.129.40", port=3306, user="root", password="root@123",charset='utf8')
        self.cursor = self.db.cursor()
    # def connection_service(self):
    #     '''连接linux服务器'''
    #     self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 允许连接不在know_hosts文件中的主机
    #     self.ssh.connect(hostname='172.16.129.40', port=8800, username='root', password='root@123') # 连接服务器
    #     sftp_client = self.ssh.open_sftp()
    #     mysqld_log = sftp_client.open("/var/log/mysqld.log")  # 文件路径
    #     l = mysqld_log.readlines()  # 获取所有日志内容
    #     row_list = [x.strip() for x in l if x.strip() != '']
    #     error_list = []
    #     for log_list in row_list:
    #         if '1733' in log_list:
    #             error_list.append(log_list)
    #     return error_list

    def synchronize(self):
        self.cursor.execute("show slave status")
        result = self.cursor.fetchall() # 获取字段信息
        self.db.commit()
        try:
            if 'no' in result[0]:
                print("数据链接断开,准备重新启动同步程序")
                self.log.info("数据同步有问题,准备重新启动同步程序")
                self.cursor.execute("start slave")
                self.db.commit()
            else:
                print("同步数据正常,状态正常")
                self.log.info("同步数据正常,无错误日志")
            self.ssh.close()  # 关闭
        except Exception as e:
            print(e)
            self.db.rollback() # 出现异常，回滚

if __name__ == "__main__":
    SynchronizeData().synchronize()