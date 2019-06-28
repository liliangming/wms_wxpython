#############################
# 字典维护
#############################

import wx
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil

columns = [qtable.CheckBoxColumnDfn(),
           qtable.ColumnDfn(u'字典类型', 'dicTypeName', percent=20, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'字典值', 'dicValue', percent=30, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'备注', 'remark', percent=50, type=qtable.TextType(), readonly=True),
           qtable.ColumnDfn(u'录入时间', 'ctime', size=150, type=qtable.TextType(), readonly=True)
           ]
YES_NO = 1
SAVE_NO = 2
DIC_TYPE_VALUE = "_$1"


def GetDicTypeDict():
    dic = {}
    db = sqliteUtil.EasySqlite()
    result = db.execute(
        "select dic_key as key, dic_value as value from sys_dictionary where dic_type = ? order by dic_key",
        [DIC_TYPE_VALUE])
    for e in result:
        dic[e["key"]] = e["value"]

    return dic


DIC_TYPE_LIST = GetDicTypeDict()


def RefreshDicTypeDict():
    DIC_TYPE_LIST.clear()
    list = GetDicTypeDict()
    for e in list.items():
        DIC_TYPE_LIST[e[0]] = e[1]


def IsDicTypeAndValueExist(dicType, dicValue):
    db = sqliteUtil.EasySqlite()
    result = db.execute(
        "select 1 from sys_dictionary where dic_type = ? and dic_value = ?",
        [dicType, dicValue])
    return result


def GetDicTypeByName(name):
    for dicType in DIC_TYPE_LIST.items():
        if dicType[1] == name:
            return dicType[0]

    return None


def GetDicTypeNameByType(type):
    for dicType in DIC_TYPE_LIST.items():
        if dicType[0] == type:
            return dicType[1]

    return None


def GetDicTypeChoice(blank=True):
    list = []
    if blank:
        list.append("")

    for dicType in DIC_TYPE_LIST.items():
        list.append(dicType[1])

    return list


class DictionaryPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 查询栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.dic_type = wx.StaticText(self, label=u'字典类型：')
        hbox1.Add(self.dic_type, flag=wx.RIGHT, border=8)
        self.dic_type_choice = wx.Choice(self)
        hbox1.Add(self.dic_type_choice, flag=wx.RIGHT, border=8)
        self.dic_value = wx.StaticText(self, label=u'字典值：')
        hbox1.Add(self.dic_value, flag=wx.RIGHT, border=8)
        self.dic_value_text = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.dic_value_text, flag=wx.RIGHT, border=8)
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
        self.add_button.SetToolTipString(u"添加字典")
        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        hbox2.Add(self.add_button, flag=wx.RIGHT, border=8)
        # self.del_button = wx.Button(self, wx.ID_ANY, u"失效", size=(70, 25))
        # self.del_button.SetToolTipString(u"失效字典")
        # self.del_button.Bind(wx.EVT_BUTTON, self.button_del_click)
        # hbox2.Add(self.del_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 失效选择栏
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBox_status = wx.CheckBox(self, -1, u'显示失效字典', pos=(10, 10))
        self.checkBox_status.Bind(wx.EVT_CHECKBOX, self.checkBox_status_change)
        hbox3.Add(self.checkBox_status, flag=wx.RIGHT, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self)

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.dic_type_choice.SetItems(GetDicTypeChoice())
        self.dic_type_choice.SetStringSelection("")
        self.DrawTable()

        self.SetSizer(vbox)
        self.Layout()
        self.Centre(wx.BOTH)

    def GenQuerySql(self, dicType=None, dicKey=None, dicValue=None, offset=None, pageSize=None,
                    orderby=["dic_type", "ctime desc"]):
        sql = "select " \
              "0 as selected, " \
              "dic_type as dicType, " \
              "dic_key as dicKey, " \
              "dic_value as dicValue, " \
              "remark, " \
              "status, " \
              "ctime, " \
              "cby, " \
              "utime, " \
              "uby " \
              "from sys_dictionary where dic_type != '" + DIC_TYPE_VALUE + "'"
        if dicType is not None:
            sql += " and dic_type = " + str(dicType)

        if dicKey is not None:
            sql += " and dic_key = " + str(dicKey)

        if dicValue is not None:
            sql += " and dic_value like \'%%" + dicValue + "%%\'"

        if self.checkBox_status.GetValue():
            sql += " and status in (0,1)"
        else:
            sql += " and status = 1"

        if orderby:
            sql += " order by"
            for index, orderbystr in enumerate(orderby):
                sql += " " + orderbystr
                if index < len(orderby) - 1:
                    sql += ","

        if offset is not None and pageSize is not None:
            sql += " limit " + str(offset) + "," + str(pageSize)

        sql = "select t1.*, t2.dic_value as dicTypeName from (" + sql + ") t1 inner join sys_dictionary t2 on t2.dic_type = '" + DIC_TYPE_VALUE + "' and t2.dic_key = t1.dicType"

        print(sql)
        return sql

    def checkBox_status_change(self, evt):
        self.button_search_click(evt)

    def button_add_click(self, evt):
        dlg = DictionaryDialog(None, title="新增字典信息")
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            db = sqliteUtil.EasySqlite()
            result = db.execute(self.GenQuerySql(offset=0, pageSize=1, orderby=["ctime desc"]))
            self.m_grid1.InsertRows(data=result)

        # 检查字典类型是否有改变
        choice = self.dic_type_choice.GetItems()
        for item in DIC_TYPE_LIST.items():
            if item[1] not in choice:
                self.dic_type_choice.AppendItems([item[1]])
        dlg.Destroy()

    # 失效状态
    def invalid_status(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要失效的字典', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要失效勾选的' + str(len(rows)) + '条字典吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 0)

    def valid_status(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要有效的字典', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要有效勾选的' + str(len(rows)) + '条字典吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 1)

    def set_status(self, rows, status):
        datas = self.m_grid1.GetGridData(rows=rows)

        sql = "update sys_dictionary set status = ? where dic_key in ("
        for index, data in enumerate(datas):
            data["status"] = status

            sql += " " + str(data["dicKey"])
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

    def button_clear_click(self, evt):
        self.dic_type_choice.SetStringSelection("")
        self.dic_value_text.SetValue("")

    def button_search_click(self, evt):
        dicTypeName = self.dic_type_choice.GetStringSelection()
        dicValue = self.dic_value_text.GetValue()

        dicType = None
        if dicTypeName.strip() != '':
            dicType = GetDicTypeByName(dicTypeName)

        if dicValue.strip() == '':
            dicValue = None

        db = sqliteUtil.EasySqlite()
        result = db.execute(self.GenQuerySql(dicType=dicType, dicValue=dicValue))
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
            wx.MessageBox(u'请先点击要编辑的行', u'错误', wx.OK | wx.ICON_ERROR)
            return

        list = self.m_grid1.GetGridData(rows=[row])
        if list:
            data = list[0]
            dlg = DictionaryDialog(None, "修改字典信息", data=data, style=SAVE_NO)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                db = sqliteUtil.EasySqlite()
                result = db.execute(self.GenQuerySql(dicKey=data["dicKey"]))
                # 更新表格数据
                if result:
                    self.m_grid1.RefreshRows([row], data=result)
            dlg.Destroy()
        else:
            wx.MessageBox(u'请先点击要编辑的行', u'错误', wx.OK | wx.ICON_ERROR)


class DictionaryDialog(wx.Dialog):
    def __init__(self, parent, title, data=None, style=YES_NO):
        wx.Dialog.__init__(self, parent, size=(600, 500), title=title)

        panel = wx.Panel(self)

        self.data = data

        vbox = wx.BoxSizer(wx.VERTICAL)

        topLbl = wx.StaticText(panel, -1, title)  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        vbox.Add(topLbl, 0, wx.ALL, 5)
        vbox.Add(wx.StaticLine(panel), 0,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        dicType = wx.StaticText(panel, label=u'字典类型 *')
        dicValue = wx.StaticText(panel, label=u'字典值 *')
        remark = wx.StaticText(panel, label=u'备 注')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.choice_dicTypeName = wx.Choice(panel, choices=GetDicTypeChoice(blank=False))
        self.choice_dicTypeName.SetSelection(0)
        hbox.Add(self.choice_dicTypeName, 0, wx.EXPAND | wx.RIGHT, 5)
        self.addType_button = wx.Button(panel, wx.ID_ANY, u"添加", size=(35, 25))
        self.addType_button.Bind(wx.EVT_BUTTON, self.button_addType_click)
        hbox.Add(self.addType_button, 0, wx.RIGHT | wx.ALIGN_RIGHT, 5)
        self.tc_dicValue = wx.TextCtrl(panel)
        self.tc_remark = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        if self.data:
            self.choice_dicTypeName.SetStringSelection(self.data["dicTypeName"])
            self.tc_dicValue.SetValue(self.data["dicValue"])
            self.tc_remark.SetValue(self.data["remark"])

        fgs = wx.FlexGridSizer(4, 2, 9, 25)
        fgs.AddMany(
            [(dicType), (hbox, 1, wx.EXPAND), (dicValue),
             (self.tc_dicValue, 1, wx.EXPAND), (remark),
             (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(2, 1)
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
        dicType = GetDicTypeByName(self.choice_dicTypeName.GetStringSelection())
        dicValue = self.tc_dicValue.GetValue()
        remark = self.tc_remark.GetValue()
        if dicValue.strip() == '':
            wx.MessageBox(u'请输入字典值', u'错误', wx.OK | wx.ICON_ERROR)
            return
        if IsDicTypeAndValueExist(dicType, dicValue):
            wx.MessageBox(u'字典已存在，请检查', u'错误', wx.OK | wx.ICON_ERROR)
            return
        db = sqliteUtil.EasySqlite()
        db.execute(
            "insert into sys_dictionary(dic_type, dic_value, remark, status, ctime, cby, utime, uby) values(?, ?, ?, 1,datetime('now'),'',datetime('now'),'')",
            [dicType, dicValue, remark])
        self.EndModal(wx.ID_OK)

    def button_update_click(self, evt):
        dicType = GetDicTypeByName(self.choice_dicTypeName.GetStringSelection())
        dicValue = self.tc_dicValue.GetValue()
        remark = self.tc_remark.GetValue()

        if dicValue.strip() == '':
            wx.MessageBox(u'请输入字典值', u'错误', wx.OK | wx.ICON_ERROR)
            return
        if IsDicTypeAndValueExist(dicType, dicValue):
            wx.MessageBox(u'字典已存在，请检查', u'错误', wx.OK | wx.ICON_ERROR)
            return

        db = sqliteUtil.EasySqlite()
        db.execute(
            "update sys_dictionary set dic_type = ?, dic_value = ?, remark = ?, utime = datetime('now') where dic_key = ?",
            [dicType, dicValue, remark, self.data["dicKey"]])
        self.EndModal(wx.ID_OK)

    def button_addType_click(self, evt):
        dlg = DictionaryTypeDialog(None)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            # 刷新字典类型列表
            RefreshDicTypeDict()
            self.choice_dicTypeName.SetItems(GetDicTypeChoice(blank=False))
            self.choice_dicTypeName.SetStringSelection(dlg.tc_dicType.GetValue())
        dlg.Destroy()


class DictionaryTypeDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(300, 150), title="增加字典类型")

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        dicType = wx.StaticText(panel, label=u'字典类型 *')
        hbox.Add(dicType, 0, wx.EXPAND | wx.RIGHT, 5)
        self.tc_dicType = wx.TextCtrl(panel, size=(180, -1))
        hbox.Add(self.tc_dicType, 0, wx.EXPAND | wx.RIGHT, 5)
        vbox.Add(hbox, flag=wx.ALL | wx.EXPAND, border=15)

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

        panel.SetSizer(vbox)
        self.Center()

    def button_add_click(self, evt):
        typeName = self.tc_dicType.GetValue()
        if typeName.strip() == '':
            wx.MessageBox(u'请输入字典类型', u'错误', wx.OK | wx.ICON_ERROR)
            return

        if IsDicTypeAndValueExist(DIC_TYPE_VALUE, typeName):
            wx.MessageBox(u'字典类型已存在，请检查', u'错误', wx.OK | wx.ICON_ERROR)
            return

        db = sqliteUtil.EasySqlite()
        db.execute(
            "insert into sys_dictionary(dic_type, dic_value, remark, status, ctime, cby, utime, uby) values(?, ?, ?, 1,datetime('now'),'',datetime('now'),'')",
            [DIC_TYPE_VALUE, typeName, ""])
        self.EndModal(wx.ID_OK)
