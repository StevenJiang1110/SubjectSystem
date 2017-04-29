import pymysql

config={
    'host':'localhost',
    'port':3306,
    'user':'zx_root',
    'password':'123456',
    'db':'test',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor,
}