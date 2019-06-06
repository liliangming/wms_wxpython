#############################
# 客户维护
#############################

import wx
import util.QTable as qtable
import wx.grid as gridlib


class CustomerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 查询栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.customer_name = wx.StaticText(self, label=u'客户名称：')
        hbox1.Add(self.customer_name, flag=wx.RIGHT, border=8)
        self.customer_name_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.customer_name_text, flag=wx.RIGHT, border=8)
        self.customer_phone = wx.StaticText(self, label=u'电话：')
        hbox1.Add(self.customer_phone, flag=wx.RIGHT, border=8)
        self.customer_phone_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.customer_phone_text, flag=wx.RIGHT, border=8)
        self.search_button = wx.Button(self, wx.ID_ANY, u"搜索", size=(45, 25))
        self.search_button.SetToolTipString(u"根据条件搜索")
        hbox1.Add(self.search_button, flag=wx.RIGHT, border=10)
        self.clear_button = wx.Button(self, wx.ID_ANY, u"清空", size=(45, 25))
        self.clear_button.SetToolTipString(u"清空搜索条件")
        hbox1.Add(self.clear_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 操作按钮栏
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self, wx.ID_ANY, u"添加", size=(70, 25))
        self.add_button.SetToolTipString(u"添加供应商")
        hbox2.Add(self.add_button, flag=wx.RIGHT, border=8)
        self.del_button = wx.Button(self, wx.ID_ANY, u"删除", size=(70, 25))
        self.del_button.SetToolTipString(u"删除供应商")
        hbox2.Add(self.del_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self)
        self.DrawTable()

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        # 翻页按钮
        hbox3 = wx.GridBagSizer(5, 3)
        self.first_button = wx.Button(self, wx.ID_ANY, u"|<<", size=(40, 25))
        self.first_button.SetToolTipString(u"首页")
        hbox3.Add(self.first_button, pos=(0, 1), flag=wx.LEFT, border=10)
        self.second_button = wx.Button(self, wx.ID_ANY, u"<", size=(40, 25))
        self.second_button.SetToolTipString(u"上一页")
        hbox3.Add(self.second_button, pos=(0, 2), flag=wx.LEFT, border=10)
        self.third_button = wx.Button(self, wx.ID_ANY, u">", size=(40, 25))
        self.third_button.SetToolTipString(u"下一页")
        hbox3.Add(self.third_button, pos=(0, 3), flag=wx.LEFT, border=10)
        self.fourth_button = wx.Button(self, wx.ID_ANY, u">>|", size=(40, 25))
        self.fourth_button.SetToolTipString(u"尾页")
        hbox3.Add(self.fourth_button, pos=(0, 4), flag=wx.LEFT | wx.RIGHT, border=10)
        hbox3.AddGrowableCol(0)

        vbox.Add(hbox3, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def DrawTable(self):
        columns = [qtable.CheckBoxColumnDfn(),
                   qtable.ColumnDfn(u'Edi', 'edi', percent=20, type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'Code', 'code', percent=10, type=qtable.TextType()),
                   qtable.ColumnDfn(u'Description', 'description', percent=None, type=qtable.TextType()),
                   qtable.ColumnDfn(u'Quantity', 'quantity', percent=10, type=qtable.NumberType(1, 10000)),
                   qtable.ColumnDfn(u'Unit', 'units', percent=20, type=qtable.ListType([('b.', 0), ('kg', 1), ('mt', 2)])),
                   qtable.ColumnDfn(u'Price', 'price', percent=10, type=qtable.FloatType(6, 2)),
                   qtable.ColumnDfn(u'Total', 'total', percent=10, type=qtable.FloatType(6, 2), readonly=True)
                   ]

        self.m_grid1.SetRowBackgroundColourChangeEnable(True)
        item1 = qtable.MenuBarItem("测试一下", self.Test1)
        item2 = qtable.MenuBarItem("测试一下", self.Test1)
        item1.AddChild(item2)
        item22 = qtable.MenuBarItem("测试一下", self.Test1)
        item2.AddChild(item22)
        item1.AddChild(qtable.SeparatorItem())
        self.m_grid1.AddPopupMenuItem(item1)
        item3 = qtable.MenuBarItem("测试两下", self.Test1)
        self.m_grid1.AddPopupMenuItem(qtable.SeparatorItem())
        self.m_grid1.AddPopupMenuItem(item3)
        self.m_grid1.AddHotKey(wx.WXK_F2, self.Test1)
        gridData = qtable.GridData(self.m_grid1, columns,
                                   [{"selected": "1", "edi": "11111111", "code": "12",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18", "rt": "dsds"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"},
                                    {"selected": "0", "edi": "123344", "code": "你是个小逗比你是个小逗比你是个小逗比你是个小逗比",
                                     "description": "13", "quantity": "14", "units": "15", "price": "16",
                                     "total": "18"}])
        self.m_grid1.DrawTable(gridData)

    def Test1(self, event):
        print("Test1")
