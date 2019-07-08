#############################
# 入库作业
#############################
import wx
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil
import wx.adv as adv

columns = [qtable.CheckBoxColumnDfn(),
           qtable.ColumnDfn(u'产品编码', 'productCode', percent=10, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'产品名称', 'productName', percent=10, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'产品分类', 'productCategoryName', percent=10, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'产品描述', 'productDesc', percent=20, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'备注', 'remark', percent=20, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'录入时间', 'ctime', size=150, type=qtable.TextType(), readonly=True)
           ]
YES_NO = 1
SAVE_NO = 2
PRODUCT_CATEGORY_VALUE = "产品分类"


########################################################################
class InStoreHousePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        swindow = wx.SplitterWindow(parent=self, id=wx.ID_ANY)
        vbox.Add(swindow, 1, flag=wx.EXPAND)

        self.top = wx.Panel(parent=swindow)
        self.bottom = wx.Panel(parent=swindow, style=wx.BORDER)
        # 设置左右布局的分割窗口left和right
        swindow.SplitHorizontally(self.top, self.bottom, 200)
        # 设置最小窗格大小，左右布局指左边窗口大小
        swindow.SetMinimumPaneSize(600)

        self.drawTopPanel()

        # 为bottom面板设置一个布局管理器
        self.drawBottomPanel()

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def drawTopPanel(self):
        # 为top面板设置一个布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 查询栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        orderNo = wx.StaticText(self.top, label=u'入库单号：')
        hbox1.Add(orderNo, flag=wx.RIGHT, border=8)
        self.tc_orderNo = wx.TextCtrl(self.top, size=wx.Size(150, -1))
        hbox1.Add(self.tc_orderNo, flag=wx.RIGHT, border=8)
        orderType = wx.StaticText(self.top, label=u'入库类型：')
        hbox1.Add(orderType, flag=wx.RIGHT, border=8)
        self.choice_orderType = wx.Choice(self.top)
        hbox1.Add(self.choice_orderType, flag=wx.RIGHT, border=8)
        customerName = wx.StaticText(self.top, label=u'供应商：')
        hbox1.Add(customerName, flag=wx.RIGHT, border=8)
        self.choice_customerName = wx.Choice(self.top)
        hbox1.Add(self.choice_customerName, flag=wx.RIGHT, border=8)
        productName = wx.StaticText(self.top, label=u'产品：')
        hbox1.Add(productName, flag=wx.RIGHT, border=8)
        self.choice_productName = wx.Choice(self.top)
        hbox1.Add(self.choice_productName, flag=wx.RIGHT, border=8)
        outdate = wx.StaticText(self.top, label=u'入库日期：')
        hbox1.Add(outdate, flag=wx.RIGHT, border=8)
        self.datectl_start = adv.DatePickerCtrl(self.top,
                                                style=adv.DP_DROPDOWN
                                                      | adv.DP_SHOWCENTURY
                                                      | adv.DP_ALLOWNONE)
        hbox1.Add(self.datectl_start, flag=wx.RIGHT, border=8)
        todate = wx.StaticText(self.top, label=u'~')
        hbox1.Add(todate, flag=wx.RIGHT, border=8)
        self.datectl_end = adv.DatePickerCtrl(self.top,
                                              style=adv.DP_DROPDOWN
                                                    | adv.DP_SHOWCENTURY
                                                    | adv.DP_ALLOWNONE)
        hbox1.Add(self.datectl_end, flag=wx.RIGHT, border=8)
        self.search_button = wx.Button(self.top, wx.ID_ANY, u"搜索", size=(45, 25))
        self.search_button.SetToolTipString(u"根据条件搜索")
        self.search_button.Bind(wx.EVT_BUTTON, self.button_search_click)
        hbox1.Add(self.search_button, flag=wx.RIGHT, border=10)
        self.clear_button = wx.Button(self.top, wx.ID_ANY, u"清空", size=(45, 25))
        self.clear_button.SetToolTipString(u"清空搜索条件")
        self.clear_button.Bind(wx.EVT_BUTTON, self.button_clear_click)
        hbox1.Add(self.clear_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 操作按钮栏
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self.top, wx.ID_ANY, u"添加", size=(70, 25))
        self.add_button.SetToolTipString(u"添加入库单")
        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        hbox2.Add(self.add_button, flag=wx.RIGHT, border=8)
        self.del_button = wx.Button(self.top, wx.ID_ANY, u"撤回", size=(70, 25))
        self.del_button.SetToolTipString(u"撤回入库单")
        self.del_button.Bind(wx.EVT_BUTTON, self.button_del_click)
        hbox2.Add(self.del_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self.top)

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.top.SetSizer(vbox)

    def drawBottomPanel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 画表格
        self.m_grid2 = qtable.QGridTable(self.bottom)

        vbox.Add(self.m_grid2, 1, wx.ALL | wx.EXPAND, 5)

        self.bottom.SetSizer(vbox)

    def button_search_click(self, evt):
        pass

    def button_clear_click(self, evt):
        pass

    def button_add_click(self, evt):
        pass

    def button_del_click(self, evt):
        pass
