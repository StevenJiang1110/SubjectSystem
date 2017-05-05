import pymysql
import DatabaseConfig

#连接数据库的配置信息
config=DatabaseConfig.config

#一个学生的最大学分数
MAX_POINT=20

#根据学号获得该学生修读的所有课程作为列表返回,信息包括课程号，课程名，课程时间和任课老师名，如果没有结果返回（）
def GetCourse(sno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT selectcourse.cno,cname,begintime,endtime,tname,point FROM course,selectcourse,teacher WHERE selectcourse.sno=%s and selectcourse.cno=course.cno AND course.tno=teacher.tno'
        cursor.execute(sql,sno)
        result=cursor.fetchall()
        conn.commit()
        conn.close()
        return result

#根据提供的课程号、课程名、教师名获得可选课程的列表
def GetSelectiveCourse(cno,cname,tname):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT course.cno,cname,tname,begintime,endtime,limits FROM course,teacher WHERE course.cno LIKE %s and cname LIKE %s and tname LIKE %s and course.tno=teacher.tno  GROUP BY course.cno'
        tmpcno=cno+'%'
        tmpcname=cname+'%'
        tmptname=tname+'%'
        cursor.execute(sql,(tmpcno,tmpcname,tmptname))
        result=cursor.fetchall()
        conn.commit()
        conn.close()
        return result

#根据给定的课程号获得选则当前课程的人数
def GetCourseSelectedNumber(cno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT COUNT(*) FROM selectcourse WHERE cno=%s'
        cursor.execute(sql,cno)
        result=cursor.fetchone()
        return result['COUNT(*)']

#根据提供的课程号，学号进行检查是否是可选课程，同时检查人数上限，时间冲突，学分上限
#该函数共有五个返回值，-4，-3，-2，-1,0
#当这门课是已选课程时返回-4
#当这门课选课人数已达上限时返回-3
#当学生的学分已经超限时返回-2
#当该课程与该学生的已选课程时间发生冲突时返回-1
#当该课程是可选课程时返回0
def CheckCourse(cno,sno,courseTime):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        #首先检查是不是已选课程
        sql='SELECT * FROM selectcourse WHERE sno=%s and cno=%s'
        cursor.execute(sql,(sno,cno))
        result=cursor.fetchall()
        if result!=():
            conn.commit()
            conn.close()
            return -4
        else:
            #检查课程人数是否已经超过上限
            sql='SELECT COUNT(sno),limits FROM selectcourse,course WHERE course.cno=selectcourse.cno AND course.cno=%s GROUP BY course.cno'
            cursor.execute(sql,cno)
            result=cursor.fetchone()
            if result==None:
                currentNumber=-1
                limits=1
            else:
                currentNumber=result['COUNT(sno)']
                limits=result['limits']
            if currentNumber>=limits:
                conn.commit()
                conn.close()
                return -3
            else:
                #检查学分是否已经超上限
                sql='SELECT SUM(course.point) FROM selectcourse,course WHERE selectcourse.sno=%s AND selectcourse.cno=course.cno'
                cursor.execute(sql,sno)
                result=cursor.fetchone()
                numResult=result['SUM(course.point)']
                currentPoint=0
                if numResult!=None:
                    currentPoint=int(result['SUM(course.point)'])
                sql='SELECT point FROM course WHERE cno=%s'
                cursor.execute(sql,cno)
                result=cursor.fetchone()
                coursePoint=result['point']
                if currentPoint+coursePoint>MAX_POINT:
                    conn.commit()
                    conn.close()
                    return -2
                else:
                    #检查时间是否冲突
                    sql='SELECT begintime,endtime FROM course WHERE cno=%s'
                    cursor.execute(sql,cno)
                    result=cursor.fetchone()
                    conn.commit()
                    conn.close()
                    begintime=int(result['begintime'])
                    endtime=int(result['endtime'])
                    flag=False
                    for i in range(begintime,endtime+1):
                        if courseTime[i]!=None:
                            flag=True
                            break
                    if flag:
                        return -1
                    else:
                        #可以选课
                        return 0

#为学号为sno的同学选课程号为cno的课
def chooseCourse(cno,sno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='INSERT INTO selectcourse(cno,sno) VALUES(%s,%s)'
        cursor.execute(sql,(cno,sno))
        conn.commit()
        conn.close()

#为学号为sno的同学退课程号为cno的课
def dropCourse(cno,sno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='DELETE FROM selectcourse WHERE cno=%s AND sno=%s'
        cursor.execute(sql,(cno,sno))
        conn.commit()
        conn.close()

#检查password是否为学号sno的学生的密码,如果是，返回True，反之，返回False
def checkPassword(sno,password):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT password FROM student WHERE sno=%s'
        cursor.execute(sql,sno)
        result=cursor.fetchone()
        conn.commit()
        conn.close()
        realpassword='**//+='
        if result!=None:
            realpassword=result['password']
        if realpassword==password:
            return True
        else:
            return False

#根据课程号获得课程名和老师名，不支持模糊匹配
def getCnameAndTname(cno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT cname,tname FROM course,teacher WHERE course.tno=teacher.tno AND course.cno=%s'
        cursor.execute(sql,cno)
        result=cursor.fetchone()
        conn.commit()
        conn.close()
        return  result

#将学号为sno的学生的登录密码改为password
def changePassword(sno,password):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='UPDATE student SET password=%s WHERE sno=%s'
        cursor.execute(sql,(password,sno))
        conn.commit()
        conn.close()

#为学号为sno同学申请课程号为cno的课
#先检查是否已经存在于选课申请表中，如果已经存在，返回False
#如果选课申请表中不存在这门课，那么将选课申请插入表中，并返回True
def applyForCourse(sno,cno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT * FROM applicationforcourse WHERE sno=%s AND cno=%s'
        cursor.execute(sql,(sno,cno))
        result=cursor.fetchone()

        returnFlag=False

        #如果还没有这个申请，则将这个申请插入到选课申请表中
        if result==None:
            sql1='INSERT INTO applicationforcourse(sno,cno) VALUES(%s,%s)'
            cursor.execute(sql1,(sno,cno))
            returnFlag=True

        conn.commit()
        conn.close()
        return returnFlag

#获得学号为sno的同学所有的选课申请的所有信息，返回一个字典
#如果没有则返回（）
def GetApplicationForCourse(sno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT applicationforcourse.cno,results,reply,tname FROM applicationforcourse,course,teacher WHERE sno=%s and applicationforcourse.cno=course.cno and course.tno=teacher.tno'
        cursor.execute(sql,sno)
        result=cursor.fetchall()
        conn.commit()
        conn.close()

        return result

#根据学号sno得到该同学选的所有课的教材信息，返回一个字典
#如果没有则返回（）
def GetTextbookInfo(sno):
    conn=pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='SELECT course.cno,cname,tname,bookname FROM selectcourse,course,teacher,textbook WHERE selectcourse.sno=%s and selectcourse.cno=course.cno and course.tno=teacher.tno and textbook.cno=course.cno and textbook.tno=teacher.tno'
        cursor.execute(sql,sno)
        result=cursor.fetchall()
        conn.commit()
        conn.close()
        return result

#将课程的开始时间和结束时间转成一个可显示的字符串
def timeToString(begintime,endtime):
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    day=int(begintime/13)
    begin=begintime-day*13
    end=endtime-day*13
    s=week[day]+'\n'+str(begin)+'-'+str(end)
    return s

if __name__=='__main__':
    conn = pymysql.connect(**config)
    with conn.cursor() as cursor:
        sql='select * from course'
        cursor.execute(sql)
        result=cursor.fetchall()

    print(GetSelectiveCourse('','',''))
    print(GetCourseSelectedNumber('1000001'))
    print(checkPassword('100000010',''))
    getCnameAndTname('1000002')
    applyForCourse('100000000','1000000')

    print(GetApplicationForCourse('100000001'))
    print(GetTextbookInfo('100000001'))
