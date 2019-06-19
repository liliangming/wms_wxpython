#############################
# 客户维护
#############################

import wx
import math
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil

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

        self.DrawTable()

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def GenQuerySql(self, customerName=None, customerPhone=None, offset=None, pageSize=None):
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

        sql += " order by ctime desc"

        if offset is not None and pageSize is not None:
            sql += " limit " + str(offset) + "," + str(pageSize)

        print(sql)
        return sql

    def button_add_click(self, evt):
        dlg = AddCustomerDialog(None)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            db = sqliteUtil.EasySqlite()
            result = db.execute(self.GenQuerySql(offset=0, pageSize=1))
            self.m_grid1.InsertRows(data=result)
        dlg.Destroy()
        # wx.MessageBox(u'添加客户成功', u'提示', wx.OK | wx.ICON_INFORMATION)

    def button_del_click(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要删除的客户', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要删除勾选的' + str(len(rows)) + '条数据吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        datas = self.m_grid1.GetGridData(rows)
        sql = "delete from customer where customer_id in ("

        for index, data in enumerate(datas):
            id = int(data["customerId"].replace("A", ""))
            sql += " " + str(id)
            if index < len(datas) - 1:
                sql += ","
        sql += ")"

        # 执行删除
        db = sqliteUtil.EasySqlite()
        db.execute(sql)

        # 刷新table
        rows.sort(reverse=True)
        for row in rows:
            self.m_grid1.DeleteRows(pos=row)

    def button_clear_click(self, evt):
        self.customer_name_text.SetValue("")
        self.customer_phone_text.SetValue("")

    def button_search_click(self, evt):
        name = self.customer_name_text.GetValue()
        phone = self.customer_phone_text.GetValue()

        if name.strip() == '':
            name = None
        if phone.strip() == '':
            phone = None

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql(customerName=name, customerPhone=phone))
        self.m_grid1.ReDrawTable(result)

    def DrawTable(self):
        # self.m_grid1.SetRowBackgroundColourChangeEnable(True)
        update_item = qtable.MenuBarItem("查看/修改\tF2", self.update)
        self.m_grid1.AddPopupMenuItem(update_item)
        self.m_grid1.AddHotKey(wx.WXK_F2, self.update)

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql())
        self.m_grid1.DrawTable(qtable.GridData(self.m_grid1, columns, result))

    def update(self, event):
        print("Test1")
        row = self.m_grid1.GetGridCursorRow()
        if row is None:
            wx.MessageBox(u'请先点击要查看/编辑的行', u'错误', wx.OK | wx.ICON_ERROR)
            return

        list = self.m_grid1.GetGridData([row])
        if list:
            dlg = UpdateCustomerDialog(None, list[0])
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                db = sqliteUtil.EasySqlite()
                result = db.execute(self.GenQuerySql(offset=0, pageSize=1))
                self.m_grid1.InsertRows(data=result)
            dlg.Destroy()
        else:
            wx.MessageBox(u'请先点击要查看/编辑的行', u'错误', wx.OK | wx.ICON_ERROR)


class AddCustomerDialog(wx.Dialog):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 500), title="新增客户信息")

        panel = wx.Panel(self)

        topLbl = wx.StaticText(panel, -1, "基本信息")  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        topLb2 = wx.StaticText(panel, -1, "联系人信息")  # 1 创建窗口部件
        topLb2.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

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

        self.add_button = wx.Button(panel, wx.ID_OK, u"添加", size=(70, 25))
        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL, u"取消", size=(70, 25))

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(topLbl, 0, wx.ALL, 5)
        vbox.Add(wx.StaticLine(panel), 0,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        fgs = wx.FlexGridSizer(5, 2, 9, 25)

        fgs.AddMany([(name), (self.tc_name, 1, wx.EXPAND), (addr),
                     (self.tc_addr, 1, wx.EXPAND), (phone), (self.tc_phone, 1, wx.EXPAND),
                     (email), (self.tc_email, 1, wx.EXPAND), (remark),
                     (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(4, 1)
        fgs.AddGrowableCol(1, 1)

        vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

        vbox.Add(topLb2, 0, wx.ALL, 5)
        vbox.Add(wx.StaticLine(panel), 0,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        self.m_grid = qtable.QGridTable(panel)
        vbox.Add(self.m_grid, 1, wx.ALL , 5)
        self.m_grid.DrawTable(qtable.GridData(self.m_grid, columns, []))

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(self.add_button)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(self.cancel_button)
        btnSizer.Add((20, 20), 1)
        vbox.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 15)

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


class UpdateCustomerDialog(wx.Dialog):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, data):
        wx.Dialog.__init__(self, parent, size=(600, 500), title="修改客户信息")

        self.data = data
        panel = wx.Panel(self)

        topLbl = wx.StaticText(panel, -1, "修改客户信息")  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        id = wx.StaticText(panel, label=u'客户编号')
        name = wx.StaticText(panel, label=u'客户名称 *')
        addr = wx.StaticText(panel, label=u'客户地址')
        phone = wx.StaticText(panel, label=u'电话号码')
        email = wx.StaticText(panel, label=u'电子邮箱')
        remark = wx.StaticText(panel, label=u'备 注')

        self.tc_id = wx.TextCtrl(panel, value=self.data["customerId"], style=wx.TE_READONLY)
        self.tc_name = wx.TextCtrl(panel, value=self.data["customerName"])
        self.tc_addr = wx.TextCtrl(panel, value=self.data["customerAddr"], style=wx.TE_MULTILINE)
        self.tc_phone = wx.TextCtrl(panel, value=self.data["phoneNumber"])
        self.tc_email = wx.TextCtrl(panel, value=self.data["email"])
        self.tc_remark = wx.TextCtrl(panel, value=self.data["remark"], style=wx.TE_MULTILINE)

        self.update_button = wx.Button(panel, wx.ID_OK, u"保存", size=(70, 25))
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL, u"取消", size=(70, 25))

        self.update_button.Bind(wx.EVT_BUTTON, self.button_update_click)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(topLbl, 0, wx.ALL, 5)
        vbox.Add(wx.StaticLine(panel), 0,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        fgs = wx.FlexGridSizer(6, 2, 9, 25)

        fgs.AddMany([(id), (self.tc_id, 1, wx.EXPAND), (name), (self.tc_name, 1, wx.EXPAND), (addr),
                     (self.tc_addr, 1, wx.EXPAND), (phone), (self.tc_phone, 1, wx.EXPAND),
                     (email), (self.tc_email, 1, wx.EXPAND), (remark),
                     (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(5, 1)
        fgs.AddGrowableCol(1, 1)

        vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(self.update_button)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(self.cancel_button)
        btnSizer.Add((20, 20), 1)
        vbox.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 15)

        panel.SetSizer(vbox)
        self.Center()

    def button_update_click(self, evt):
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
