import wx
from ui.Login import LoginFrame

###################################################################
# 欢迎界面
###################################################################

welcome_content = "欢迎使用商品信息管理系统"
login_content = "登陆"
exit_content = "退出"


class WelcomeFrame(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.SetBackgroundColour(wx.Colour(204, 232, 207))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        # 标题栏
        self.MainTitle = wx.StaticText(self, wx.ID_ANY, welcome_content, wx.Point(1000, 1000), wx.Size(1500, 100),
                                       wx.ALIGN_CENTRE)
        self.MainTitle.Wrap(-1)
        self.MainTitle.SetFont(wx.Font(50, 70, 90, 90, False, wx.EmptyString))
        self.MainTitle.SetForegroundColour(wx.Colour(255, 0, 128))
        self.MainTitle.SetBackgroundColour(wx.Colour(146, 215, 252))
        bSizer1.Add(self.MainTitle, 0, wx.ALL, 5)

        self.login_button = wx.Button(self, wx.ID_ANY, login_content, wx.Point(-1, -1), wx.Size(500, 100), 0)
        self.login_button.SetFont(wx.Font(20, 70, 90, 92, False, wx.EmptyString))
        self.login_button.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.login_button.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        bSizer1.Add(self.login_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.exit_button = wx.Button(self, wx.ID_ANY, exit_content, wx.DefaultPosition, wx.Size(500, 100), 0)
        self.exit_button.SetFont(wx.Font(20, 70, 90, 92, False, wx.EmptyString))
        self.exit_button.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.exit_button.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        bSizer1.Add(self.exit_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.set_bgimg)
        self.login_button.Bind(wx.EVT_BUTTON, self.goto_loginframe)
        self.exit_button.Bind(wx.EVT_BUTTON, self.exitapp)

    def __del__(self):
        pass

    def set_bgimg(self, event):
        event.Skip()

    def goto_loginframe(self, event):
        self.Destroy()
        loginFrame = LoginFrame(None)
        loginFrame.Show(True)

    def exitapp(self, event):
        self.Destroy()
