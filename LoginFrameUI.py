import wx
import LoginController
import StudentFrameUI

def confirm(user,password):
    inputuser=user.GetValue()
    inputpassword=password.GetValue()
    result=LoginController.check(inputuser,inputpassword)
    return result

class LoginFrame(wx.Frame):
    def __init__(self,parent,title):
        super(LoginFrame,self).__init__(parent,title=title,size=(370,200))
        self.InitUI()
        self.Center()
        self.Show()

    #界面初始化
    def InitUI(self):
        #设置界面所用字体
        f=wx.Font(20,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        f1=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        f2=wx.Font(15,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)

        self.panel1=wx.Panel(self,-1)

        user=wx.StaticText(self.panel1,label="用户名",pos=(25,13),size=(80,35))
        user.SetFont(f)
        password=wx.StaticText(self.panel1,label="密码",pos=(25,68),size=(80,35))
        password.SetFont(f)

        self.tc1=wx.TextCtrl(self.panel1,pos=(140,10),size=(170,35),style=wx.TE_PROCESS_ENTER)
        self.tc1.SetFont(f)
        self.tc1.Bind(wx.EVT_TEXT_ENTER,self.keyDown)

        self.tc2=wx.TextCtrl(self.panel1,pos=(140,65),size=(170,35),style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.tc2.SetFont(f1)
        self.tc2.Bind(wx.EVT_TEXT_ENTER,self.keyDown)

        confirmButton=wx.Button(self.panel1,label="确认",pos=(80,110),size=(60,30))
        confirmButton.Bind(wx.EVT_BUTTON,self.innerConfirm)
        confirmButton.SetFont(f2)

        closeButton=wx.Button(self.panel1,label="退出",pos=(210,110),size=(60,30))
        closeButton.Bind(wx.EVT_BUTTON,self.close)
        closeButton.SetFont(f2)

    def close(self,event):
        self.Close()

    #按下回车之后的界面逻辑，与按下确认键实现相同的功能
    def keyDown(self,event):
        self.innerConfirm(event)

    #确认按键的逻辑
    def innerConfirm(self,event):
        result=confirm(self.tc1,self.tc2)


        if result==-2:
            dlg=wx.MessageDialog(None,u'用户名不存在',u'错误信息',wx.YES_NO|wx.ICON_QUESTION)
            dlg.ShowModal()
            dlg.Destroy()
            self.tc1.SetValue('')
            self.tc2.SetValue('')
            self.tc1.SetFocus()
        elif result==-1:
            dlg = wx.MessageDialog(None, u'密码错误', u'错误信息', wx.YES_NO | wx.ICON_QUESTION)
            dlg.ShowModal()
            dlg.Destroy()
            self.tc2.SetValue('')
            self.tc2.SetFocus()
        else:
            dlg = wx.MessageDialog(None, u'登陆成功', u'欢迎', wx.YES_NO | wx.ICON_QUESTION)
            dlg.ShowModal()
            #根据result的值启动别的界面
            if result==3:
                self.Close()
                sno=self.tc1.GetValue()
                sname=LoginController.GetStudentName(sno)
                swin=StudentFrameUI.StudentFrame(None,u'学生界面',sno,sname)


if __name__=='__main__':
    app=wx.App()
    win=LoginFrame(None,title="登录选课系统")
    app.MainLoop()