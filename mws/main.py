import wx
from ui.Welcome import WelcomeFrame


###################################################################
# 主程序入口
###################################################################

def main():
    app = wx.App(False)
    frame = WelcomeFrame(None, title="sdsd", size=wx.Size(1078, 679))
    frame.Show(True)
    # start the applications
    app.MainLoop()


if __name__ == '__main__':
    main()
