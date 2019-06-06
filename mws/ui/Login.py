import wx
from ui.MainFrame import MainFrame

###################################################################
# 登录界面
###################################################################

login_title_text = "登陆"
user_name_text = "用户名："
password_text = "  密码："
button_ok_text = "确定"
button_clear_text = "清除"
button_exit_text = "退出"


class LoginFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=login_title_text, pos=wx.DefaultPosition,
                          size=wx.Size(774, 340),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(204, 232, 207))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.loginTitle = wx.StaticText(self, wx.ID_ANY, login_title_text, wx.Point(1000, 1000), wx.Size(1500, 100),
                                        wx.ALIGN_CENTRE)
        self.loginTitle.Wrap(-1)
        self.loginTitle.SetFont(wx.Font(50, 70, 90, 90, False, wx.EmptyString))
        self.loginTitle.SetForegroundColour(wx.Colour(255, 0, 128))
        self.loginTitle.SetBackgroundColour(wx.Colour(146, 215, 252))

        bSizer1.Add(self.loginTitle, 0, wx.ALL, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.user_name = wx.StaticText(self, wx.ID_ANY, user_name_text, wx.DefaultPosition, wx.Size(150, 30),
                                       wx.ALIGN_RIGHT)
        self.user_name.Wrap(-1)
        self.user_name.SetFont(wx.Font(20, 71, 90, 92, False, wx.EmptyString))

        bSizer3.Add(self.user_name, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.pswd = wx.StaticText(self, wx.ID_ANY, password_text, wx.DefaultPosition, wx.Size(150, 30),
                                  wx.ALIGN_RIGHT)
        self.pswd.Wrap(-1)
        self.pswd.SetFont(wx.Font(20, 71, 90, 92, False, wx.EmptyString))

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

        gSizer2 = wx.GridSizer(1, 3, 0, 0)

        self.button_ok = wx.Button(self, wx.ID_ANY, button_ok_text, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.button_ok, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.button_clear = wx.Button(self, wx.ID_ANY, button_clear_text, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.button_clear, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.button_exit = wx.Button(self, wx.ID_ANY, button_exit_text, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.button_exit, 0, wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        bSizer2.Add(gSizer2, 1, wx.EXPAND, 1)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_ok.Bind(wx.EVT_BUTTON, self.button_ok_click)
        self.button_clear.Bind(wx.EVT_BUTTON, self.button_clear_click)
        self.button_exit.Bind(wx.EVT_BUTTON, self.button_exit_click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def button_ok_click(self, event):
        self.Destroy()
        main_frame = MainFrame(None)
        main_frame.Show(True)

    def button_clear_click(self, event):
        self.login_text_id.Clear()
        self.login_text_password.Clear()

    def button_exit_click(self, event):
        self.Destroy()
