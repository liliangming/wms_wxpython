import wx


class ChatFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)  # 设置对话框的大小
        self.Center()  # 设置弹窗在屏幕中间

        # 使用尺寸器改写,改写后拉大或者缩小窗口，中间的控件会随着窗口的大小已固定的尺寸而改变
        panel = wx.Panel(self)  # self表示实例即ChatFrame，创建一个面板
        # 定义panel中的元件
        self.receiveLabel = wx.StaticText(panel, label="Receive Msg")
        self.sendLabel = wx.StaticText(panel, label="Send Msg")
        self.noticeLabel = wx.StaticText(panel, label="Notice")
        self.chatFrame1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT)
        self.chatFrame2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RIGHT)
        self.noticeFrame = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(panel, value='input message')  # 设置发送消息的文本输入框的位置和尺寸
        self.toUser = wx.TextCtrl(panel, value='input username')  # 设置指定用户的文本输入框的位置和尺寸
        self.sendButton = wx.Button(panel, label="Send")
        self.sendDesignButton = wx.Button(panel, label="SendDesign")
        self.closeButton = wx.Button(panel, label="Close")
        self.usersButton = wx.Button(panel, label="Online")

        print(panel.GetBackgroundColour())

        self.box1 = wx.BoxSizer()  # 定义横向的box1
        self.box1.Add(self.receiveLabel, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)  # 该元素占box1的比例为40%，方式为伸缩，边界为5
        self.box1.Add(self.sendLabel, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box1.Add(self.noticeLabel, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        self.box2 = wx.BoxSizer()  # 定义横向的box2
        self.box2.Add(self.chatFrame1, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box2.Add(self.chatFrame2, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box2.Add(self.noticeFrame, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        self.box3 = wx.BoxSizer()  # 定义横向的box3
        self.box3.Add(self.message, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)
        self.box3.Add(self.sendButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.box3.Add(self.usersButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        self.box4 = wx.BoxSizer()  # 定义横向的box3
        self.box4.Add(self.toUser, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)
        self.box4.Add(self.sendDesignButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.box4.Add(self.closeButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        self.v_box = wx.BoxSizer(wx.VERTICAL)  # 定义一个纵向的v_box
        self.v_box.Add(self.box1, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box1，比例为1
        self.v_box.Add(self.box2, proportion=7, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box2，比例为7
        self.v_box.Add(self.box3, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box3，比例为1
        self.v_box.Add(self.box4, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box4，比例为1

        panel.SetSizer(self.v_box)
        self.Show()


if __name__ == '__main__':
    app = wx.App()  # 实例化一个主循环
    ChatFrame(None, -1, title="ShiYanLou Chat Client", size=(780, 500))
    app.MainLoop()