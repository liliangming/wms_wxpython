import wx
import wx.aui
import xml.dom.minidom as xmldom
import os
from ui.test.Test import cjlists
from ui.Customer import CustomerPanel

welcome_content = "商品信息管理系统"
login_content = "登陆"
exit_content = "退出"
tree_dict = {}
xml_file_path = "ui/menu.xml"
xml_ele_key_root = "root"
xml_ele_key_item = "item"
xml_attr_key_name = "name"
xml_attr_key_image = "image"
xml_attr_key_clazz = "clazz"
tree_item_instance_key = "item"


class MainFrame(wx.Frame):
    def __init__(self, parent, user):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="sdsdsd", pos=wx.DefaultPosition, size=wx.Size(1078, 800),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.user = user

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.SetBackgroundColour(wx.Colour(204, 232, 207))

        # 创建状态栏
        self.create_status_bar()

        # 创建菜单栏
        self.create_menu_bar()

        self.s_window = wx.SplitterWindow(parent=self, id=wx.ID_ANY)
        self.left = wx.Panel(parent=self.s_window)
        # self.right = wx.Panel(parent=self.s_window)
        self.right = wx.aui.AuiNotebook(parent=self.s_window)
        self.right.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.change_page, self.right)

        # 设置左右布局的分割窗口left和right
        self.s_window.SplitVertically(self.left, self.right, 200)
        # 设置最小窗格大小，左右布局指左边窗口大小
        self.s_window.SetMinimumPaneSize(80)

        # 创建一棵树
        self.tree = self.create_tree_ctrl(self.left)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_click, self.tree)
        # 为left面板设置一个布局管理器
        self.v_box1 = wx.BoxSizer(wx.VERTICAL)
        self.left.SetSizer(self.v_box1)
        self.v_box1.Add(self.tree, 1, flag=wx.EXPAND | wx.ALL, border=5)

    # 创建菜单栏
    def create_menu_bar(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        menubar.Append(file_menu, '&File')
        self.SetMenuBar(menubar)

        file_menu.Append(-1, "Simple menu item", "This is some help text")
        file_menu.AppendSeparator()
        file_menu.Append(-1, "Exit")

    def create_status_bar(self):
        status = wx.StatusBar(self, -1)  # 实例化 wx.StatusBar
        status.SetFieldsCount(3)  # 状态栏分成3个区域
        status.SetStatusWidths([-2, -1, -1])  # 区域宽度比列，用负数
        status.SetStatusText("当前用户：" + self.user["nickname"], 1)  # 给状态栏设文字
        status.SetStatusText("登录时间：" + self.user["loginTime"], 2)  # 给状态栏设文字
        self.SetStatusBar(status)  # 将状态栏附加到框架上

    def on_click(self, event):
        item = event.GetItem()
        if self.tree.GetChildrenCount(item) == 0:
            self.open_page(item)
        elif self.tree.IsExpanded(item):
            self.tree.Collapse(item)
        else:
            self.tree.Expand(item)

    def open_page(self, item):
        index = self.find_page(item)
        if index == -1:
            # 根据配置文件动态生成UI实例
            clazz_name = tree_dict[self.tree.GetItemText(item)][xml_attr_key_clazz]
            clazz = globals()[clazz_name](self.right)
            self.right.AddPage(clazz, self.tree.GetItemText(item), select=True)
        else:
            self.right.SetSelection(index)

    def find_page(self, item):
        name = self.tree.GetItemText(item)
        index = 0
        count = self.right.GetPageCount()
        while index < count:
            if self.right.GetPageText(index) == name:
                return index

            index += 1
        return -1

    def change_page(self, event):
        item = tree_dict[self.right.GetPageText(self.right.GetSelection())][tree_item_instance_key]
        if item is not None:
            self.tree.SelectItem(item, True)
        pass

    def create_tree_ctrl(self, parent):
        tree = wx.TreeCtrl(parent)
        # 通过wx.ImageList()创建一个图像列表imglist并保存在树中
        img_list = wx.ImageList(16, 16, True, 2)
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        tree.AssignImageList(img_list)

        # 解析菜单配置文件，生成菜单并缓存配置的必要信息
        xmlfilepath = os.path.abspath(xml_file_path)
        domobj = xmldom.parse(xmlfilepath)
        for root_node in domobj.documentElement.getElementsByTagName(xml_ele_key_root):
            attr_name = root_node.getAttribute(xml_attr_key_name)
            attr_image = root_node.getAttribute(xml_attr_key_image)
            attr_clazz = root_node.getAttribute(xml_attr_key_clazz)
            tree_item = tree.AddRoot(attr_name, image=1)
            tree_dict[attr_name] = {xml_attr_key_image: attr_image,
                                    xml_attr_key_clazz: attr_clazz,
                                    tree_item_instance_key: tree_item}
            self.parse_node(root_node, tree, tree_item)

        print(tree_dict)
        # 返回树对象
        return tree

    def parse_node(self, node, tree, tree_father_item):
        if node.hasChildNodes():
            for child in node.childNodes:
                if child.nodeType == 1 and child.nodeName == xml_ele_key_item:
                    attr_name = child.getAttribute(xml_attr_key_name)
                    attr_image = child.getAttribute(xml_attr_key_image)
                    attr_clazz = child.getAttribute(xml_attr_key_clazz)
                    tree_child = tree.AppendItem(tree_father_item, attr_name, 1)
                    tree_dict[attr_name] = {xml_attr_key_image: attr_image,
                                            xml_attr_key_clazz: attr_clazz,
                                            tree_item_instance_key: tree_child}
                    self.parse_node(child, tree, tree_child)

            # 默认展开子节点
            tree.Expand(tree_father_item)
            # 修改图标样式
            tree.SetItemImage(tree_father_item, 0)
