import wx


# 自定义窗口类MyFrame
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Tree", size=(500, 400))
        self.Center()
        swindow = wx.SplitterWindow(parent=self, id=-1)
        left = wx.Panel(parent=swindow)
        right = wx.Panel(parent=swindow)
        # 设置左右布局的分割窗口left和right
        swindow.SplitVertically(left, right, 200)
        # 设置最小窗格大小，左右布局指左边窗口大小
        swindow.SetMinimumPaneSize(80)
        # 创建一棵树

        self.tree = self.createTreeCtrl(left)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.on_click, self.tree)
        # 为left面板设置一个布局管理器
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        left.SetSizer(vbox1)
        vbox1.Add(self.tree, 1, flag=wx.EXPAND | wx.ALL, border=5)
        # 为right面板设置一个布局管理器
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        right.SetSizer((vbox2))
        self.st = wx.StaticText(right, 2, label='右侧面板')
        vbox2.Add(self.st, 1, flag=wx.EXPAND | wx.ALL, border=5)

    def on_click(self, event):
        item = event.GetItem()
        self.st.SetLabel(self.tree.GetItemText(item))

    def createTreeCtrl(self, parent):
        tree = wx.TreeCtrl(parent)
        # 通过wx.ImageList()创建一个图像列表imglist并保存在树中
        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        tree.AssignImageList(imglist)
        # 创建根节点和5个子节点并展开
        root = tree.AddRoot('TreeRoot', image=0)
        item1 = tree.AppendItem(root, 'Item1', 0)
        item2 = tree.AppendItem(root, 'Item2', 0)
        item3 = tree.AppendItem(root, 'Item3', 0)
        item4 = tree.AppendItem(root, 'Item4', 0)
        item5 = tree.AppendItem(root, 'Item5', 0)
        tree.Expand(root)
        tree.SelectItem(root)

        # 给item1节点添加5个子节点并展开
        tree.AppendItem(item1, 'file 1', 1)
        tree.AppendItem(item1, 'file 2', 1)
        tree.AppendItem(item1, 'file 3', 1)
        tree.AppendItem(item1, 'file 4', 1)
        tree.AppendItem(item1, 'file 5', 1)
        tree.Expand(item1)

        # 给item2节点添加5个子节点并展开
        tree.AppendItem(item2, 'file 1', 1)
        tree.AppendItem(item2, 'file 2', 1)
        tree.AppendItem(item2, 'file 3', 1)
        tree.AppendItem(item2, 'file 4', 1)
        tree.AppendItem(item2, 'file 5', 1)
        tree.Expand(item2)

        # 返回树对象
        return tree


class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame = MyFrame()
        frame.Show()
        return True

    def OnExit(self):
        print("应用程序退出")
        return 0


if __name__ == '__main__':
    app = App()
    app.MainLoop()