#############################
# 供应商维护
#############################

import wx
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil

columns = [qtable.CheckBoxColumnDfn(),
           qtable.ColumnDfn(u'编号', 'supplierId', size=60, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'名称', 'supplierName', percent=10, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'地址', 'supplierAddr', percent=20, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'电话', 'phoneNumber', percent=10, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'邮箱', 'email', percent=10,
                            type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'备注', 'remark', percent=20, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'录入时间', 'ctime', size=150, type=qtable.TextType(), readonly=True)
           ]
YES_NO = 1
SAVE_NO = 2


class SupplierPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 查询栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.supplier_name = wx.StaticText(self, label=u'供应商名称：')
        hbox1.Add(self.supplier_name, flag=wx.RIGHT, border=8)
        self.supplier_name_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.supplier_name_text, flag=wx.RIGHT, border=8)
        self.supplier_phone = wx.StaticText(self, label=u'电话：')
        hbox1.Add(self.supplier_phone, flag=wx.RIGHT, border=8)
        self.supplier_phone_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.supplier_phone_text, flag=wx.RIGHT, border=8)
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

        # 失效选择栏
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBox_status = wx.CheckBox(self, -1, u'显示失效客户', pos=(10, 10))
        self.checkBox_status.Bind(wx.EVT_CHECKBOX, self.checkBox_status_change)
        hbox3.Add(self.checkBox_status, flag=wx.RIGHT, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self)

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.DrawTable()

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def GenQuerySql(self, supplierId=None, supplierName=None, supplierPhone=None, offset=None, pageSize=None):
        sql = "select " \
              "0 as selected, " \
              "substr('S00000',0,7-length(supplier_id))||supplier_id as supplierId, " \
              "supplier_name as supplierName, " \
              "supplier_addr as supplierAddr, " \
              "phone_number as phoneNumber, " \
              "email, " \
              "remark, " \
              "status, " \
              "ctime, " \
              "cby, " \
              "utime, " \
              "uby " \
              "from supplier where 1 = 1"
        if supplierId is not None:
            sql += " and supplier_id = " + str(supplierId)

        if supplierName is not None:
            sql += " and supplier_name like \'%%" + supplierName + "%%\'"

        if supplierPhone is not None:
            sql += " and phone_number = '" + supplierPhone + "'"

        if self.checkBox_status.GetValue():
            sql += " and status in (0,1)"
        else:
            sql += " and status = 1"

        sql += " order by ctime desc"

        if offset is not None and pageSize is not None:
            sql += " limit " + str(offset) + "," + str(pageSize)

        print(sql)
        return sql

    def checkBox_status_change(self, evt):
        self.button_search_click(evt)

    def button_add_click(self, evt):
        dlg = SupplierDialog(None, title="新增供应商信息")
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            db = sqliteUtil.EasySqlite()
            result = db.execute(self.GenQuerySql(offset=0, pageSize=1))
            self.m_grid1.InsertRows(data=result)
        dlg.Destroy()

    def button_del_click(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要删除的供应商', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要删除勾选的' + str(len(rows)) + '条数据吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        datas = self.m_grid1.GetGridData(rows=rows)
        sql = "delete from supplier where supplier_id in ("

        for index, data in enumerate(datas):
            id = int(data["supplierId"].replace("S", ""))
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
        self.supplier_name_text.SetValue("")
        self.supplier_phone_text.SetValue("")

    def button_search_click(self, evt):
        name = self.supplier_name_text.GetValue()
        phone = self.supplier_phone_text.GetValue()

        if name.strip() == '':
            name = None
        if phone.strip() == '':
            phone = None

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql(supplierName=name, supplierPhone=phone))
        self.m_grid1.ReDrawTable(result)

    def DrawTable(self):
        # self.m_grid1.SetRowBackgroundColourChangeEnable(True)
        item1 = qtable.MenuBarItem("查看/修改\tF2", self.update)
        self.m_grid1.AddPopupMenuItem(item1)
        item2 = qtable.MenuBarItem("设置", None)
        item2.AddChild(qtable.MenuBarItem("有效", self.valid_status))
        item2.AddChild(qtable.MenuBarItem("失效", self.invalid_status))
        self.m_grid1.AddPopupMenuItem(item2)

        self.m_grid1.AddHotKey(wx.WXK_F2, self.update)

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql())
        self.m_grid1.DrawTable(qtable.GridData(self.m_grid1, columns, result))

    def update(self, event):
        row = self.m_grid1.GetGridCursorRow()
        if row is None:
            wx.MessageBox(u'请先点击要查看/编辑的行', u'错误', wx.OK | wx.ICON_ERROR)
            return

        list = self.m_grid1.GetGridData(rows=[row])
        if list:
            data = list[0]
            dlg = SupplierDialog(None, "查看/修改供应商信息", data=data, style=SAVE_NO)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                id = int(data["supplierId"].replace("S", ""))
                db = sqliteUtil.EasySqlite()
                result = db.execute(self.GenQuerySql(supplierId=id))
                # 更新表格数据
                if result:
                    self.m_grid1.RefreshRows([row], data=result)
            dlg.Destroy()
        else:
            wx.MessageBox(u'请先点击要查看/编辑的行', u'错误', wx.OK | wx.ICON_ERROR)

    # 失效状态
    def invalid_status(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要失效的供应商', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要失效勾选的' + str(len(rows)) + '条供应商吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 0)

    def valid_status(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要有效的供应商', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要有效勾选的' + str(len(rows)) + '条供应商吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 1)

    def set_status(self, rows, status):
        datas = self.m_grid1.GetGridData(rows=rows)

        sql = "update supplier set status = ? where supplier_id in ("
        for index, data in enumerate(datas):
            data["status"] = status

            sql += " " + str(int(data["supplierId"].replace("S", "")))
            if index < len(datas) - 1:
                sql += ","

        sql += ")"

        # 执行状态变更
        db = sqliteUtil.EasySqlite()
        db.execute(sql, [status])

        # 刷新table
        if not self.checkBox_status.GetValue() and not status:
            rows.sort(reverse=True)
            for row in rows:
                self.m_grid1.DeleteRows(row)
        else:
            self.m_grid1.RefreshRows(rows, datas)


class SupplierDialog(wx.Dialog):
    def __init__(self, parent, title, data=None, style=YES_NO):
        wx.Dialog.__init__(self, parent, size=(600, 500), title=title)
        panel = wx.Panel(self)

        nb = wx.Notebook(panel)

        self.page1 = BaseInfoPage(nb, data)
        self.page2 = LiaisonPage(nb, data)
        self.page3 = PageThree(nb, data)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.page1, "基本信息")
        nb.AddPage(self.page2, "联系人")
        nb.AddPage(self.page3, "收货地址")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND)

        if style == YES_NO:
            self.add_button = wx.Button(panel, wx.ID_OK, u"添加", size=(70, 25))
            self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
            self.cancel_button = wx.Button(panel, wx.ID_CANCEL, u"取消", size=(70, 25))

            btnSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer.Add((20, 20), 1)
            btnSizer.Add(self.add_button)
            btnSizer.Add((20, 20), 1)
            btnSizer.Add(self.cancel_button)
            btnSizer.Add((20, 20), 1)
            sizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.TOP, 15)
        else:
            self.save_button = wx.Button(panel, wx.ID_OK, u"保存", size=(70, 25))
            self.save_button.Bind(wx.EVT_BUTTON, self.button_update_click)
            self.cancel_button = wx.Button(panel, wx.ID_CANCEL, u"取消", size=(70, 25))

            btnSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer.Add((20, 20), 1)
            btnSizer.Add(self.save_button)
            btnSizer.Add((20, 20), 1)
            btnSizer.Add(self.cancel_button)
            btnSizer.Add((20, 20), 1)
            sizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.TOP, 15)

        panel.SetSizer(sizer)
        self.Center()

    def button_add_click(self, evt):
        name = self.page1.tc_name.GetValue()
        if name.strip() == '':
            wx.MessageBox(u'请输入供应商名称', u'错误', wx.OK | wx.ICON_ERROR)
            return
        addr = self.page1.tc_addr.GetValue()
        phone = self.page1.tc_phone.GetValue()
        email = self.page1.tc_email.GetValue()
        remark = self.page1.tc_remark.GetValue()
        db = sqliteUtil.EasySqlite()
        db.execute(
            "insert into supplier(supplier_name, supplier_addr, phone_number, email, remark, ctime, cby, utime, uby) values('" + name + "','" + addr + "','" + phone + "','" + email + "','" + remark + "',datetime('now'),'',datetime('now'),'')")
        self.EndModal(wx.ID_OK)

    def button_update_click(self, evt):
        name = self.page1.tc_name.GetValue()
        if name.strip() == '':
            wx.MessageBox(u'请输入供应商名称', u'错误', wx.OK | wx.ICON_ERROR)
            return
        id = int(self.page1.tc_id.GetValue().replace("S", ""))
        addr = self.page1.tc_addr.GetValue()
        phone = self.page1.tc_phone.GetValue()
        email = self.page1.tc_email.GetValue()
        remark = self.page1.tc_remark.GetValue()

        db = sqliteUtil.EasySqlite()
        db.execute(
            "update supplier set supplier_name = ?, supplier_addr = ?, phone_number = ?, email = ?, remark = ?, utime = datetime('now') where supplier_id = ?",
            [name, addr, phone, email, remark, id])
        self.EndModal(wx.ID_OK)


