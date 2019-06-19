import wx
import pymysql


# 由于当前对布局管理器不是很熟悉，所系使用的是固定位置，导致窗口拉伸的效果不是很好
class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        frame = wx.Frame(parent=None, title='登陆', size=(532, 420))
        # 设置窗口的左上角的图标
        # 其中参数type表示图片的类型，还有ico，jpgm等类型
        icon_1 = wx.Icon(name='images/logo.png', type=wx.BITMAP_TYPE_PNG)
        frame.SetIcon(icon_1)

        panel = wx.Panel(frame, -1)
        # 向panel中添加图片
        image = wx.Image("images/bg.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wx.StaticBitmap(panel, -1, bitmap=image, pos=(0, 0))

        # 添加静态标签
        label_user = wx.StaticText(panel, -1, "账号:", pos=(80, 200))
        label_pass = wx.StaticText(panel, -1, "密码:", pos=(80, 240))
        # 添加文本输入框
        self.entry_user = wx.TextCtrl(panel, -1, size=(200, 30), pos=(130, 200))
        # style 为设置输入
        self.entry_pass = wx.TextCtrl(panel, -1, size=(200, 30), pos=(130, 240), style=wx.TE_PASSWORD)
        # 添加按钮
        self.but_login = wx.Button(panel, -1, "登陆", size=(120, 50), pos=(120, 300))
        self.but_cancel = wx.Button(panel, -1, "退出", size=(120, 50), pos=(260, 300))
        # 设置按钮的颜色
        # self.but_login.SetBackgroundColour("#0a74f7")
        # self.but_register.SetBackgroundColour("#282c34")
        # 给按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.on_but_login, self.but_login)
        self.Bind(wx.EVT_BUTTON, self.on_but_cancel, self.but_cancel)
        #
        frame.Center()
        frame.Show(True)

    # 定义一个消息弹出框的函数
    def show_message(self, word=""):
        dlg = wx.MessageDialog(None, word, u"错误", wx.YES_NO | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            # self.Close(True)
            pass
        dlg.Destroy()

    def on_but_login(self, event):
        # 连接到本地数据库

        user_name = self.entry_user.GetValue()
        pass_word = self.entry_pass.GetValue()

        sql = """select pass from student where name ='%s' """ % (user_name)
        # 判断，查看用户名和密码名是否为空
        # 不为空之后在进行查询和判断
        # 不然当密码或用户名为空时会出现会导致出错
        if user_name and pass_word:
            db = pymysql.connect(host="localhost", user="root",
                                 password="zhang123", db="user", port=3306)
            # 使用cursor()方法获取操作游标
            cur = db.cursor()
            try:

                cur.execute(sql)  # 执行sql语句

                results = cur.fetchall()  # 获取查询的所有记录
                # 返回值是一个元组的形式
                # print(type(results))
                if results:
                    # print(type(results[0][0]))
                    # print(results[0][0])
                    if results[0][0] == pass_word:
                        # 表示登陆成功，后续可以写登陆成功后的界面
                        # 此处就不再写
                        pass
                        # print("sucessful")

                    else:
                        self.show_message(word="密码错误")


                else:
                    self.show_message(word='用户名不存在')

            except Exception as e:
                db.rollback()


            finally:

                db.close()  # 关闭连接
        else:
            self.show_message(word='账号和密码不能为空')

    def on_but_cancel(self, event):
        pass


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
