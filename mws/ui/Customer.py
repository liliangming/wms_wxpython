#############################
# 客户维护
#############################

import wx
import math
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil


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
        self.search_button.Bind(wx.EVT_BUTTON, self.button_search_click)
        hbox1.Add(self.search_button, flag=wx.RIGHT, border=10)
        self.clear_button = wx.Button(self, wx.ID_ANY, u"清空", size=(45, 25))
        self.clear_button.SetToolTipString(u"清空搜索条件")
        self.clear_button.Bind(wx.EVT_BUTTON, self.button_clear_click)
        hbox1.Add(self.clear_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 操作按钮栏
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self, wx.ID_ANY, u"添加", size=(70, 25))
        self.add_button.SetToolTipString(u"添加供应商")
        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        hbox2.Add(self.add_button, flag=wx.RIGHT, border=8)
        self.del_button = wx.Button(self, wx.ID_ANY, u"删除", size=(70, 25))
        self.del_button.SetToolTipString(u"删除供应商")
        self.del_button.Bind(wx.EVT_BUTTON, self.button_del_click)
        hbox2.Add(self.del_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self)

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        # 翻页栏
        hbox3 = wx.GridBagSizer(5, 3)
        page_text1 = wx.StaticText(self, label=u'共')
        hbox3.Add(page_text1, pos=(0, 1), flag=wx.LEFT, border=10)
        self.total_record = wx.TextCtrl(self, value="0", size=wx.Size(45, -1), style=wx.TE_READONLY)
        hbox3.Add(self.total_record, pos=(0, 2), flag=wx.LEFT, border=10)
        page_text2 = wx.StaticText(self, label=u'条 | 每页')
        hbox3.Add(page_text2, pos=(0, 3), flag=wx.LEFT, border=10)
        self.page_size = wx.Choice(self, choices=["20", "50", "100", "200"], size=(45, 25))
        self.page_size.SetSelection(0)
        self.page_size.Bind(wx.EVT_CHOICE, self.choice_page_size)
        hbox3.Add(self.page_size, pos=(0, 4), flag=wx.LEFT, border=10)
        page_text3 = wx.StaticText(self, label=u'条 | 共')
        hbox3.Add(page_text3, pos=(0, 5), flag=wx.LEFT, border=10)
        self.total_page = wx.TextCtrl(self, value="0", size=wx.Size(45, -1), style=wx.TE_READONLY)
        hbox3.Add(self.total_page, pos=(0, 6), flag=wx.LEFT, border=10)
        page_text4 = wx.StaticText(self, label=u'页 | 第')
        hbox3.Add(page_text4, pos=(0, 7), flag=wx.LEFT, border=10)
        self.cur_page = wx.Choice(self, choices=["1"], size=(-1, 25))
        self.cur_page.SetSelection(0)
        self.cur_page.Bind(wx.EVT_CHOICE, self.choice_cur_page)
        hbox3.Add(self.cur_page, pos=(0, 8), flag=wx.LEFT, border=10)
        page_text5 = wx.StaticText(self, label=u'页 | ')
        hbox3.Add(page_text5, pos=(0, 9), flag=wx.LEFT, border=10)

        self.first_button = wx.Button(self, wx.ID_ANY, u"|<<", size=(40, 25))
        self.first_button.SetToolTipString(u"首页")
        self.first_button.Bind(wx.EVT_BUTTON, self.button_first_click)
        hbox3.Add(self.first_button, pos=(0, 10), flag=wx.LEFT, border=10)
        self.second_button = wx.Button(self, wx.ID_ANY, u"<", size=(40, 25))
        self.second_button.SetToolTipString(u"上一页")
        self.second_button.Bind(wx.EVT_BUTTON, self.button_second_click)
        hbox3.Add(self.second_button, pos=(0, 11), flag=wx.LEFT, border=10)
        self.third_button = wx.Button(self, wx.ID_ANY, u">", size=(40, 25))
        self.third_button.SetToolTipString(u"下一页")
        self.third_button.Bind(wx.EVT_BUTTON, self.button_third_click)
        hbox3.Add(self.third_button, pos=(0, 12), flag=wx.LEFT, border=10)
        self.fourth_button = wx.Button(self, wx.ID_ANY, u">>|", size=(40, 25))
        self.fourth_button.SetToolTipString(u"尾页")
        self.fourth_button.Bind(wx.EVT_BUTTON, self.button_fourth_click)
        hbox3.Add(self.fourth_button, pos=(0, 13), flag=wx.LEFT | wx.RIGHT, border=10)

        hbox3.AddGrowableCol(0)

        vbox.Add(hbox3, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.PageBarChange()
        self.DrawTable()

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def GenCountSql(self, customerName=None, customerPhone=None):
        sql = "select count(*) as total from customer where 1 = 1"
        if customerName is not None:
            sql += " and customer_name like \'%" + customerName + "%\'"

        if customerPhone is not None:
            sql += " and phone_number = '" + customerPhone + "'"

        print(sql)
        return sql

    def GenQuerySql(self, curPage=None, customerName=None, customerPhone=None):
        sql = "select " \
              "0 as selected, " \
              "substr('A00000',0,7-length(customer_id))||customer_id as customerId, " \
              "customer_name as customerName, " \
              "customer_addr as customerAddr, " \
              "phone_number as phoneNumber, " \
              "email, remark, " \
              "ctime, " \
              "cby, " \
              "utime, " \
              "uby " \
              "from customer where 1 = 1"
        if customerName is not None:
            sql += " and customer_name like \'%%" + customerName + "%%\'"

        if customerPhone is not None:
            sql += " and phone_number = '" + customerPhone + "'"

        print(sql)
        return sql

    def PageBarChange(self, curPage=None, customerName=None, customerPhone=None):
        pageSize = self.page_size.GetStringSelection()
        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenCountSql(customerName, customerPhone))
        total = result[0]["total"]
        pageTotal = 0
        if total > 0:
            pageTotal = math.ceil(total / int(pageSize))

            c = []
            for i in range(pageTotal):
                c.append(str(i + 1))
            self.cur_page.SetItems(c)
            if curPage is None:
                curPage = c[0]

        self.total_record.SetValue(str(total))
        self.total_page.SetValue(str(pageTotal))
        self.cur_page.SetStringSelection(str(curPage))

        # 当前页是第一页，灰化前一页和首页按钮
        if curPage is None or int(curPage) <= 1:
            self.first_button.Enable(False)
            self.second_button.Enable(False)
        else:
            self.first_button.Enable(True)
            self.second_button.Enable(True)

        # 当前页是最后一页，灰化后一页和尾页按钮
        if curPage is None or int(curPage) >= int(pageTotal):
            self.third_button.Enable(False)
            self.fourth_button.Enable(False)
        else:
            self.third_button.Enable(True)
            self.fourth_button.Enable(True)

    def choice_page_size(self, evt):
        print("choice_page_size")
        self.PageBarChange()

    def choice_cur_page(self, evt):
        print("choice_cur_page")
        self.PageBarChange(evt.GetString())

    def button_add_click(self, evt):
        print("button_add_click")
        dlg = AddCustomerDialog(None)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            self.DrawTable()
        dlg.Destroy()

    def button_del_click(self, evt):
        print("button_del_click")
        pass

    def button_clear_click(self, evt):
        print("button_clear_click")
        pass

    def button_search_click(self, evt):
        print("button_search_click")
        pass

    def button_first_click(self, evt):
        print("button_first_click")
        pass

    def button_second_click(self, evt):
        print("button_second_click")
        pass

    def button_third_click(self, evt):
        print("button_third_click")
        pass

    def button_fourth_click(self, evt):
        print("button_fourth_click")
        pass

    def DrawTable(self):
        columns = [qtable.CheckBoxColumnDfn(),
                   qtable.ColumnDfn(u'编号', 'customerId', percent=20, type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'名称', 'customerName', percent=10, type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'地址', 'customerAddr', percent=None, type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'电话', 'phoneNumber', percent=10, type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'邮箱', 'email', percent=20,
                                    type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'备注', 'remark', percent=10, type=qtable.TextType(), readonly=True),
                   qtable.ColumnDfn(u'录入时间', 'ctime', percent=10, type=qtable.TextType(), readonly=True)
                   ]

        self.m_grid1.SetRowBackgroundColourChangeEnable(True)
        # item1 = qtable.MenuBarItem("测试一下", self.Test1)
        # item2 = qtable.MenuBarItem("测试一下", self.Test1)
        # item1.AddChild(item2)
        # item22 = qtable.MenuBarItem("测试一下", self.Test1)
        # item2.AddChild(item22)
        # item1.AddChild(qtable.SeparatorItem())
        # self.m_grid1.AddPopupMenuItem(item1)
        # item3 = qtable.MenuBarItem("测试两下", self.Test1)
        # self.m_grid1.AddPopupMenuItem(qtable.SeparatorItem())
        # self.m_grid1.AddPopupMenuItem(item3)
        # self.m_grid1.AddHotKey(wx.WXK_F2, self.Test1)

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql())
        self.m_grid1.DrawTable(qtable.GridData(self.m_grid1, columns, result))

    def Test1(self, event):
        print("Test1")


