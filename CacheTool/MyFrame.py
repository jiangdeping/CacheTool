# -*- coding: utf-8 -*-
# Author:jiang
# 2020/12/21 16:24
import wx,os

from CacheTool.core.windowOperaiton import  TaskBarIcon
from CacheTool.core.menu import MyMenu
from CacheTool.core.NoteBook import MyNoteBook
from CacheTool.core.codingTransImage import codingTransImage
"pyinstaller -F -w MyFrame.py"
"pyinstaller -F -w -i D:\pythonTest\XGT_tool\CacheTool\core\log.ico MyFrame.py"
class MyFrame(wx.Frame):  # Frame 样式
    def __init__(self, parent):
        super(MyFrame, self).__init__(parent, pos=(180, 100), size=(1000, 400), title="星购途")
        ico_name=codingTransImage()
        self.icon=wx.Icon(ico_name, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        # menuBar=MyMenu(self).InitUI() #获取菜单
        # self.Bind(wx.EVT_MENU, self.menuHandler)
        # self.SetMenuBar(menuBar)
        self.book=MyNoteBook(self)
        self.taskBarIcon = TaskBarIcon(self) #窗口最大化、最小化
        # 绑定事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE,self.OnIconfiy)  # 窗口最小化时，调用OnIconfiy,注意Wx窗体上的最小化按钮，触发的事件是 wx.EVT_ICONIZE,而根本就没有定义什么wx.EVT_MINIMIZE,但是最大化，有个wx.EVT_MAXIMIZE。
        self.Show()
    def menuHandler(self, event):
        id = event.GetId()
        if id == 11111:
            self.book.getCacheFush()
        if id == 22222:
            self.book.getSelectSql()
    def OnHide(self, event):
        self.Hide()
    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()
    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()
app=wx.App()
frame=MyFrame(None)
app.MainLoop()