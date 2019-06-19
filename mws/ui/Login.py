import wx
import os
from ui.MainFrame import MainFrame
import util.SqliteUtil as sqliteUtil

###################################################################
# 登录界面
###################################################################

login_title_text = "欢迎使用商品信息管理系统"
user_name_text = "账 号："
password_text = "密 码："
button_ok_text = "登录"
button_exit_text = "退出"


class LoginFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="商品信息管理系统", pos=wx.DefaultPosition,
                          size=wx.Size(774, 340),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(204, 232, 207))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.loginTitle = wx.StaticText(self, wx.ID_ANY, login_title_text, wx.Point(1000, 1000), wx.Size(1500, 100),
                                        wx.ALIGN_CENTRE)
        self.loginTitle.Wrap(-1)
        self.loginTitle.SetFont(wx.Font(45, 70, 90, 90, False, wx.EmptyString))
        self.loginTitle.SetForegroundColour(wx.Colour(255, 0, 128))
        self.loginTitle.SetBackgroundColour(wx.Colour(146, 215, 252))

        bSizer1.Add(self.loginTitle, 0, wx.ALL, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.user_name = wx.StaticText(self, wx.ID_ANY, user_name_text, wx.DefaultPosition, wx.Size(150, 30),
                                       wx.ALIGN_RIGHT)
        self.user_name.Wrap(-1)
        self.user_name.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, wx.EmptyString))

        bSizer3.Add(self.user_name, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.pswd = wx.StaticText(self, wx.ID_ANY, password_text, wx.DefaultPosition, wx.Size(150, 30),
                                  wx.ALIGN_RIGHT)
        self.pswd.Wrap(-1)
        self.pswd.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, wx.EmptyString))

        bSizer3.Add(self.pswd, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        gSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.login_text_id = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, 30), 0)
        self.login_text_id.SetMaxLength(20)
        bSizer4.Add(self.login_text_id, 0, wx.ALL, 5)

        self.login_text_password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, 30),
                                               wx.TE_PASSWORD)
        self.login_text_password.SetMaxLength(20)
        bSizer4.Add(self.login_text_password, 0, wx.ALL, 5)

        gSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer2.Add(gSizer1, 1, wx.EXPAND, 5)

        gSizer2 = wx.GridSizer(1, 2, 0, 0)

        self.button_ok = wx.Button(self, wx.ID_ANY, button_ok_text, wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ok.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, wx.EmptyString))
        gSizer2.Add(self.button_ok, 0, wx.ALL | wx.ALIGN_RIGHT, 40)

        self.button_exit = wx.Button(self, wx.ID_ANY, button_exit_text, wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_exit.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, wx.EmptyString))
        gSizer2.Add(self.button_exit, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 40)

        bSizer2.Add(gSizer2, 1, wx.EXPAND, 1)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_ok.Bind(wx.EVT_BUTTON, self.button_ok_click)
        self.button_exit.Bind(wx.EVT_BUTTON, self.button_exit_click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def button_ok_click(self, event):
        user_id = self.login_text_id.GetValue()
        password = self.login_text_password.GetValue()
        user_id = "admin"
        password = "admin"
        if user_id.strip() == '':
            wx.MessageBox(u'请输入账号', u'错误', wx.OK | wx.ICON_ERROR)
            return

        if password.strip() == '':
            wx.MessageBox(u'请输入密码', u'错误', wx.OK | wx.ICON_ERROR)
            return

        db = sqliteUtil.EasySqlite()
        result = db.execute(
            "select id as userId, ifnull(nickname,id) as nickname, datetime('now') as loginTime from user where id=\'" + user_id + "\' and pwd=\'" + password + "\'")
        if len(result) == 0:
            wx.MessageBox(u'账号或密码错误', u'错误', wx.OK | wx.ICON_ERROR)
        else:
            self.Destroy()
            main_frame = MainFrame(None, result[0])
            main_frame.Show(True)

    def button_exit_click(self, event):
        self.Destroy()