class BaseInfoPage(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        self.data = data

        vbox = wx.BoxSizer(wx.VERTICAL)

        if self.data:
            id = wx.StaticText(self, label=u'供应商编号')
            name = wx.StaticText(self, label=u'供应商名称 *')
            addr = wx.StaticText(self, label=u'供应商地址')
            phone = wx.StaticText(self, label=u'电话号码')
            email = wx.StaticText(self, label=u'电子邮箱')
            remark = wx.StaticText(self, label=u'备 注')

            self.tc_id = wx.TextCtrl(self, value=self.data["supplierId"], style=wx.TE_READONLY)
            self.tc_name = wx.TextCtrl(self, value=self.data["supplierName"])
            self.tc_addr = wx.TextCtrl(self, value=self.data["supplierAddr"], style=wx.TE_MULTILINE)
            self.tc_phone = wx.TextCtrl(self, value=self.data["phoneNumber"])
            self.tc_email = wx.TextCtrl(self, value=self.data["email"])
            self.tc_remark = wx.TextCtrl(self, value=self.data["remark"], style=wx.TE_MULTILINE)

            fgs = wx.FlexGridSizer(6, 2, 9, 25)
            fgs.AddMany([(id), (self.tc_id, 1, wx.EXPAND), (name), (self.tc_name, 1, wx.EXPAND), (addr),
                         (self.tc_addr, 1, wx.EXPAND), (phone), (self.tc_phone, 1, wx.EXPAND),
                         (email), (self.tc_email, 1, wx.EXPAND), (remark),
                         (self.tc_remark, 1, wx.EXPAND)])

            fgs.AddGrowableRow(5, 1)
            fgs.AddGrowableCol(1, 1)

            vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        else:
            name = wx.StaticText(self, label=u'供应商名称 *')
            addr = wx.StaticText(self, label=u'供应商地址')
            phone = wx.StaticText(self, label=u'电话号码')
            email = wx.StaticText(self, label=u'电子邮箱')
            remark = wx.StaticText(self, label=u'备 注')

            self.tc_name = wx.TextCtrl(self)
            self.tc_addr = wx.TextCtrl(self, style=wx.TE_MULTILINE)
            self.tc_phone = wx.TextCtrl(self)
            self.tc_email = wx.TextCtrl(self)
            self.tc_remark = wx.TextCtrl(self, style=wx.TE_MULTILINE)

            fgs = wx.FlexGridSizer(5, 2, 9, 25)

            fgs.AddMany([(name), (self.tc_name, 1, wx.EXPAND), (addr),
                         (self.tc_addr, 1, wx.EXPAND), (phone), (self.tc_phone, 1, wx.EXPAND),
                         (email), (self.tc_email, 1, wx.EXPAND), (remark),
                         (self.tc_remark, 1, wx.EXPAND)])

            fgs.AddGrowableRow(4, 1)
            fgs.AddGrowableCol(1, 1)

            vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

        self.SetSizer(vbox)


class LiaisonPage(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        self.data = data
        t = wx.StaticText(self, -1, "待建设", (40, 40))


class PageThree(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)
        self.data = data
        t = wx.StaticText(self, -1, "待建设", (60, 60))
