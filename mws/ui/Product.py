#############################
# 产品维护
#############################

import wx
import os
import shutil
import util.QTable as qtable
import util.SqliteUtil as sqliteUtil
import util.CheckList as checkList

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


def GetProductCategoryDict():
    dic = {}
    db = sqliteUtil.EasySqlite()
    result = db.execute(
        " select t1.dic_key as key, t1.dic_value as value "
        " from sys_dictionary t1 "
        " inner join sys_dictionary t2 "
        " on t2.dic_key = t1.dic_type "
        " where t2.dic_type = ?"
        " and t2.dic_value = ? "
        " and t1.status = 1 "
        " order by t1.dic_key",
        ["_$1", PRODUCT_CATEGORY_VALUE])
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


def IsProductCodeExist(productId, productCode):
    sql = "select 1 from product where product_code = '" + productCode + "'"
    if productId:
        sql += " and product_id != " + str(productId)

    db = sqliteUtil.EasySqlite()
    result = db.execute(sql)

    return result


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)


class ProductPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.product_category_dict = GetProductCategoryDict()

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 查询栏
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.product_category = wx.StaticText(self, label=u'产品分类：')
        hbox1.Add(self.product_category, flag=wx.RIGHT, border=8)
        self.choice_product_category = wx.Choice(self)
        hbox1.Add(self.choice_product_category, flag=wx.RIGHT, border=8)
        self.product_code = wx.StaticText(self, label=u'产品编码：')
        hbox1.Add(self.product_code, flag=wx.RIGHT, border=8)
        self.tc_product_code = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.tc_product_code, flag=wx.RIGHT, border=8)
        self.product_name = wx.StaticText(self, label=u'产品名称：')
        hbox1.Add(self.product_name, flag=wx.RIGHT, border=8)
        self.tc_product_name = wx.TextCtrl(self, size=wx.Size(150, -1))
        hbox1.Add(self.tc_product_name, flag=wx.RIGHT, border=8)
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
        self.add_button.SetToolTipString(u"添加产品")
        self.add_button.Bind(wx.EVT_BUTTON, self.button_add_click)
        hbox2.Add(self.add_button, flag=wx.RIGHT, border=8)
        self.del_button = wx.Button(self, wx.ID_ANY, u"删除", size=(70, 25))
        self.del_button.SetToolTipString(u"删除产品")
        self.del_button.Bind(wx.EVT_BUTTON, self.button_del_click)
        hbox2.Add(self.del_button, flag=wx.RIGHT, border=8)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 失效选择栏
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBox_status = wx.CheckBox(self, -1, u'显示失效产品', pos=(10, 10))
        self.checkBox_status.Bind(wx.EVT_CHECKBOX, self.checkBox_status_change)
        hbox3.Add(self.checkBox_status, flag=wx.RIGHT, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 画表格
        self.m_grid1 = qtable.QGridTable(self)

        vbox.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.choice_product_category.SetItems(GetDicTypeChoice(self.product_category_dict))
        self.choice_product_category.SetStringSelection("")
        self.DrawTable()

        self.SetSizer(vbox)
        self.Layout()

        self.Centre(wx.BOTH)

    def GenQuerySql(self, productId=None, productCategory=None, productCode=None, productName=None, offset=None,
                    pageSize=None):
        sql = "select " \
              "0 as selected, " \
              "product_id as productId, " \
              "product_code as productCode, " \
              "product_name as productName, " \
              "product_desc as productDesc, " \
              "product_category as productCategory, " \
              "remark, " \
              "status, " \
              "ctime, " \
              "cby, " \
              "utime, " \
              "uby " \
              "from product where 1 = 1"
        if productId is not None:
            sql += " and product_id = '" + str(productId) + "'"

        if productName is not None:
            sql += " and product_name like \'%%" + productName + "%%\'"

        if productCategory is not None:
            sql += " and product_category = '" + str(productCategory) + "'"

        if productCode is not None:
            sql += " and product_code = '" + productCode + "'"

        if self.checkBox_status.GetValue():
            sql += " and status in (0,1)"
        else:
            sql += " and status = 1"

        sql += " order by ctime desc"

        if offset is not None and pageSize is not None:
            sql += " limit " + str(offset) + "," + str(pageSize)

        sql = "select t1.*, t2.dic_value as productCategoryName from (" + sql + ") t1 left join sys_dictionary t2 on t2.dic_key = t1.productCategory"

        print(sql)
        return sql

    def checkBox_status_change(self, evt):
        self.button_search_click(evt)

    def button_add_click(self, evt):
        dlg = ProductAddDialog(None, title="新增产品信息")
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            db = sqliteUtil.EasySqlite()
            result = db.execute(self.GenQuerySql(offset=0, pageSize=1))
            self.m_grid1.InsertRows(data=result)
        dlg.Destroy()

    def button_del_click(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要删除的产品', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要删除勾选的' + str(len(rows)) + '条数据吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        datas = self.m_grid1.GetGridData(rows=rows)
        sql = "delete from product where product_id in ("

        for index, data in enumerate(datas):
            sql += " '" + str(data["productId"]) + "'"
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
        self.choice_product_category.SetStringSelection("")
        self.tc_product_code.SetValue("")
        self.tc_product_name.SetValue("")

    def button_search_click(self, evt):
        productCategory = GetDicTypeByName(self.product_category_dict,
                                           self.choice_product_category.GetStringSelection())
        productCode = self.tc_product_code.GetValue()
        productName = self.tc_product_name.GetValue()

        if productCode.strip() == '':
            productCode = None

        if productName.strip() == '':
            productName = None

        db = sqliteUtil.EasySqlite()
        result = db.execute(
            self.GenQuerySql(productCategory=productCategory, productCode=productCode, productName=productName))
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
            dlg = ProductUpdDialog(None, "查看/修改产品信息", data=data)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                db = sqliteUtil.EasySqlite()
                result = db.execute(self.GenQuerySql(productId=data["productId"]))
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
            wx.MessageBox(u'请勾选要失效的产品', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要失效勾选的' + str(len(rows)) + '条数据吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 0)

    def valid_status(self, evt):
        rows = self.m_grid1.GetCheckedRows()
        if not rows:
            wx.MessageBox(u'请勾选要有效的产品', u'错误', wx.OK | wx.ICON_ERROR)
            return

        res = wx.MessageBox(u'确认要有效勾选的' + str(len(rows)) + '条数据吗', u'提示', wx.YES_NO | wx.ICON_INFORMATION)
        if res == wx.NO:
            return
        self.set_status(rows, 1)

    def set_status(self, rows, status):
        datas = self.m_grid1.GetGridData(rows=rows)

        sql = "update product set status = ? where product_id in ("
        for index, data in enumerate(datas):
            data["status"] = status

            sql += " '" + str(data["productId"]) + "'"
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


class ProductAddDialog(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, size=(600, 500), title=title)
        self.product_category_dict = GetProductCategoryDict()

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        topLbl = wx.StaticText(panel, -1, title)  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        vbox.Add(topLbl, 0, wx.ALL, 5)
        vbox.Add(wx.StaticLine(panel), 0,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        productCategoryName = wx.StaticText(panel, label=u'产品分类 *')
        productCode = wx.StaticText(panel, label=u'产品编码 *')
        productName = wx.StaticText(panel, label=u'产品名称 *')
        productDesc = wx.StaticText(panel, label=u'产品描述')
        remark = wx.StaticText(panel, label=u'备 注')

        self.choice_productCategoryName = wx.Choice(panel)
        self.choice_productCategoryName.SetItems(GetDicTypeChoice(self.product_category_dict, blank=False))
        self.choice_productCategoryName.SetSelection(0)
        self.tc_productCode = wx.TextCtrl(panel)
        self.tc_productName = wx.TextCtrl(panel)
        self.tc_productDesc = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.tc_remark = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fgs = wx.FlexGridSizer(5, 2, 9, 25)
        fgs.AddMany(
            [(productCategoryName), (self.choice_productCategoryName, 1, wx.EXPAND),
             (productCode), (self.tc_productCode, 1, wx.EXPAND),
             (productName), (self.tc_productName, 1, wx.EXPAND),
             (productDesc), (self.tc_productDesc, 1, wx.EXPAND),
             (remark), (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(4, 1)
        fgs.AddGrowableCol(1, 1)

        vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

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

    def button_add_click(self, evt):
        productCategory = GetDicTypeByName(self.product_category_dict,
                                           self.choice_productCategoryName.GetStringSelection())
        productCode = self.tc_productCode.GetValue()
        if productCode.strip() == '':
            wx.MessageBox(u'请输入商品编码', u'错误', wx.OK | wx.ICON_ERROR)
            return

        if IsProductCodeExist(None, productCode):
            wx.MessageBox(u'商品编码已存在，请检查', u'错误', wx.OK | wx.ICON_ERROR)
            return

        productName = self.tc_productName.GetValue()
        if productName.strip() == '':
            wx.MessageBox(u'请输入商品名称', u'错误', wx.OK | wx.ICON_ERROR)
            return
        productDesc = self.tc_productDesc.GetValue()
        remark = self.tc_remark.GetValue()
        db = sqliteUtil.EasySqlite()
        db.execute(
            "insert into product(product_code, product_name, product_desc, product_category, remark, status, ctime, cby, utime, uby) values(?, ?, ?, ?, ?, 1, datetime('now'),'',datetime('now'),'')",
            [productCode, productName, productDesc, productCategory, remark])
        self.EndModal(wx.ID_OK)


class ProductUpdDialog(wx.Dialog):
    def __init__(self, parent, title, data=None):
        wx.Dialog.__init__(self, parent, size=(600, 500), title=title)
        self.data = data

        panel = wx.Panel(self)

        nb = wx.Notebook(panel)

        self.page1 = ProductInfoPage(nb, self.data)
        self.page2 = ProductAttachPage(nb, self.data)
        self.page3 = ProductAttrPage(nb, self.data)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.page1, "产品信息")
        nb.AddPage(self.page2, "产品附件")
        nb.AddPage(self.page3, "产品属性")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND)

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

    def button_update_click(self, evt):
        productCategory = GetDicTypeByName(self.page1.product_category_dict,
                                           self.page1.choice_productCategoryName.GetStringSelection())
        productCode = self.page1.tc_productCode.GetValue()
        if productCode.strip() == '':
            wx.MessageBox(u'请输入商品编码', u'错误', wx.OK | wx.ICON_ERROR)
            return

        if IsProductCodeExist(self.data["productId"], productCode):
            wx.MessageBox(u'商品编码已存在，请检查', u'错误', wx.OK | wx.ICON_ERROR)
            return

        productName = self.page1.tc_productName.GetValue()
        if productName.strip() == '':
            wx.MessageBox(u'请输入商品名称', u'错误', wx.OK | wx.ICON_ERROR)
            return
        productDesc = self.page1.tc_productDesc.GetValue()
        remark = self.page1.tc_remark.GetValue()

        db = sqliteUtil.EasySqlite()
        db.execute(
            "update product set product_code = ?, product_name = ?, product_desc = ?, product_category = ?, remark = ?, utime = datetime('now') where product_id = ?",
            [productCode, productName, productDesc, productCategory, remark, self.data["productId"]])
        self.EndModal(wx.ID_OK)


class ProductInfoPage(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        self.data = data
        self.product_category_dict = GetProductCategoryDict()

        vbox = wx.BoxSizer(wx.VERTICAL)

        topLbl = wx.StaticText(self, wx.ID_ANY, u"基本信息")
        topLbl.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(topLbl, 0, wx.ALL, 5)

        productCategoryName = wx.StaticText(self, label=u'产品分类 *')
        productCode = wx.StaticText(self, label=u'产品编码 *')
        productName = wx.StaticText(self, label=u'产品名称 *')
        productDesc = wx.StaticText(self, label=u'产品描述')
        remark = wx.StaticText(self, label=u'备 注')

        self.choice_productCategoryName = wx.Choice(self)
        self.choice_productCategoryName.SetItems(GetDicTypeChoice(self.product_category_dict, blank=False))
        self.choice_productCategoryName.SetSelection(0)
        self.tc_productCode = wx.TextCtrl(self)
        self.tc_productName = wx.TextCtrl(self)
        self.tc_productDesc = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.tc_remark = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        if self.data:
            self.choice_productCategoryName.SetStringSelection(self.data["productCategoryName"])
            self.tc_productCode.SetValue(self.data["productCode"])
            self.tc_productName.SetValue(self.data["productName"])
            self.tc_productDesc.SetValue(self.data["productDesc"])
            self.tc_remark.SetValue(self.data["remark"])

        fgs = wx.FlexGridSizer(5, 2, 9, 25)
        fgs.AddMany(
            [(productCategoryName), (self.choice_productCategoryName, 1, wx.EXPAND),
             (productCode), (self.tc_productCode, 1, wx.EXPAND),
             (productName), (self.tc_productName, 1, wx.EXPAND),
             (productDesc), (self.tc_productDesc, 1, wx.EXPAND),
             (remark), (self.tc_remark, 1, wx.EXPAND)])

        fgs.AddGrowableRow(4, 1)
        fgs.AddGrowableCol(1, 1)

        vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

        self.SetSizer(vbox)


class ProductAttachPage(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        self.data = data
        self.product_attach = []

        vbox = wx.BoxSizer(wx.VERTICAL)

        topLbl = wx.StaticText(self, wx.ID_ANY, u"附件列表")
        topLbl.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(topLbl, 0, wx.ALL, 5)

        self.list = checkList.CheckListCtrl(self)
        self.list.SetSize(wx.Size(800, 800))
        self.list.InsertColumn(0, u'文件名称', width=140)
        self.list.InsertColumn(1, u'文件大小')
        self.list.InsertColumn(2, u'上传时间')
        self.list.InsertColumn(3, u'备注')

        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDclick)

        self.DrawList()

        vbox.Add(self.list, 1,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBox_all = wx.CheckBox(self, -1, u'全选', pos=(10, 10))
        self.checkBox_all.Bind(wx.EVT_CHECKBOX, self.checkBox_all_change)
        hbox1.Add(self.checkBox_all, flag=wx.RIGHT, border=10)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT, border=5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.upload_button = wx.Button(self, wx.ID_ANY, u"上传", size=(70, 25))
        self.upload_button.SetToolTipString(u"上传附件")
        self.upload_button.Bind(wx.EVT_BUTTON, self.button_upload_click)
        hbox2.Add(self.upload_button, flag=wx.RIGHT | wx.LEFT, border=10)
        self.download_button = wx.Button(self, wx.ID_ANY, u"下载", size=(70, 25))
        self.download_button.SetToolTipString(u"下载选择的附件")
        self.download_button.Bind(wx.EVT_BUTTON, self.button_download_click)
        hbox2.Add(self.download_button, flag=wx.RIGHT | wx.LEFT, border=10)
        self.del_button = wx.Button(self, wx.ID_ANY, u"删除", size=(70, 25))
        self.del_button.SetToolTipString(u"删除选择的附件")
        self.del_button.Bind(wx.EVT_BUTTON, self.button_del_click)
        hbox2.Add(self.del_button, flag=wx.RIGHT | wx.LEFT, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vbox)

    def DrawList(self):
        sql = "select attach_id as attachId, " \
              "product_id as productId, " \
              "attach_name as attachName, " \
              "attach_path as attachPath, " \
              "attach_size as attachSize, " \
              "remark as remark, " \
              "ctime, " \
              "cby, " \
              "utime, " \
              "uby " \
              "from product_attach where product_id = ? order by ctime desc"
        print(sql)
        db = sqliteUtil.EasySqlite()
        result = db.execute(sql, str(self.data["productId"]))

        self.product_attach = result
        if result:
            for idx, data in enumerate(result):
                index = self.list.InsertItem(idx, data["attachName"])
                self.list.SetItem(index, 1, data["attachSize"])
                self.list.SetItem(index, 2, data["ctime"])
                self.list.SetItem(index, 3, data["remark"])
        else:
            self.list.ClearAll()

    def OnDclick(self, evt):
        os.startfile(self.product_attach[evt.GetItem().GetId()]["attachPath"])

    def checkBox_all_change(self, evt):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, self.checkBox_all.GetValue())

    def GetCheckedItems(self):
        rows = []
        num = self.list.GetItemCount()
        for i in range(num):
            if self.list.IsChecked(i):
                rows.append(i)

        return rows

    def button_upload_click(self, evt):
        dlg = wx.FileDialog(self, message=u"选择文件",
                            # defaultDir=os.getcwd(),
                            # defaultFile="",
                            style=wx.FD_OPEN | wx.FD_MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            productId = str(self.data["productId"])
            root = os.path.join(os.getcwd(), "upload", "product", productId)
            if not os.path.exists(root):
                os.makedirs(root)
            for path in paths:
                newPath = shutil.copy(path, root)
                db = sqliteUtil.EasySqlite()
                db.execute(
                    "insert into product_attach(product_id, attach_name, attach_path, attach_size, remark, ctime, cby, utime, uby) values(?, ?, ?, ?, '', datetime('now'), '', datetime('now'), '')",
                    [productId, os.path.basename(path), newPath, formatSize(os.path.getsize(path))])
            self.DrawList()
        dlg.Destroy()

    def button_download_click(self, evt):
        rows = self.GetCheckedItems()
        if not rows:
            wx.MessageBox(u'请勾选要下载的附件', u'错误', wx.OK | wx.ICON_ERROR)
            return

    def button_del_click(self, evt):
        rows = self.GetCheckedItems()
        if not rows:
            wx.MessageBox(u'请勾选要删除的附件', u'错误', wx.OK | wx.ICON_ERROR)
            return


packages = [('abiword', '5.8M', 'base'), ('adie', '145k', 'base'),
            ('airsnort', '71k', 'base'), ('ara', '717k', 'base'), ('arc', '139k', 'base'),
            ('asc', '5.8M', 'base'), ('ascii', '74k', 'base'), ('ash', '74k', 'base'), ('ash', '74k', 'base'),
            ('ash', '74k', 'base'), ('ash', '74k', 'base'), ('ash', '74k', 'base'), ('ash', '74k', 'base')]


class ProductAttrPage(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)
        self.data = data

        vbox = wx.BoxSizer(wx.VERTICAL)

        topLbl = wx.StaticText(self, wx.ID_ANY, u"属性列表")
        topLbl.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(topLbl, 0, wx.ALL, 5)

        self.list = checkList.CheckListCtrl(self)
        self.list.SetSize(wx.Size(800, 800))
        self.list.InsertColumn(0, u'属性名称')
        self.list.InsertColumn(1, u'属性值')
        self.list.InsertColumn(2, u'备注')

        # idx = 0
        #
        # for i in packages:
        #     index = self.list.InsertItem(idx, i[0])
        #     self.list.SetItem(index, 1, i[1])
        #     self.list.SetItem(index, 2, i[2])
        #     idx += 1

        vbox.Add(self.list, 1,
                 wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBox_status = wx.CheckBox(self, -1, u'全选', pos=(10, 10))
        hbox1.Add(self.checkBox_status, flag=wx.RIGHT, border=10)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT, border=5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.upload_button = wx.Button(self, wx.ID_ANY, u"新增", size=(70, 25))
        self.upload_button.SetToolTipString(u"新增")
        hbox2.Add(self.upload_button, flag=wx.RIGHT | wx.LEFT, border=10)
        self.del_button = wx.Button(self, wx.ID_ANY, u"删除", size=(70, 25))
        self.del_button.SetToolTipString(u"删除选择的属性")
        hbox2.Add(self.del_button, flag=wx.RIGHT | wx.LEFT, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vbox)
