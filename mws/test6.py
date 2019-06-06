import wx

from ui.test.Test import cjlists


def main():
    app = wx.App(False)
    frame = cjlists(wx.Panel(wx.Frame))
    frame.Show(True)
    # start the applications
    app.MainLoop()


if __name__ == '__main__':
    main()