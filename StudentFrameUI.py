import wx
import StudentController
import LoginFrameUI


class StudentFrame(wx.Frame):
    def __init__(self,parent,title,sno,sname):
        super(StudentFrame,self).__init__(parent,title=title,size=(1300,700))
        self.sno=sno
        self.initUI(sname)
        self.Center()
        self.Show()

        #一个人每周的所有课用一个7*13=91的列表表示，如果这一节次没有课，那么就是一个None元素，如果有课，就用课程名来表示
        self.courseTime=[]
        self.initCourseTime()
        self.refreshCourseTime()

        #用来保存显示可选课程结果的所有label，选课界面用来刷新
        self.courseLabel=[]

        #用来保存所有已选课程结果的label，退课界面用来刷新
        self.SelectedCourseLabel=[]

        #用来保存查看选课申请界面的label，用来刷新
        self.ApplyForCourseLabel=[]

        #用来保存教材信息界面的label，用来刷新
        self.TextbookInfoLabel=[]

        #用来保存选课申请界面的文本输入框
        self.ApplyTextCtrl=[]

    #初始化学生的课程时间列表为92个NULL
    def initCourseTime(self):
        for i in range(0,93):
            self.courseTime.append(None)

    #刷新学生的课程时间
    def refreshCourseTime(self):
        for i in range(1,92):
            self.courseTime[i]=None

        courseResult=StudentController.GetCourse(self.sno)
        for dic in courseResult:
            begintime=dic['begintime']
            endtime=dic['endtime']
            cname=dic['cname']
            for i in range(begintime,endtime+1):
                self.courseTime[i]=cname

    #初始化主界面，包括左边的按键还有所有分界面的panel
    def initUI(self,sname):
        #设置欢迎字体样式
        f=wx.Font(25,wx.ROMAN,wx.ITALIC,wx.BOLD,True)
        s='尊敬的'+sname
        self.warmGreeting1=wx.StaticText(self,-1,label=s,pos=(10,10),size=(150,50),style=wx.ALIGN_LEFT)
        self.warmGreeting2=wx.StaticText(self,-1,label='欢迎使用学生选课系统',pos=(10,65),size=(150,50),style=wx.ALIGN_CENTER)
        self.warmGreeting1.SetFont(f)
        self.warmGreeting2.SetFont(f)
        #加入功能选择按键
        #按键的字体
        f2=wx.Font(15,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        #查看课表
        self.firstButton=wx.Button(self,label='查看课表',pos=(30,150),size=(120,40),style=wx.ALIGN_LEFT)
        self.firstButton.SetFont(f2)
        self.firstButton.Bind(wx.EVT_BUTTON,self.showTables)
        #选课
        self.secondButton=wx.Button(self,label='选课',pos=(30,210),size=(120,40),style=wx.ALIGN_LEFT)
        self.secondButton.SetFont(f2)
        self.secondButton.Bind(wx.EVT_BUTTON,self.SelectCourse)
        #退课
        self.thirdButton = wx.Button(self, label='退课', pos=(30, 270), size=(120, 40), style=wx.ALIGN_LEFT)
        self.thirdButton.SetFont(f2)
        self.thirdButton.Bind(wx.EVT_BUTTON,self.initDropCourseUI)
        #选课申请
        self.fourthButton=wx.Button(self, label='选课申请', pos=(30, 330), size=(120, 40), style=wx.ALIGN_LEFT)
        self.fourthButton.SetFont(f2)
        self.fourthButton.Bind(wx.EVT_BUTTON,self.initApplyForCourseUI)
        #查看申请结果
        self.fifthButton=wx.Button(self,label='查看申请结果',pos=(30,390),size=(120,40),style=wx.ALIGN_LEFT)
        self.fifthButton.SetFont(f2)
        self.fifthButton.Bind(wx.EVT_BUTTON,self.initResultForApplication)
        #修改密码
        self.sixthButton = wx.Button(self, label='修改密码', pos=(30, 450), size=(120, 40), style=wx.ALIGN_LEFT)
        self.sixthButton.SetFont(f2)
        self.sixthButton.Bind(wx.EVT_BUTTON,self.initChangePasswordUI)
        #查看教材信息
        self.seventhButton = wx.Button(self, label='查看教材信息', pos=(30, 510), size=(120, 40), style=wx.ALIGN_LEFT)
        self.seventhButton.SetFont(f2)
        self.seventhButton.Bind(wx.EVT_BUTTON,self.initTextbookInfoUI)
        #退出登录
        self.eighthButton=wx.Button(self,label='退出登录',pos=(30,570),size=(120,40),style=wx.ALIGN_LEFT)
        self.eighthButton.SetFont(f2)
        self.eighthButton.Bind(wx.EVT_BUTTON,self.exitSystem)

        #设置显示课表的panel
        self.panel1=wx.Panel(self,pos=(200,120),size=(1000,500))
        self.panel1.SetBackgroundColour('white')
        #设置课表本体，共有8*14=112个StaticText组成，所有标签放到一个列表中去
        self.labels=[]
        self.panel1.Hide()

        #设置选课用的panel
        self.panel2 = wx.Panel(self, pos=(200, 120), size=(1000, 500))
        self.panel2.SetBackgroundColour('white')
        self.initSelectCourseUI()
        self.panel2.Hide()

        #设置退课用的panel
        self.panel3=wx.Panel(self,pos=(200,120),size=(1000,500))
        self.panel3.SetBackgroundColour('white')
        self.panel3.Hide()

        #设置修改密码用的panel
        self.panel4=wx.Panel(self,pos=(200,120),size=(1000,500))
        self.panel4.SetBackgroundColour('white')
        self.panel4.Hide()

        #设置选课申请用的panel
        self.panel5=wx.Panel(self,pos=(200,120),size=(1000,500))
        self.panel5.SetBackgroundColour('white')
        self.panel5.Hide()

        #设置查看申请结果用的panel
        self.panel6=wx.Panel(self,pos=(200,120),size=(1000,500))
        self.panel6.SetBackgroundColour('white')
        self.panel6.Hide()

        #设置查看教材信息用的panel
        self.panel7=wx.Panel(self,pos=(200,120),size=(1000,500))
        self.panel7.SetBackgroundColour('white')
        self.panel7.Hide()

    #初始化查看教材信息的UI
    def initTextbookInfoUI(self,event):
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.panel6.Hide()
        self.panel7.Show()

        for label in self.TextbookInfoLabel:
            label.Hide()
        self.TextbookInfoLabel.clear()

        result=StudentController.GetTextbookInfo(self.sno)
        if result==():
            f=wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
            label1=wx.StaticText(self.panel7,pos=(370,200),size=(200,100),label=u'你没有教材信息!')
            label1.SetFont(f)
            self.TextbookInfoLabel.append(label1)
        else:
            f1=wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
            label2=wx.StaticText(self.panel7,pos=(20,20),size=(200,35),label=u'课程号',style=wx.ALIGN_CENTER)
            label2.SetFont(f1)
            label2.SetBackgroundColour('sky blue')
            self.TextbookInfoLabel.append(label2)

            label3 = wx.StaticText(self.panel7, pos=(220, 20), size=(200, 35), label=u'课程名', style=wx.ALIGN_CENTER)
            label3.SetFont(f1)
            self.TextbookInfoLabel.append(label3)

            label4 = wx.StaticText(self.panel7, pos=(420, 20), size=(200, 35), label=u'任课老师', style=wx.ALIGN_CENTER)
            label4.SetFont(f1)
            label4.SetBackgroundColour('sky blue')
            self.TextbookInfoLabel.append(label4)

            label5 = wx.StaticText(self.panel7, pos=(620, 20), size=(200, 35), label=u'教材', style=wx.ALIGN_CENTER)
            label5.SetFont(f1)
            self.TextbookInfoLabel.append(label5)

            initX=20
            initY=60
            for dic in result:
                cno=dic['cno']
                cname=dic['cname']
                tname=dic['tname']
                bookname=dic['bookname']

                label01=wx.StaticText(self.panel7,pos=(initX,initY),size=(200,35),style=wx.ALIGN_CENTER)
                label01.SetFont(f1)
                label01.SetLabel(cno)
                self.TextbookInfoLabel.append(label01)

                label02 = wx.StaticText(self.panel7, pos=(initX+200, initY), size=(200, 35), style=wx.ALIGN_CENTER)
                label02.SetFont(f1)
                label02.SetLabel(cname)
                self.TextbookInfoLabel.append(label02)

                label03 = wx.StaticText(self.panel7, pos=(initX+400, initY), size=(200, 35), style=wx.ALIGN_CENTER)
                label03.SetFont(f1)
                label03.SetLabel(tname)
                self.TextbookInfoLabel.append(label03)

                label04 = wx.StaticText(self.panel7, pos=(initX+600, initY), size=(200, 35), style=wx.ALIGN_CENTER)
                label04.SetFont(f1)
                label04.SetLabel(bookname)
                self.TextbookInfoLabel.append(label04)

                initY+=35


    #初始化查看选课申请结果界面
    def initResultForApplication(self,event):
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.panel7.Hide()
        self.panel6.Show()

        for label in self.ApplyForCourseLabel:
            label.Hide()

        self.ApplyForCourseLabel.clear()

        f=wx.Font(17,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        label1=wx.StaticText(self.panel6,pos=(20,20),size=(150,30),label=u'课程号',style=wx.ALIGN_CENTER)
        label1.SetFont(f)
        label1.SetBackgroundColour('sky blue')

        label2=wx.StaticText(self.panel6,pos=(170,20),size=(150,30),label=u'任课老师名',style=wx.ALIGN_CENTER)
        label2.SetFont(f)
        label2.SetBackgroundColour('white')

        label3=wx.StaticText(self.panel6,pos=(320,20),size=(150,30),label=u'结果',style=wx.ALIGN_CENTER)
        label3.SetFont(f)
        label3.SetBackgroundColour('sky blue')

        label4=wx.StaticText(self.panel6,pos=(470,20),size=(400,30),label=u'回复理由',style=wx.ALIGN_CENTER)
        label4.SetFont(f)
        label4.SetBackgroundColour('white')

        result=StudentController.GetApplicationForCourse(self.sno)

        if result==():
            f1=wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
            label5=wx.StaticText(self.panel6,pos=(30,70),size=(200,60),label=u'你没有申请课程!')
            label5.SetFont(f1)
            self.ApplyForCourseLabel.append(label5)
        else:
            initX=20
            initY=70
            for dic in result:
                f2=wx.Font(18,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)

                label01=wx.StaticText(self.panel6,pos=(initX,initY),size=(150,35),style=wx.ALIGN_CENTER)
                label01.SetLabel(dic['cno'])
                label01.SetFont(f2)
                self.ApplyForCourseLabel.append(label01)

                label02=wx.StaticText(self.panel6,pos=(initX+150,initY),size=(150,35),style=wx.ALIGN_CENTER)
                label02.SetLabel(dic['tname'])
                label02.SetFont(f2)
                self.ApplyForCourseLabel.append(label02)

                label03=wx.StaticText(self.panel6,pos=(initX+300,initY),size=(150,35),style=wx.ALIGN_CENTER)
                results=dic['results']
                if results==None:
                    results=u'未处理'
                label03.SetLabel(results)
                label03.SetFont(f2)
                self.ApplyForCourseLabel.append(label03)

                label04=wx.StaticText(self.panel6,pos=(initX+450,initY),size=(400,35),style=wx.ALIGN_CENTER)
                reply=dic['reply']
                if reply==None:
                    reply=u''
                f3=wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
                label04.SetLabel(reply)
                label04.SetFont(f3)
                self.ApplyForCourseLabel.append(label04)

                initY+=35

    #初始化选课申请界面
    def initApplyForCourseUI(self,event):
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel6.Hide()
        self.panel7.Hide()
        self.panel5.Show()

        for tc in self.ApplyTextCtrl:
            tc.Hide()
        self.ApplyTextCtrl.clear()

        f=wx.Font(18,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        label1=wx.StaticText(self.panel5,label=u'请输入课程号',pos=(20,25),size=(100,30))
        label1.SetFont(f)

        f1 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.tc001=wx.TextCtrl(self.panel5,pos=(200,20),size=(200,30))
        self.tc001.SetFont(f1)
        self.tc001.Bind(wx.EVT_KILL_FOCUS,self.setCnameAndTname)
        self.ApplyTextCtrl.append(self.tc001)

        label2=wx.StaticText(self.panel5,pos=(20,70),size=(100,30),label=u'课程名')
        label2.SetFont(f)

        self.tc002=wx.TextCtrl(self.panel5,pos=(200,70),size=(200,30),style=wx.TE_READONLY)
        self.tc002.SetFont(f1)
        self.ApplyTextCtrl.append(self.tc002)

        label3=wx.StaticText(self.panel5,pos=(450,20),size=(100,30),label=u'任课老师')
        label3.SetFont(f)

        self.tc003 = wx.TextCtrl(self.panel5, pos=(630, 20), size=(200, 30), style=wx.TE_READONLY)
        self.tc003.SetFont(f1)
        self.ApplyTextCtrl.append(self.tc003)

        f2=wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        label4=wx.StaticText(self.panel5,pos=(20,110),size=(200,30),label=u'请输入申请理由（不能为空,不多于100字）:')
        label4.SetFont(f2)

        self.tc004=wx.TextCtrl(self.panel5,pos=(20,140),size=(800,350),style=wx.TE_MULTILINE|wx.HSCROLL)
        self.tc004.SetFont(f1)
        self.ApplyTextCtrl.append(self.tc004)

        button1=wx.Button(self.panel5,pos=(680,70),size=(120,40),label=u'确认申请')
        button1.SetFont(f2)
        button1.Bind(wx.EVT_BUTTON,self.confirmApplyForCourse)


    #选课申请界面确认选课按钮所用的函数
    def confirmApplyForCourse(self,event):
        cno=self.tc001.GetValue()
        cname=self.tc002.GetValue()
        tname=self.tc003.GetValue()
        reason=self.tc004.GetValue()

        if cno=='' or cname=='' or tname=='':
            dlg=wx.MessageDialog(None,u'请输入有效的课程号！',u'错误提示',style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif reason=='':
            dlg = wx.MessageDialog(None, u'申请理由不可为空！', u'错误提示', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(reason)>200:
            dlg = wx.MessageDialog(None, u'申请理由过长', u'错误提示', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dlg=wx.MessageDialog(None,u'选课申请一经提交，不可撤销\n是否确认申请',u'警告信息',style=wx.YES_NO)
            if dlg.ShowModal()==wx.ID_YES:
                dlg.Destroy()
                if StudentController.applyForCourse(self.sno,cno)==False:
                    dlg2=wx.MessageDialog(None,u'申请失败，你已经申请过该门课程',u'错误信息',style=wx.OK)
                    dlg2.ShowModal()
                    dlg2.Destroy()
                else:
                    dlg2 = wx.MessageDialog(None, u'申请成功！\n请到查看申请界面查看申请结果', u'错误信息', style=wx.OK)
                    dlg2.ShowModal()
                    dlg2.Destroy()
            else:
                dlg.Destroy()


    #选课申请界面当焦点离开课程号编辑框时所用的函数，用来自动获得课程名和任课老师名字
    def setCnameAndTname(self,event):
        print(1)

        cno=self.tc001.GetValue()
        print('cno=',cno)
        self.refreshCourseTime()
        result=StudentController.getCnameAndTname(cno)
        if cno=='':
            pass
        elif result==None:
            dlg=wx.MessageDialog(None,u'这门课不存在',u'错误信息',style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.tc001.Clear()
            self.tc002.Clear()
            self.tc003.Clear()
            #self.tc001.SetFocus()
        elif StudentController.CheckCourse(cno,self.sno,self.courseTime)!=0:
            dlg = wx.MessageDialog(None, u'你不能申请这门课', u'错误信息', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.tc001.Clear()
            self.tc002.Clear()
            self.tc003.Clear()
            #self.tc001.SetFocus()
        else:
            self.tc002.SetValue(result['cname'])
            self.tc003.SetValue(result['tname'])

        event.Skip()

    #初始化修改密码界面
    def initChangePasswordUI(self,event):
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel5.Hide()
        self.panel6.Hide()
        self.panel7.Hide()
        self.panel4.Show()

        f=wx.Font(18,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        label1=wx.StaticText(self.panel4,label=u'请输入原密码',pos=(200,100),size=(100,30))
        label1.SetFont(f)
        label2=wx.StaticText(self.panel4,label=u'请输入新密码',pos=(200,150),size=(100,30))
        label2.SetFont(f)
        label3=wx.StaticText(self.panel4,label=u'请确认新密码',pos=(200,200),size=(100,30))
        label3.SetFont(f)

        f1=wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        self.tc01=wx.TextCtrl(self.panel4,pos=(450,100),size=(200,30),style=wx.TE_PASSWORD)
        self.tc01.SetFont(f1)
        self.tc02=wx.TextCtrl(self.panel4,pos=(450,150),size=(200,30),style=wx.TE_PASSWORD)
        self.tc02.SetFont(f1)
        self.tc03=wx.TextCtrl(self.panel4,pos=(450,200),size=(200,30),style=wx.TE_PASSWORD)
        self.tc03.SetFont(f1)

        button1=wx.Button(self.panel4,label=u'确认',pos=(280,270),size=(100,35))
        button1.SetFont(f)
        button2=wx.Button(self.panel4,label=u'取消',pos=(480,270),size=(100,35))
        button2.SetFont(f)

        button1.Bind(wx.EVT_BUTTON,self.changePassword)

    #修改密码界面按钮所用的函数
    def changePassword(self,event):
        rawPassword=self.tc01.GetValue()
        newPassword=self.tc02.GetValue()
        repeatPassword=self.tc03.GetValue()

        if StudentController.checkPassword(self.sno,rawPassword)==False:
            self.tc01.Clear()
            self.tc02.Clear()
            self.tc03.Clear()
            self.tc01.SetFocus()

            dlg=wx.MessageDialog(None,u'原密码不正确！请重新输入',u'错误提示',style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(newPassword)>=45:
            self.tc02.Clear()
            self.tc03.Clear()
            self.tc02.SetFocus()

            dlg=wx.MessageDialog(None,u'新密码过长！请重新输入',u'错误提示',style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(newPassword)<=4:
            self.tc02.Clear()
            self.tc03.Clear()
            self.tc02.SetFocus()

            dlg = wx.MessageDialog(None, u'新密码过短！请重新输入', u'错误提示', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif newPassword==rawPassword:
            self.tc02.Clear()
            self.tc03.Clear()
            self.tc02.SetFocus()

            dlg = wx.MessageDialog(None, u'新密码不能与原密码一致！\n请重新输入', u'错误提示', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        elif newPassword!=repeatPassword:
            self.tc02.Clear()
            self.tc03.Clear()
            self.tc02.SetFocus()

            dlg = wx.MessageDialog(None, u'两次输入密码不一致！\n请重新输入', u'错误提示', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            StudentController.changePassword(self.sno,newPassword)
            dlg = wx.MessageDialog(None, u'密码修改成功\n请重新登录', u'操作成功', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

            self.Close()
            LoginFrameUI.LoginFrame(None,title='登录选课系统')

    #初始化退课界面
    def initDropCourseUI(self,event):
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.panel6.Hide()
        self.panel7.Hide()
        self.panel3.Show()

        self.refreshDropCourseUI()

    #退课后刷新退课界面
    def refreshDropCourseUI(self):
        for label in self.SelectedCourseLabel:
            label.Hide()

        self.SelectedCourseLabel.clear()

        result=StudentController.GetCourse(self.sno)
        if result==():
            f=wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
            label1=wx.StaticText(self.panel3,label=u'你没有已选课程!',pos=(400,200),size=(200,100))
            label1.SetFont(f)
            self.SelectedCourseLabel.append(label1)
        else:
            initX=5
            initY=5
            f=wx.Font(15,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
            #标签1：课程号
            label1=wx.StaticText(self.panel3,label=u'课程号',pos=(initX,initY),size=(150,35),style=wx.ALIGN_CENTER)
            label1.SetFont(f)
            self.SelectedCourseLabel.append(label1)
            #标签2：课程名
            label2 = wx.StaticText(self.panel3, label=u'课程名', pos=(initX+150, initY), size=(150, 35),style=wx.ALIGN_CENTER)
            label2.SetFont(f)
            self.SelectedCourseLabel.append(label2)
            #标签3：老师名
            label3 = wx.StaticText(self.panel3, label=u'老师名', pos=(initX+300, initY), size=(150, 35),style=wx.ALIGN_CENTER)
            label3.SetFont(f)
            self.SelectedCourseLabel.append(label3)
            #标签4：课程时间
            label4 = wx.StaticText(self.panel3, label=u'课程时间', pos=(initX+450, initY), size=(150, 45),style=wx.ALIGN_CENTER)
            label4.SetFont(f)
            self.SelectedCourseLabel.append(label4)
            # 标签5：
            label5 = wx.StaticText(self.panel3, label=u'学分', pos=(initX + 600, initY), size=(100, 45),style=wx.ALIGN_CENTER)
            label5.SetFont(f)
            self.SelectedCourseLabel.append(label5)

            initY+=45

            for dic in result:
                cno=dic['cno']
                cname=dic['cname']
                tname=dic['tname']
                point=str(dic['point'])
                begintime=int(dic['begintime'])
                endtime=int(dic['endtime'])
                ctime=StudentController.timeToString(begintime,endtime)

                label1 = wx.StaticText(self.panel3, label=cno, pos=(initX, initY), size=(150, 45),style=wx.ALIGN_CENTER)
                label1.SetFont(f)
                self.SelectedCourseLabel.append(label1)
                # 标签2：课程名
                label2 = wx.StaticText(self.panel3, label=cname, pos=(initX + 150, initY), size=(150, 45),style=wx.ALIGN_CENTER)
                label2.SetFont(f)
                self.SelectedCourseLabel.append(label2)
                # 标签3：老师名
                label3 = wx.StaticText(self.panel3, label=tname, pos=(initX + 300, initY), size=(150, 45),style=wx.ALIGN_CENTER)
                label3.SetFont(f)
                self.SelectedCourseLabel.append(label3)
                # 标签4：课程时间
                label4 = wx.StaticText(self.panel3, label=ctime, pos=(initX + 450, initY), size=(150, 45),style=wx.ALIGN_CENTER)
                label4.SetFont(f)
                self.SelectedCourseLabel.append(label4)
                # 标签5：学分
                label5 = wx.StaticText(self.panel3, label=point, pos=(initX + 600, initY), size=(100, 45),style=wx.ALIGN_CENTER)
                label5.SetFont(f)
                self.SelectedCourseLabel.append(label5)
                #退课按钮
                dropButton=wx.Button(self.panel3,label='退课',pos=(initX+700,initY),size=(120,35),style=wx.ALIGN_LEFT)
                dropButton.SetFont(f)
                dropButton.Bind(wx.EVT_BUTTON,lambda evt,ccno=cno:self.dropCourse(ccno))
                self.SelectedCourseLabel.append(dropButton)

                initY+=45

    #退课界面退课按钮所用函数
    def dropCourse(self,cno):
        StudentController.dropCourse(cno,self.sno)
        self.refreshDropCourseUI()

    #初始化选课界面
    def initSelectCourseUI(self):
        # 课程列表第一行字体格式
        f7 = wx.Font(17, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        # label1
        label1 = wx.StaticText(self.panel2, label='课程号', pos=(0, 5), size=(150, 35), style=wx.ALIGN_CENTER)
        label1.SetFont(f7)
        label1.SetBackgroundColour('sky blue')
        # label2
        label2 = wx.StaticText(self.panel2, label='课程名', pos=(150, 5), size=(150, 35), style=wx.ALIGN_CENTER)
        label2.SetFont(f7)
        label2.SetBackgroundColour('white')
        # label3
        label3 = wx.StaticText(self.panel2, label='任课老师名', pos=(300, 5), size=(150, 35), style=wx.ALIGN_CENTER)
        label3.SetFont(f7)
        label3.SetBackgroundColour('sky blue')
        # label4
        label4 = wx.StaticText(self.panel2, label='时间', pos=(450, 5), size=(150, 35), style=wx.ALIGN_CENTER)
        label4.SetFont(f7)
        label4.SetBackgroundColour('white')
        # label5
        label5 = wx.StaticText(self.panel2, label='选课人数/上限', pos=(600, 5), size=(150, 35), style=wx.ALIGN_CENTER)
        label5.SetFont(f7)
        label5.SetBackgroundColour('sky blue')

        # 四个文本输入框，用来精确查找课程
        # 文本框输入字体的格式
        f8 = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        # tc1
        self.tc1 = wx.TextCtrl(self.panel2, pos=(0, 40), size=(150, 35), style=wx.ALIGN_LEFT)
        self.tc1.SetFont(f8)
        # tc2
        self.tc2 = wx.TextCtrl(self.panel2, pos=(150, 40), size=(150, 35), style=wx.ALIGN_LEFT)
        self.tc2.SetFont(f8)
        # tc3
        self.tc3 = wx.TextCtrl(self.panel2, pos=(300, 40), size=(150, 35), style=wx.ALIGN_LEFT)
        self.tc3.SetFont(f8)
        # tc4
        tc4 = wx.TextCtrl(self.panel2, pos=(450, 40), size=(150, 35), value='暂不支持', style=wx.ALIGN_LEFT|wx.TE_READONLY)
        tc4.SetFont(f8)
        # tc5
        tc4 = wx.TextCtrl(self.panel2, pos=(600, 40), size=(150, 35), value='暂不支持', style=wx.ALIGN_LEFT|wx.TE_READONLY)
        tc4.SetFont(f8)

        #用来显示没有可选课程的scrollwindow
        self.scrollwindow1=wx.ScrolledWindow(parent=self.panel2,pos=(0,80),size=(750,400))
        self.scrollwindow1.SetBackgroundColour('green')
        self.scrollwindow1.SetScrollbar(1,1,600,400)
        #用来显示课程列表的scrollwindow
        self.scrollwindow2 = wx.ScrolledWindow(parent=self.panel2, pos=(0, 80), size=(920, 400))
        self.scrollwindow2.SetBackgroundColour('white')
        self.scrollwindow2.SetScrollbar(0,20,0,20)

        self.scrollwindow1.Hide()
        self.scrollwindow2.Hide()

    #显示并刷新课表所用的函数
    def showTables(self,event):
        #隐藏别的panel
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.panel6.Hide()
        self.panel7.Hide()
        #将自己的panel显示出来
        self.panel1.Show()
        #将课表更新
        self.refreshCourseTime()
        # 课表显示所用字体
        #课表第一行
        f3 = wx.Font(25, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        #课标第一列
        f4=wx.Font(13,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        #课表左上第一格
        f5 = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        #课表主体
        f6=wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        #一周对应七天
        week=['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
        timelabel=['第一节\n8:00-8:45',
                   '第二节\n8:55-9:40',
                   '第三节\n9:55-10:40',
                   '第四节\n10：50-11:35',
                   '第五节\n11:45-12:30',
                   '第六节\n13:30-14:15',
                   '第七节\n14:25-15:10',
                   '第八节\n15:25-16:10',
                   '第九节\n16:20-17:05',
                   '第十节\n17:20-18:00',
                   '第十一节\n18:30-19:10',
                   '第十二节\n19:25-20:10',
                   '第十三节\n20:20-21:05',]
        for i in range(0,8):
            for j in range(0,14):
                #将表格画出来
                absoluteX=20+120*i
                absoluteY=5+35*j
                flag=True
                if i%2==j%2:
                    flag=True
                else:
                    flag=False
                label=wx.StaticText(self.panel1,pos=(absoluteX,absoluteY),size=(120,35),style=wx.ALIGN_CENTER)
                if i==0 and j==0:
                    label.SetFont(f5)
                    label.SetLabel('节次/周次')
                elif j==0 and i!=0:
                    label.SetFont(f3)
                    label.SetLabel(week[i-1])
                elif i==0 and j!=0:
                    label.SetFont(f4)
                    label.SetLabel(timelabel[j-1])
                else:
                    #将课填到课表中对应位置
                    label.SetFont(f6)
                    k=13*(i-1)+j
                    if self.courseTime[k]!=None:
                        label.SetLabel(self.courseTime[k])
                    else:
                        label.SetLabel('')
                if flag==True:
                    label.SetBackgroundColour('sky blue')
                else:
                    label.SetBackgroundColour('white')
                self.labels.append(label)

    #主界面选课button所用函数。用来转到选课界面
    def SelectCourse(self,event):
        #将别的功能对应的panel隐藏起来，将选课功能对应的panel显示出来
        self.panel1.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel5.Hide()
        self.panel6.Hide()
        self.panel7.Hide()
        self.panel2.Show()

        for label in self.courseLabel:
            label.Hide()

        #搜索按钮
        f8 = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        searchButton=wx.Button(self.panel2,pos=(770,40),label='搜索',size=(150,35),style=wx.ALIGN_LEFT)
        searchButton.SetFont(f8)
        searchButton.Bind(wx.EVT_BUTTON,self.showSelectiveCourse)

    #选课界面搜索按钮的函数，用来显示给定条件下的可选课程
    def showSelectiveCourse(self,event):
        cno=self.tc1.GetValue()
        cname=self.tc2.GetValue()
        tname=self.tc3.GetValue()
        result=StudentController.GetSelectiveCourse(cno,cname,tname)

        initX=0
        initY=0

        if result==():
            self.scrollwindow2.Hide()
            self.scrollwindow1.Show()

            showNoResult=wx.StaticText(self.scrollwindow1,label=u'没有可选课程！',pos=(initX,initY),size=(200,100))
            f9=wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
            showNoResult.SetFont(f9)
        else:
            #print(result)

            for mlabel in self.courseLabel:
                #print('mlabel=',mlabel)
                mlabel.Hide()

            self.courseLabel.clear()

            self.scrollwindow1.Hide()
            self.scrollwindow2.Show()
            for dic in result:
                cnoValue=dic['cno']
                cnameValue=dic['cname']
                tnameValue=dic['tname']
                limits=dic['limits']
                ctime=StudentController.timeToString(dic['begintime'],dic['endtime'])
                pNumber=StudentController.GetCourseSelectedNumber(cnoValue)
                pNumber_limits=str(pNumber)+'/'+str(limits)

                #label用的字体
                f10=wx.Font(13,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
                #第一个label
                clabel1=wx.StaticText(self.scrollwindow2,pos=(initX,initY),size=(150,35),style=wx.ALIGN_CENTER)
                clabel1.SetLabel(cnoValue)
                clabel1.SetFont(f10)
                self.courseLabel.append(clabel1)
                #第二个label
                clabel2 = wx.StaticText(self.scrollwindow2, pos=(initX+150, initY), size=(150, 35), style=wx.ALIGN_CENTER)
                clabel2.SetLabel(cnameValue)
                clabel2.SetFont(f10)
                self.courseLabel.append(clabel2)
                #第三个label
                clabel3 = wx.StaticText(self.scrollwindow2, pos=(initX+300, initY), size=(150, 35), style=wx.ALIGN_CENTER)
                clabel3.SetLabel(tnameValue)
                clabel3.SetFont(f10)
                self.courseLabel.append(clabel3)
                #第四个label
                clabel4 = wx.StaticText(self.scrollwindow2, pos=(initX+450, initY), size=(150, 35), style=wx.ALIGN_CENTER)
                clabel4.SetLabel(ctime)
                clabel4.SetFont(f10)
                self.courseLabel.append(clabel4)
                #第五个label
                clabel5 = wx.StaticText(self.scrollwindow2, pos=(initX+600, initY), size=(150, 35), style=wx.ALIGN_CENTER)
                clabel5.SetLabel(pNumber_limits)
                clabel5.SetFont(f10)
                self.courseLabel.append(clabel5)

                #选课按钮
                selectCourseButton=wx.Button(self.scrollwindow2,label='选课',pos=(initX+770,initY),size=(120,35),style=wx.ALIGN_LEFT)
                selectCourseButton.SetFont(f10)
                self.courseLabel.append(selectCourseButton)

                cno=clabel1.GetLabel()
                selectCourseButton.Bind(wx.EVT_BUTTON,lambda evt,i=cno:self.chooseCourse(i))

                initY+=35

    #选课界面选课按钮所用的函数
    def chooseCourse(self,cno):
        self.refreshCourseTime()
        result=StudentController.CheckCourse(cno,self.sno,self.courseTime)
        message=u''
        title=u'错误信息'
        if result==-4:
            message=u'这门课已经在你的课程列表中！'
        elif result==-3:
            message=u'选课人数已到上限！'
        elif result==-2:
            message=u'你的学分已经超过上限！'
        elif result==-1:
            message=u'课程时间冲突'
        else:
            title=u'操作成功'
            message=u'选课成功'
            StudentController.chooseCourse(cno,self.sno)
        dlg=wx.MessageDialog(None,message,title,style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    #退出登录button所用函数
    def exitSystem(self,event):
        dlg=wx.MessageDialog(None,u'是否确认退出？',u'退出系统',wx.YES_NO|wx.ICON_QUESTION)
        result=dlg.ShowModal()
        #如果按是则退出，否则不做任何操作
        if result==wx.ID_YES:
            #print(3)
            self.Close()
            #LoginFrameUI.LoginFrame(None, title="登录选课系统")
        dlg.Destroy()

if __name__=='__main__':
    app=wx.App()
    win=StudentFrame(None,'欢迎使用选课系统','100000001','JJF')
    app.MainLoop()