import wx
from ui.MainFrame import MainFrame


###################################################################
# 主程序入口
###################################################################

def main():
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()


if __name__ == '__main__':
    main()
