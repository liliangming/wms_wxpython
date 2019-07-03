#!/usr/bin/env python
# encoding: utf8
import wx
import locale
import wx.grid as gridlib


class QGridTable(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        # 设置常量
        self._fields = {}  # dict of fields. Used on class RowData
        self._totalSize = 0  # sum of size of columns with fixed sizes
        self._autoSize = []  # list of columns with variable sizes
        self._percentSize = {}
        self._unknownSize = []
        self._gridData = None
        self._checkBox = True
        self._checkedAll = False
        self._rowHeight = None
        self._rowHeightRatio = 1
        self._rowBackgroundColourChange = False
        self._oddRowColour = wx.Colour(245, 245, 245)
        self._evenRowColour = wx.Colour(255, 255, 255)
        self._invalidRowColour = wx.Colour(192, 192, 192)
        self._popupMenu = None
        self._copy = True
        self._paste = True
        self._exportExcel = True
        self._definePopupMenuItems = []
        self._hotKeys = {}

    def SetRowHeightRatio(self, ratio):
        self._rowHeightRatio = ratio

    def AddPopupMenuItem(self, item):
        self._definePopupMenuItems.append(item)

    def AddHotKey(self, key, function):
        self._hotKeys[key] = function

    def SetCheckBoxEnable(self, enable):
        self._checkBox = enable

    def SetCopyEnable(self, enable):
        self._copy = enable

    def SetPasteEnable(self, enable):
        self._paste = enable

    def SetExportExcelEnable(self, enable):
        self._exportExcel = enable

    def SetRowBackgroundColourChangeEnable(self, enable):
        self._rowBackgroundColourChange = enable

    def SetCheckedRows(self, rows=None, checked=True):
        if self._fields.__contains__("selected"):
            col = self._fields["selected"][0]
            if rows:
                for row in rows:
                    self._gridData.gridData[row]["selected"] = int(checked)
                    self.SetCellValue(row, col, str(int(checked)))
            else:
                for row, item in enumerate(self._gridData.gridData):
                    self._gridData.gridData[row]["selected"] = int(checked)
                    self.SetCellValue(row, col, str(int(checked)))

    def GetCheckedRows(self):
        rows = []
        for row, item in enumerate(self._gridData.gridData):
            if item["selected"]:
                rows.append(row)

        return rows

    def GetGridData(self, all=False, rows=[]):
        if all:
            return self._gridData.gridData

        data = []
        if rows:
            for row in rows:
                data.append(self._gridData.gridData[row])
        return data

    def DeleteRows(self, pos=0, numRows=1, updateLabels=True):
        success = super().DeleteRows(pos, numRows, updateLabels)
        if success:
            for index in range(numRows):
                row = pos + index
                self._gridData.gridData.pop(row)

    def RefreshRows(self, rows=[], data=[]):
        if rows:
            for index, row in enumerate(rows):
                if data and len(data) > index:
                    self._gridData.gridData.pop(row)
                    self._gridData.gridData.insert(row, data[index])
                    self.FillRowData(row)

    def InsertRows(self, pos=0, numRows=1, updateLabels=True, data=None):
        success = super().InsertRows(pos, numRows, updateLabels)
        if success:
            for index in range(numRows):
                row = pos + index
                self.ForceRefresh()
                self.FormatRows(row)
                self.SetGridCursor(row, 0)
                self.MakeCellVisible(row, 0)
                if data is not None and len(data) > index:
                    self._gridData.gridData.insert(row, data[index])
                    self.FillRowData(row)
        return success

    def AppendRows(self, numRows=1, updateLabels=True, data=None):
        newRow = self.GetTable().GetNumberRows()
        success = super().AppendRows(numRows, updateLabels)
        if success:
            for index in range(numRows):
                row = newRow + index
                self.ForceRefresh()
                self.FormatRows(row)
                self.SetGridCursor(row, 0)
                self.MakeCellVisible(row, 0)
                if data is not None and len(data) > index:
                    self._gridData.gridData.insert(row, data[index])
                    for col in range(self._gridData.GetNumCols()):
                        self.SetCellValue(row, col, self._gridData.GetFormartValue(col))
        return success

    def ReDrawTable(self, data):
        if self.GetNumberRows() > 0:
            super().DeleteRows(0, self.GetNumberRows())
        if len(data) > 0:
            self.AppendRows(len(data))

        # 重新填充数据
        self._gridData.SetData(data)
        for row, item in enumerate(data):
            self.FillRowData(row)

    def DrawTable(self, rowdata):
        self._gridData = rowdata
        numCols = self._gridData.GetNumCols()
        numRows = self._gridData.GetNumRows()
        self.CreateGrid(numRows, numCols)

        self.ParseColumns()
        self.SetRowLabelSize(40)
        if numRows > 0:
            self._rowHeight = int(self.GetRowSize(0) * self._rowHeightRatio)
        self.CreatePopupMenu()

        for row in range(numRows):
            self.FormatRows(row)

        # 非固定宽度的列，支持根据窗口大小调整宽度
        if len(self._unknownSize) or len(self._percentSize):
            self.Bind(wx.EVT_SIZE, self.OnSize)

        # 填充数据
        for row in range(numRows):
            self.FillRowData(row)

        # implement all the events
        # 左单击
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        # 右单击
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        # 左双击
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        # 右双击
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
        # label 左单击
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        # label 右单击
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        # label 左双击
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        # label 右双击
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)
        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)
        # 拖动Row大小
        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        # 拖动Col大小
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)
        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.GetGridWindow().Bind(wx.EVT_MOTION, self.onMouseOver)

        self.ForceRefresh()

    def FillRowData(self, row):
        self._gridData.row = row
        # 包含状态字段，并且为失效状态
        invalid = self._gridData.gridData[row].keys().__contains__("status") and not bool(
            self._gridData.gridData[row]["status"])

        for col, item in enumerate(self._gridData.GetColumnDfns()):
            self.SetCellValue(row, col, self._gridData.GetFormartValue(col))
            if invalid:
                self.SetCellBackgroundColour(row, col, self._invalidRowColour)
            elif self._rowBackgroundColourChange and row % 2 == 1:
                self.SetCellBackgroundColour(row, col, self._oddRowColour)
            elif self._rowBackgroundColourChange and row % 2 == 0:
                self.SetCellBackgroundColour(row, col, self._evenRowColour)
            else:
                self.SetCellBackgroundColour(row, col, None)

    def ParseColumns(self):
        for col, item in enumerate(self._gridData.GetColumnDfns()):
            self._fields[item.field] = (col, item)
            self.SetColLabelValue(col, item.label)
            if item.size:
                self._totalSize += item.size
                self.SetColSize(col, item.size)
            elif item.percent:
                self._percentSize[col] = item.percent
                self._autoSize.append(col)
            else:
                self._unknownSize.append(col)
                self._autoSize.append(col)

    def FormatRows(self, row):
        if self._rowHeight:
            self.SetRowSize(row, self._rowHeight)

        for col, item in enumerate(self._gridData.GetColumnDfns()):
            self.SetCellRenderer(row, col, item.type.renderer())
            if item.type.editor() and item.readonly is False:
                self.SetCellEditor(row, col, item.type.editor())
            else:
                self.SetReadOnly(row, col, True)

    def OnSize(self, event):
        width = self.GetSize()[0] - self.GetRowLabelSize() - self._totalSize
        if width > 0:
            for col in self._autoSize:
                weight = self.CalcColWeight(col)
                new_width = width * weight
                if new_width >= 0:
                    self.SetColSize(col, new_width)

    # 按权重计算非固定大小的列宽
    def CalcColWeight(self, col):
        if self._unknownSize and not self._percentSize:
            return 1 / len(self._unknownSize)
        elif not self._unknownSize and self._percentSize:
            return self._percentSize[col] / sum(self._percentSize.values())
        else:
            percent_total = sum(self._percentSize.values())
            if percent_total < 100:
                if col in self._unknownSize:
                    per = (100 - percent_total) / len(self._unknownSize)
                    return per / 100
                else:
                    return self._percentSize[col] / 100
            else:
                # 按比例重新分配总量
                new_total = percent_total + percent_total / len(self._percentSize) * len(self._unknownSize)
                if col in self._unknownSize:
                    per = (new_total - percent_total) / len(self._unknownSize)
                    return per / new_total
                else:
                    return self._percentSize[col] / new_total

    def OnKeyDown(self, evt):
        if evt.GetKeyCode() in self._hotKeys and self._hotKeys[evt.GetKeyCode()]:
            function = self._hotKeys[evt.GetKeyCode()]
            function(evt)
        # ctl + c 支持复制
        elif evt.ControlDown() and evt.GetKeyCode() == 67:
            self.CopyToClipboard()
        # 下
        elif evt.GetKeyCode() == wx.WXK_DOWN:
            self.SetGridCursor(min(self.GetGridCursorRow() + 1, self.GetNumberRows() - 1), self.GetGridCursorCol())
        # 上
        elif evt.GetKeyCode() == wx.WXK_UP:
            self.SetGridCursor(max(self.GetGridCursorRow() - 1, 0), self.GetGridCursorCol())
        # 左
        elif evt.GetKeyCode() == wx.WXK_LEFT:
            self.SetGridCursor(self.GetGridCursorRow(), max(self.GetGridCursorCol() - 1, 0))
        # 右
        elif evt.GetKeyCode() == wx.WXK_RIGHT:
            self.SetGridCursor(self.GetGridCursorRow(), min(self.GetGridCursorCol() + 1, self.GetNumberCols() - 1))
        else:
            evt.Skip()

    def CopyToClipboard(self):
        string = ""
        # 选择列
        if self.GetSelectedCols():
            li = sorted(self.GetSelectedCols())
            for row in range(self.GetNumberRows()):
                for col in li:
                    string += self.GetCellValue(row, col) + "\t"
                string += "\n"
        # 选择行
        elif self.GetSelectedRows():
            li = sorted(self.GetSelectedRows())
            for row in li:
                for col in range(self.GetNumberCols()):
                    string += self.GetCellValue(row, col) + "\t"
                string += "\n"
        # 选择某块区域
        elif len(self.GetSelectionBlockTopLeft()) == 1 and len(self.GetSelectionBlockBottomRight()) == 1:
            for row in self.GetSelectionBlockRows():
                for col in self.GetSelectionBlockCols():
                    string += self.GetCellValue(row, col) + "\t"
                string += "\n"
        # 选择当前单元格
        else:
            string += self.GetCellValue(self.GetGridCursorRow(), self.GetGridCursorCol())

        # 写入剪贴板
        text_obj = wx.TextDataObject()
        text_obj.SetText(string)
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Close()

    def Copy(self, event):
        self.CopyToClipboard()

    def Paste(self, event):
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            text_obj = wx.TextDataObject()
            if wx.TheClipboard.GetData(text_obj):
                text = text_obj.GetText()
                self.SetCellValue(self.GetGridCursorRow(), self.GetGridCursorCol(), text)

    def ExportExcel(self, event):
        print("ExportExcel")

    def onMouseOver(self, evt):
        x, y = self.CalcUnscrolledPosition(evt.GetX(), evt.GetY())
        coords = self.XYToCell(x, y)
        col = coords[1]
        row = coords[0]

        if col != -1 and row != -1:
            value = self.GetCellValue(row, col)
            if value is not None and value.strip() != "":
                dc = wx.ScreenDC()
                dc.SetFont(self.GetCellFont(row, col))
                size = dc.GetTextExtent(value)
                # 内容长度大于单元格长度，tips显示内容
                if size[0] > self.GetColSize(col):
                    evt.GetEventObject().SetToolTip(value)
                else:
                    evt.GetEventObject().SetToolTip("")
            else:
                evt.GetEventObject().SetToolTip("")
        else:
            evt.GetEventObject().SetToolTip("")

        evt.Skip()

    def GetSelectionBlockRows(self):
        row1 = self.GetSelectionBlockTopLeft()[0].Row
        row2 = self.GetSelectionBlockBottomRight()[0].Row

        if row1 == row2:
            return [row1]
        else:
            return range(row1, row2 + 1)

    def GetSelectionBlockCols(self):
        col1 = self.GetSelectionBlockTopLeft()[0].Col
        col2 = self.GetSelectionBlockBottomRight()[0].Col

        if col1 == col2:
            return [col1]
        else:
            return range(col1, col2 + 1)

    def OnCellLeftClick(self, evt):
        if isinstance(self.GetCellRenderer(evt.GetRow(), evt.GetCol()),
                      gridlib.GridCellBoolRenderer) and not self.IsReadOnly(evt.GetRow(), evt.GetCol()):
            value = self.GetCellValue(evt.GetRow(), evt.GetCol())
            if not bool(value) or value == "0":
                # self.SetCellValue(evt.GetRow(), evt.GetCol(), "1")
                self.SetCheckedRows([evt.GetRow()], True)
            else:
                # self.SetCellValue(evt.GetRow(), evt.GetCol(), "0")
                self.SetCheckedRows([evt.GetRow()], False)
        else:
            evt.Skip()

    def CreatePopupMenu(self):
        self._popupMenu = wx.Menu()

        if self._copy:
            item = self._popupMenu.Append(wx.ID_COPY, "复制")
            self.Bind(wx.EVT_MENU, self.Copy, item)

        if self._paste:
            item = self._popupMenu.Append(wx.ID_PASTE, "粘贴")
            self.Bind(wx.EVT_MENU, self.Paste, item)

        if self._copy or self._paste:
            self._popupMenu.AppendSeparator()

        if self._exportExcel:
            item = self._popupMenu.Append(wx.ID_ANY, "导出Excel")
            self.Bind(wx.EVT_MENU, self.ExportExcel, item)
            self._popupMenu.AppendSeparator()

        if len(self._definePopupMenuItems) != 0:
            self.CreateDefinePopupMenuItems()

    def CreateDefinePopupMenuItems(self):
        for pop_item in self._definePopupMenuItems:
            if isinstance(pop_item, SeparatorItem):
                self._popupMenu.AppendSeparator()
            elif len(pop_item.children) == 0:
                item = self._popupMenu.Append(pop_item.action_id, pop_item.name)
                self.Bind(wx.EVT_MENU, pop_item.function, item)
            else:
                self._popupMenu.AppendSubMenu(self.CreateSubPopupMenu(pop_item), pop_item.name)

    def CreateSubPopupMenu(self, pop_item):
        subMenu = wx.Menu()
        for child_item in pop_item.children:
            if isinstance(child_item, SeparatorItem):
                subMenu.AppendSeparator()
            elif len(child_item.children) == 0:
                item = subMenu.Append(child_item.action_id, child_item.name)
                self.Bind(wx.EVT_MENU, child_item.function, item)
            else:
                subMenu.AppendSubMenu(self.CreateSubPopupMenu(child_item), child_item.name)

        return subMenu

    def OnCellRightClick(self, evt):
        self.PopupMenu(self._popupMenu)
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        if isinstance(self.GetCellRenderer(evt.GetRow(), evt.GetCol()),
                      gridlib.GridCellBoolRenderer) and not self.IsReadOnly(evt.GetRow(), evt.GetCol()):
            value = self.GetCellValue(evt.GetRow(), evt.GetCol())
            if not bool(value) or value == "0":
                self.SetCheckedRows([evt.GetRow()], True)
            else:
                self.SetCheckedRows([evt.GetRow()], False)
        else:
            evt.Skip()

    def OnCellRightDClick(self, evt):
        print("OnCellRightDClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        print("OnLabelLeftClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightClick(self, evt):
        print("OnLabelRightClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        print("OnLabelLeftDClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        print("OnLabelRightDClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnGridColSort(self, evt):
        if isinstance(self._gridData.GetColumnDfns()[evt.GetCol()].type, BoolType) and not \
                self._gridData.GetColumnDfns()[
                    evt.GetCol()].readonly:
            self._checkBox = not self._checkBox
            self.SetCheckedRows(checked=self._checkBox)
        print("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())
        evt.Skip()

    def OnRowSize(self, evt):
        print("OnRowSize: row %d, %s\n" %
              (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnColSize(self, evt):
        print("OnColSize: col %d, %s\n" %
              (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print("OnRangeSelect: %s  top-left %s, bottom-right %s\n" %
              (msg, evt.GetTopLeftCoords(), evt.GetBottomRightCoords()))
        evt.Skip()

    def OnCellChange(self, evt):
        print("OnCellChange: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        value = self.GetCellValue(evt.GetRow(), evt.GetCol())

    def OnSelectCell(self, evt):
        # 如果选中的单元不可见，需要改变滚动条位置，使其可见
        print(self.GetScrollLineX())
        print(self.GetScrollLineY())
        print(self.GetSize()[0])
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print("OnSelectCell: %s (%d,%d) %s\n" %
              (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        # row = self.GetGridCursorRow()
        # col = self.GetGridCursorCol()
        #
        # if self.IsCellEditControlEnabled():
        #     self.HideCellEditControl()
        #     self.DisableCellEditControl()
        #
        # value = self.GetCellValue(row, col)
        #
        # if value == 'no good 2':
        #     return  # cancels the cell selection

        evt.Skip()

    def OnEditorShown(self, evt):
        print("OnEditorShown: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorHidden(self, evt):
        # if evt.GetRow() == 6 and evt.GetCol() == 3 and \
        #         wx.MessageBox("Are you sure you wish to  finish editing this cell?",
        #                       "Checking", wx.YES_NO) == wx.NO:
        #     evt.Veto()
        #     return

        print("OnEditorHidden: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorCreated(self, evt):
        print("OnEditorCreated: (%d, %d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetControl()))


class DataType(object):
    '''    Base type, no meant to be used directly. Provide some defaults
    '''

    def __init__(self, *args, **kargs):
        self.args = args
        self.kargs = kargs

    def renderer(self):
        return gridlib.GridCellStringRenderer()

    def editor(self):
        return gridlib.GridCellTextEditor()

    def fromStr(self, value):
        return value

    def toStr(self, value):
        return value


class ReadOnlyType(DataType):
    def editor(self):
        return None


class NumberType(DataType):
    def renderer(self):
        return gridlib.GridCellNumberRenderer()

    def editor(self):
        return gridlib.GridCellNumberEditor(*self.args)

    def fromStr(self, value):
        try:
            return int(value)
        except ValueError:
            return 0

    def toStr(self, value):
        if value != 0:
            return locale.str(value)
        else:
            return u''


class FloatType(DataType):
    def renderer(self):
        return gridlib.GridCellFloatRenderer(*self.args)

    def editor(self):
        return gridlib.GridCellFloatEditor(*self.args)

    def fromStr(self, value):
        try:
            return locale.atof(value)
        except ValueError:
            return 0

    def toStr(self, value):
        if value != 0:
            return locale.str(value)
        else:
            return u''


class BoolType(DataType):
    def renderer(self):
        return gridlib.GridCellBoolRenderer()

    def editor(self):
        return gridlib.GridCellBoolEditor()

    def fromStr(self, value):
        if value == u'1':
            return True
        else:
            return False

    def toStr(self, value):
        if value:
            return u'1'
        else:
            return u''


class TextType(DataType):
    def renderer(self):
        return gridlib.GridCellAutoWrapStringRenderer()

    def editor(self):
        return gridlib.GridCellTextEditor()


class ListType(DataType):
    def __init__(self, *args):
        DataType.__init__(self, *args)
        self.values = [x[0] for x in self.args[0]]
        self.keys = [x[1] for x in self.args[0]]

    def editor(self):
        return gridlib.GridCellChoiceEditor(self.values)

    def fromStr(self, value):
        try:
            idx = self.values.index(value)
            return self.keys[idx]
        except ValueError:
            return None

    def toStr(self, value):
        try:
            idx = self.keys.index(value)
            return self.values[idx]
        except ValueError:
            return ''


class ImageRenderer(gridlib.PyGridCellRenderer):
    def __init__(self, bitmap):
        """ This just places an image
        """
        gridlib.PyGridCellRenderer.__init__(self)
        # self.table = table
        self.bitmap = bitmap
        self.colSize = None
        self.rowSize = None

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        image = wx.MemoryDC()
        image.SelectObject(self.bitmap)

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)

        if isSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangle(rect)

        # copy the image but only to the size of the grid cell
        width, height = self.bitmap.GetWidth(), self.bitmap.GetHeight()

        if width > rect.width - 2:
            width = rect.width - 2

        if height > rect.height - 2:
            height = rect.height - 2

        dc.Blit(rect.x + 1, rect.y + 1, width, height,
                image,
                0, 0, wx.COPY, True)


class ButtonType(DataType):
    def renderer(self):
        return ImageRenderer(self.args[0])

    def editor(self):
        return None

    def fromStr(self, value):
        pass

    def toStr(self, value):
        pass


class ColumnDfn(object):
    """To define columns, if size is None, this is an autosize column"""

    def __init__(self, title, field, size=None, percent=None, type=DataType(), readonly=False):
        self.label = title
        self.field = field
        self.size = size
        self.percent = percent
        self.type = type
        self.readonly = readonly


class CheckBoxColumnDfn(ColumnDfn):
    def __init__(self, title=u"全选", field="selected", size=30, _type=BoolType(), readonly=False):
        self.label = title
        self.field = field
        self.size = size
        self.type = _type
        self.readonly = readonly


class GridData(dict):
    def __init__(self, my_Grid, columns, gridData):
        self._grid = my_Grid
        self.columns = columns
        self.gridData = gridData
        self.row = 0

    def GetValue(self, row, col):
        item = self.columns[col]
        if self.gridData[self.row].keys().__contains__(item.field):
            return self.gridData[row][item.field]
        else:
            return None

    def GetFormartValue(self, col):
        item = self.columns[col]
        if self.gridData[self.row].keys().__contains__(item.field):
            return item.type.toStr(self.gridData[self.row][item.field])
        else:
            return None

    def GetValue(self, col):
        item = self.columns[col]
        if self.gridData[self.row].keys().__contains__(item.field):
            return self.gridData[self.row][item.field]
        else:
            return None

    def GetColumnDfns(self):
        return self.columns

    def GetData(self):
        return self.gridData

    def SetData(self, date):
        self.gridData = date

    def GetNumRows(self):
        return len(self.gridData)

    def GetNumCols(self):
        return len(self.columns)


class MenuBarItem(object):
    def __init__(self, name, function, action_id=wx.ID_ANY):
        self.name = name
        self.function = function
        self.action_id = action_id
        self.children = []

    def AddChild(self, child):
        self.children.append(child)


class SeparatorItem(MenuBarItem):
    def __init__(self):
        self.name = None
        self.function = None
        self.action_id = None
        self.children = []
