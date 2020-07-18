import wx

class AppFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(AppFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        staticText = wx.StaticText(panel, label='HQBot', pos=(350, 50))
        font = staticText.GetFont()
        font.PointSize += 10
        font = font.Bold()
        staticText.SetFont(font)

        self.createMenuBar()

        self.screenshotBtn = wx.Button(panel, -1, 'Scan', wx.Point(345, 120))
        self.Bind(wx.EVT_BUTTON, self.takeScreenshot, self.screenshotBtn)

    
    def takeScreenshot(self, event):
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)

        wx.MessageBox('Screenshot taken')

    def createMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&Help')
        
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
     self.Close(True)

    def OnAbout(self, event):
        wx.MessageBox('HQBot v1.00', 'About', wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    frameSize = wx.Size(800, 800)
    frame = AppFrame(None, size=frameSize, title='HQBot')
    frame.Show()
    app.MainLoop()