class AddCustomerDialog(wx.Dialog):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 500), title="新增客户")

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(5, 2, 9, 25)

        name = wx.StaticText(panel, label=u'客户名称 *')
        addr = wx.StaticText(panel, label=u'客户地址')
        phone = wx.StaticText(panel, label=u'电话号码')
        email = wx.StaticText(panel, label=u'电子邮箱')
        remark = wx.StaticText(panel, label=u'备 注')

        self.tc_name = wx.TextCtrl(panel)
        self.tc_addr = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.tc_phone = wx.TextCtrl(panel)
        self.tc_email = wx.TextCtrl(panel)
        self.tc_remark = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fgs.AddMany([(name), (self.tc_name, 1, wx.EXPAND), (addr),
                     (self.tc_addr, 1, wx.EXPAND), (phone), (self.tc_phone, 1, wx.EXPAND),
                     (email), (self.tc_email, 1, wx.EXPAND), (remark),
                     (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(4, 1)
        fgs.AddGrowableCol(1, 1)

        vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

        gSizer = wx.GridBagSizer(5, 3)

        self.add_button = wx.Button(panel, wx.ID_OK, u"添加", size=(70, 25))
        gSizer.Add(self.add_button, pos=(1, 1), flag=wx.LEFT | wx.RIGHT, border=10)
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL, u"取消", size=(70, 25))
        gSizer.Add(self.cancel_button, pos=(1, 2), flag=wx.LEFT | wx.RIGHT, border=10)

        gSizer.AddGrowableCol(0)

        vbox.Add(gSizer, flag=wx.EXPAND | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=30)

        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        # self.cancel_button.Bind(wx.EVT_BUTTON, self.button_cancel_click)

        panel.SetSizer(vbox)
        self.Center()

    def button_add_click(self, evt):
        name = self.tc_name.GetValue()
        if name.strip() == '':
            wx.MessageBox(u'请输入客户名称', u'错误', wx.OK | wx.ICON_ERROR)
            return
        addr = self.tc_addr.GetValue()
        phone = self.tc_phone.GetValue()
        email = self.tc_email.GetValue()
        remark = self.tc_remark.GetValue()
        db = sqliteUtil.EasySqlite()
        db.execute(
            "insert into customer(customer_name, customer_addr, phone_number, email, remark, ctime, cby, utime, uby) values('" + name + "','" + addr + "','" + phone + "','" + email + "','" + remark + "',datetime('now'),'',datetime('now'),'')")
        self.EndModal(wx.ID_OK)

    # def button_cancel_click(self, evt):
    #     self.Destroy()
