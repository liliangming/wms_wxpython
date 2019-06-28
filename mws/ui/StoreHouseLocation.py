#############################
# 库位维护
#############################

import wx
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil

columns = [qtable.CheckBoxColumnDfn(),
           qtable.ColumnDfn(u'仓库', 'shAlias', percent=20, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'库位编号', 'slId', percent=15, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'库位名称', 'slName', percent=15, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'备注', 'remark', percent=40, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'录入时间', 'ctime', size=150, type=qtable.TextType(), readonly=True)
           ]
YES_NO = 1
SAVE_NO = 2


def GetSHDict():
    dic = {}
    db = sqliteUtil.EasySqlite()
    result = db.execute(
        " select t1.sh_id as key, t1.sh_id || '-' || (case when t1.status = 1 then t1.sh_name else t1.sh_name || '(失效)' end) as value "
        " from storehouse t1 "
        " order by t1.ctime desc")
    for e in result:
        dic[e["key"]] = e["value"]

    return dic


def GetDicTypeByName(dict, name):
    for dicType in dict.items():
        if dicType[1] == name:
            return dicType[0]

    return None


def GetDicTypeNameByType(dict, type):
    for dicType in dict.items():
        if dicType[0] == type:
            return dicType[1]

    return None


def GetDicTypeChoice(dict, blank=True):
    list = []
    if blank:
        list.append("")

    for dicType in dict.items():
        list.append(dicType[1])

    return list


def IsSLExist(slId):
    db = sqliteUtil.EasySqlite()
    result = db.execute(
        "select 1 from storehouse_location where sh_id = ?",
        [slId])
    return result


class StoreHouseLocationPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sh_dict = GetSHDict()

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 查询栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sh_name = wx.StaticText(self, label=u'仓库：')
        hbox1.Add(self.sh_name, flag=wx.RIGHT, border=8)
        self.sh_name_choice = wx.Choice(self)
        hbox1.Add(self.sh_name_choice, flag=wx.RIGHT, border=8)
        self.sl_id = wx.StaticText(self, label=u'库位编号：')
        hbox1.Add(self.sl_id, flag=wx.RIGHT, border=8)
        self.sl_id_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.sl_id_text, flag=wx.RIGHT, border=8)
        self.sl_name = wx.StaticText(self, label=u'库位名称：')
        hbox1.Add(self.sl_name, flag=wx.RIGHT, border=8)
        self.sl_name_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.sl_name_text, flag=wx.RIGHT, border=8)
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
        self.add_button.SetToolTipString(u"添加库位")
        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        hbox2.Add(self.add_button, flag=wx.RIGHT, border=8)
        self.del_button = wx.Button(self, wx.ID_ANY, u"删除", size=(70, 25))
        self.del_button.SetToolTipString(u"删除库位")
        self.del_button.Bind(wx.EVT_BUTTON, self.button_del_click)
        hbox2.Add(self.del_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 失效选择栏
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBox_status = wx.CheckBox(self, -1, u'显示失效库位', pos=(10, 10))
        self.checkBox_status.Bind(wx.EVT_CHECKBOX, self.checkBox_status_change)
        hbox3.Add(self.checkBox_status, flag=wx.RIGHT, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self)

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.sh_name_choice.SetItems(GetDicTypeChoice(self.sh_dict))
        self.sh_name_choice.SetStringSelection("")
        self.DrawTable()

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def GenQuerySql(self, slId=None, slName=None, shId=None, offset=None, pageSize=None):
        sql = "select " \
              "0 as selected, " \
              "sh_id as shId, " \
              "sl_id as slId, " \
              "sl_name as slName, " \
              "remark, " \
              "status, " \
              "ctime, " \
              "cby, " \
              "utime, " \
              "uby " \
              "from storehouse_location where 1 = 1"
        if slId is not None:
            sql += " and sl_id = '" + str(slId) + "'"

        if slName is not None:
            sql += " and sl_name like \'%%" + slName + "%%\'"

        if shId is not None:
            sql += " and sh_id = '" + str(shId) + "'"

        if self.checkBox_status.GetValue():
            sql += " and status in (0,1)"
        else:
            sql += " and status = 1"

        sql += " order by ctime desc"

        if offset is not None and pageSize is not None:
            sql += " limit " + str(offset) + "," + str(pageSize)

        sql = "select t1.*, t2.sh_name as shName, t1.shId || '-' || (case when t2.status = 1 then ifnull(t2.sh_name,'UNKNOW') else ifnull(t2.sh_name,'UNKNOW') || '(失效)' end) as shAlias from (" + sql + ") t1 left join storehouse t2 on t2.sh_id = t1.shId"

        print(sql)
        return sql

    def checkBox_status_change(self, evt):
        self.button_search_click(evt)

    def button_add_click(self, evt):
        dlg = StoreHouseLocationDialog(None, title="新增库位信息")
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
            wx.MessageBox(u'请勾选要删除的库位', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要删除勾选的' + str(len(rows)) + '条数据吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        datas = self.m_grid1.GetGridData(rows=rows)
        sql = "delete from storehouse_location where sl_id in ("

        for index, data in enumerate(datas):
            sql += " '" + data["slId"] + "'"
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
        self.sh_name_choice.SetStringSelection("")
        self.sl_id_text.SetValue("")
        self.sl_name_text.SetValue("")

    def button_search_click(self, evt):
        shId = GetDicTypeByName(self.sh_dict, self.sh_name_choice.GetStringSelection())
        slId = self.sl_id_text.GetValue()
        slName = self.sl_name_text.GetValue()

        if slId.strip() == '':
            slId = None

        if slName.strip() == '':
            slName = None

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql(shId=shId, slId=slId, slName=slName))
        self.m_grid1.ReDrawTable(result)

    def DrawTable(self):
        self.m_grid1.SetRowBackgroundColourChangeEnable(True)
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
            dlg = StoreHouseLocationDialog(None, "查看/修改库位信息", data=data, style=SAVE_NO)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                id = data["slId"]
                db = sqliteUtil.EasySqlite()
                result = db.execute(self.GenQuerySql(slId=id))
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
            wx.MessageBox(u'请勾选要失效的库位', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要失效勾选的' + str(len(rows)) + '条库位吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 0)

    def valid_status(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要有效的库位', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要有效勾选的' + str(len(rows)) + '条库位吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 1)

    def set_status(self, rows, status):
        datas = self.m_grid1.GetGridData(rows=rows)

        sql = "update storehouse_location set status = ? where sl_id in ("
        for index, data in enumerate(datas):
            data["status"] = status

            sql += " '" + data["slId"] + "'"
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


class StoreHouseLocationDialog(wx.Dialog):
    def __init__(self, parent, title, data=None, style=YES_NO):
        wx.Dialog.__init__(self, parent, size=(600, 500), title=title)
        self.sh_dict = GetSHDict()

        panel = wx.Panel(self)

        self.data = data

        vbox = wx.BoxSizer(wx.VERTICAL)

        topLbl = wx.StaticText(panel, -1, title)  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        vbox.Add(topLbl, 0, wx.ALL, 5)
        vbox.Add(wx.StaticLine(panel), 0,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        slId = wx.StaticText(panel, label=u'库位编号 *')
        sh = wx.StaticText(panel, label=u'仓 库 *')
        slName = wx.StaticText(panel, label=u'库位名称 *')
        remark = wx.StaticText(panel, label=u'备 注')

        self.tc_slId = wx.TextCtrl(panel)
        self.sh_choice = wx.Choice(panel)
        self.sh_choice.SetItems(GetDicTypeChoice(self.sh_dict, blank=False))
        self.sh_choice.SetSelection(0)
        self.tc_slName = wx.TextCtrl(panel)
        self.tc_remark = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        if self.data:
            self.tc_slId.SetValue(self.data["slId"])
            self.tc_slId.Enable(False)
            self.sh_choice.SetStringSelection(self.data["shAlias"])
            self.tc_slName.SetValue(self.data["slName"])
            self.tc_remark.SetValue(self.data["remark"])

        fgs = wx.FlexGridSizer(4, 2, 9, 25)
        fgs.AddMany(
            [(sh), (self.sh_choice, 1, wx.EXPAND),
             (slId), (self.tc_slId, 1, wx.EXPAND),
             (slName), (self.tc_slName, 1, wx.EXPAND),
             (remark), (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(3, 1)
        fgs.AddGrowableCol(1, 1)

        vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

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
            vbox.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.TOP, 15)
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
            vbox.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.TOP, 15)

        panel.SetSizer(vbox)
        self.Center()

    def button_add_click(self, evt):
        slId = self.tc_slId.GetValue()
        if slId.strip() == '':
            wx.MessageBox(u'请输入库位编号', u'错误', wx.OK | wx.ICON_ERROR)
            return
        if IsSLExist(slId):
            wx.MessageBox(u'库位编号已存在，请检查', u'错误', wx.OK | wx.ICON_ERROR)
            return

        slName = self.tc_slName.GetValue()
        if slName.strip() == '':
            wx.MessageBox(u'请输入库位名称', u'错误', wx.OK | wx.ICON_ERROR)
            return

        shId = GetDicTypeByName(self.sh_dict, self.sh_choice.GetStringSelection())
        remark = self.tc_remark.GetValue()

        db = sqliteUtil.EasySqlite()
        db.execute(
            "insert into storehouse_location(sl_id, sh_id, sl_name, remark, status, ctime, cby, utime, uby) values(?, ?, ?, ?, 1, datetime('now'),'',datetime('now'),'')",
            [slId, shId, slName, remark])
        self.EndModal(wx.ID_OK)

    def button_update_click(self, evt):
        slName = self.tc_slName.GetValue()
        if slName.strip() == '':
            wx.MessageBox(u'请输入库位名称', u'错误', wx.OK | wx.ICON_ERROR)
            return

        shId = GetDicTypeByName(self.sh_dict, self.sh_choice.GetStringSelection())
        remark = self.tc_remark.GetValue()

        db = sqliteUtil.EasySqlite()
        db.execute(
            "update storehouse_location set sh_id = ?, sl_name = ?, remark = ?, utime = datetime('now') where sl_id = ?",
            [shId, slName, remark, self.data["slId"]])
        self.EndModal(wx.ID_OK)
