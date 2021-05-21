# -*- coding: utf-8 -*-
# Author:jiang
# 2020/12/21 16:23
import wx,os
import wx.adv
from CacheTool.core.codingTransImage import codingTransImage
class TaskBarIcon(wx.adv.TaskBarIcon):  # 窗口最大化 最小化
    ID_About = wx.NewIdRef()
    ID_show = wx.NewIdRef()
    ID_Maxshow = wx.NewIdRef()
    ID_Closeshow = wx.NewIdRef()

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        ico_name=codingTransImage()
        self.SetIcon(wx.Icon(name=ico_name, type=wx.BITMAP_TYPE_ICO), '系统托盘演示!')  # wx.ico为ico图标文件
        os.remove(ico_name)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)  # 定义左键双击
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.Onshow, id=self.ID_show)
        self.Bind(wx.EVT_MENU, self.OnMaxshow, id=self.ID_Maxshow)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
            self.frame.Raise()
    def OnAbout(self, event):
        wx.MessageBox('系统托盘演示V1.0 python2.x!', '关于')

    def Onshow(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
            self.frame.Raise()

    def OnMaxshow(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
        self.frame.Maximize(True)  # 最大化显示

    def OnCloseshow(self, event):
        self.frame.Close(True)  # 右键菜单

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_show, '还原')
        menu.Append(self.ID_Maxshow, '最大化')
        menu.Append(self.ID_About, '关于')
        menu.Append(self.ID_Closeshow, '退出')
        return menu
