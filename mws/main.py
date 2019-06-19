import wx

from ui.Login import LoginFrame


###################################################################
# 主程序入口
###################################################################

def main():
    app = wx.App(False)
    frame = LoginFrame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()


if __name__ == '__main__':
    main()
