# -*- coding: utf-8 -*-\n',
# # Author:jiang\n',
# 2020/12/21 17:44\n',
import MySQLdb
tool_ico_name="log.ico"
MySqlConfig_go2 = {
"host": "192.168.10.13",
"port": 40003,
"user": "root",
"password": "leweisa",
"db": "db_go2",
"charset": "utf8",# 数据库连接编码'
}
MySqlConfig_stats = {
"host": "192.168.10.13",
"port": 40003,
"user": "root",
"password": "leweisa",
"db": "db_stats",
"charset": "utf8",# 数据库连接编码'
}
MySqlConfig_drop_shipping = {
"host": "47.96.162.123",
"port": 3306,
"user": "cqdev",
"password": "cqdev",
"db": "drop_shipping",
"charset": "utf8",# 数据库连接编码'
}

def MySql_stats(sql):
    conn = MySQLdb.Connect(**MySqlConfig_stats)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
def MySql_go2(sql):
    conn = MySQLdb.Connect(**MySqlConfig_go2)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
def MySql_drop_shipping(sql):
    conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
