# coding=utf-8
import wx


class Myframe(wx.Frame):
    def __init__(self, flag=True):
        wx.Frame.__init__(self, None)
        self.first = 0
        self.flag = flag
        self.sp = wx.SplitterWindow(self)  # 创建一个分割窗,parent是frame
        self.p1 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)  # 创建子面板p1
        self.p2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)  # 创建子面板p2
        self.p1.Hide()  # 确保备用的子面板被隐藏
        self.p2.Hide()
        self.sp1 = wx.SplitterWindow(self.p1)  # 创建一个子分割窗，parent是p1
        self.box = wx.BoxSizer(wx.VERTICAL)  # 创建一个垂直布局
        self.box.Add(self.sp1, 1, wx.EXPAND)  # 将子分割窗布局延伸至整个p1空间
        self.p1.SetSizer(self.box)
        self.p2.SetBackgroundColour("blue")
        self.p1_1 = wx.Panel(self.sp1, style=wx.SUNKEN_BORDER)  # 在子分割窗self.sp1的基础上创建子画板p1_1
        self.p1_2 = wx.Panel(self.sp1, style=wx.SUNKEN_BORDER)  # 在子分割窗self.sp1的基础上创建子画板p1_2
        self.p1_1.Hide()
        self.p1_2.Hide()
        self.p1_1.SetBackgroundColour("red")
        self.p1_2.SetBackgroundColour("yellow")
        self.sp.SplitHorizontally(self.p1, self.p2, 0)
        self.sp1.SplitVertically(self.p1_1, self.p1_2, 0)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnEraseBack(self, event):
        if self.first < 2 or self.flag:
            self.sp.SetSashPosition(100)
            self.sp1.SetSashPosition(-100)
            self.first = self.first + 1

        self.Refresh()


app = wx.PySimpleApp()
frame = Myframe(True)
frame.Show(True)
app.MainLoop()
