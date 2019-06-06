#!/usr/bin/env python
# encoding: utf8
import wx
import locale
import wx.grid as gridlib


class QGridTable(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        # TODO 设置常量
        self._numRows = 0
        self._columnData = []
        self.fields = {}  # dict of fields. Used on class RowData
        self.totalsize = 0  # sum of size of columns with fixed sizes
        self.autosize = []  # list of columns with variable sizes
        self.rowdata = RowData(self)
        self._rowBackgroundColourChange = False
        self._oddRowBackgroundColour = gridlib.GridCellAttr()
        self._oddRowBackgroundColour.SetBackgroundColour(wx.Colour(245, 245, 245))
        self._evenRowBackgroundColour = gridlib.GridCellAttr()
        self._evenRowBackgroundColour.SetBackgroundColour(wx.Colour(255, 255, 255))

    def SetRowBackgroundColourChange(self, isChange):
        self._rowBackgroundColourChange = isChange

    def DrawTable(self, columns, data):
        self._numRows = len(data)
        self._columnData = columns

        self.CreateGrid(self._numRows, len(self._columnData))
        self.ParseColumns()
        self.SetRowLabelSize(40)

        for row in range(self._numRows):
            self.FormatRows(row)

        # 非固定宽度的列，支持根据窗口大小调整宽度
        if len(self.autosize):
            self.Bind(wx.EVT_SIZE, self.OnSize)

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

        self.ForceRefresh()

    def ParseColumns(self):
        for col, item in enumerate(self._columnData):
            self.fields[item.field] = (col, item)
            self.SetColLabelValue(col, item.label)
            if item.size:
                self.totalsize += item.size
                self.SetColSize(col, item.size)
            else:
                self.autosize.append(col)

    def OnSize(self, event):
        width = self.GetSize()[0] - self.GetRowLabelSize() - self.totalsize
        for col in self.autosize:
            new_width = width / len(self.autosize)
            if new_width >= 0:
                self.SetColSize(col, new_width)

    def FormatRows(self, row):
        # self.SetRowSize(row, self.height_row)
        for col, item in enumerate(self._columnData):
            self.SetCellRenderer(row, col, item.type.renderer())
            if item.type.editor() and item.readonly is False:
                self.SetCellEditor(row, col, item.type.editor())
            else:
                self.SetReadOnly(row, col, True)
        if self._rowBackgroundColourChange and row % 2 == 1:
            self.SetRowAttr(row, self._oddRowBackgroundColour)
        elif self._rowBackgroundColourChange and row % 2 == 0:
            self.SetRowAttr(row, self._evenRowBackgroundColour)

    def OnCellLeftClick(self, evt):
        print("OnCellLeftClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellRightClick(self, evt):
        print("OnCellRightClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        print("OnCellLeftDClick: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
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
        print("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())

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
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print("OnSelectCell: %s (%d,%d) %s\n" %
              (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()

        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()

        value = self.GetCellValue(row, col)

        if value == 'no good 2':
            return  # cancels the cell selection

        evt.Skip()

    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
                wx.MessageBox("Are you sure you wish to edit this cell?",
                              "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        print("OnEditorShown: (%d,%d) %s\n" %
              (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
                wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                              "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

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

    def __init__(self, title, field, size=None, _type=DataType(), readonly=False):
        self.label = title
        self.field = field
        self.size = size
        self.type = _type
        self.readonly = readonly


class RowData(dict):
    """a dict-like class to easy access of data. dataitems return a real dict,
    __getitem__ return data from row, __getattr__ return data as an attribute"""

    def __init__(self, my_grid):
        self._grid = my_grid
        self.row = 0  # from which row can be get and set all the data
        self.initialised = True  # to access dict items as class properties

    def update(self, data):
        for key, value in data.items():
            self.__setitem__(key, value)

    def dataitems(self):
        """creates a dict to put all the data in the correspondent format
        self.m_grid1[row+1]=self.m_grid1[row].dataitems()"""
        data = {}
        for (col, item) in self._grid.fields.values():
            data[item.field] = item.type.fromStr(self._grid.GetCellValue(self.row, col))
        return data

    def __len__(self):
        return len(self._grid.fields)

    def __getitem__(self, key):
        'get items from self.row row and key field'
        col, item = self._grid.fields[key]
        value = self._grid.GetCellValue(self.row, col)
        return item.type.fromStr(value)

    def __setitem__(self, key, value):
        'set items on self.row row and key field'
        col, item = self._grid.fields[key]
        formatted = item.type.toStr(value)
        self._grid.SetCellValue(self.row, col, formatted)

    def __repr__(self):
        'return a string representing the data'
        return repr(self.dataitems())

    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        if not self.__dict__.keys().__contains__(
                'initialised'):  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif self.__dict__.keys().__contains__(
                item):  # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def isEmpty(self):
        for col in range(self.__len__()):
            if self._grid.GetCellValue(self.row, col).strip():
                return False
        return True
