import pymysql
import DatabaseConfig

config=DatabaseConfig.config

#这个函数用来检查用户的登录信息，传入的变量为用户名和密码
#该函数有五个返回值，分别为-2，-1,1,2,3
#-2表示用户名不存在
#-1表示用户名存在但密码错误
#1表示这是一个管理员账户，且密码正确
#2表示这是一个教师账户，且密码正确
#3表示这是一个学生账户，且密码正确
def check(username,password):
    if username=='admin':
        conn = pymysql.connect(**config)
        with conn.cursor() as cursor:
            sql='select password from admin_info'
            cursor.execute(sql)

            result=cursor.fetchone()
            conn.commit()
            conn.close()
            if(result['password']==password):
                return 1
            else:
                return -1
    elif len(username)==5:
        conn=pymysql.connect(**config)
        with conn.cursor() as cursor:
            sql='select password from teacher where tno=%s'
            cursor.execute(sql,username)

            result=cursor.fetchone()
            conn.commit()
            conn.close()

            if result==None:
                return -2
            elif result['password']==password:
                return 2
            else:
                return -1
    elif len(username)==9:
        conn = pymysql.connect(**config)
        with conn.cursor() as cursor:
            sql = 'select password from student where sno=%s'
            cursor.execute(sql, username)

            result = cursor.fetchone()
            conn.commit()
            conn.close()

            if result == None:
                return -2
            elif result['password'] == password:
                return 3
            else:
                return -1
    else:
        return -2

#根据学号获得学生的名字
def GetStudentName(sno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT sname FROM student WHERE sno=%s'
        cursor.execute(sql,sno)

        result=cursor.fetchone()
        conn.commit()
        conn.close()
        return result['sname']

if __name__=='__main__':
    sno='100000000'
    print(GetStudentName(sno))