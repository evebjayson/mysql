import pymysql

db = pymysql.connect(host="172.16.129.40", port=3306, user="root", password="root@123",charset='utf8')
cursor = db.cursor()


cursor.execute("show slave status")
result=cursor.fetchall()
db.commit()

print(result[0])