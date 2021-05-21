# -*- coding: utf-8 -*-
# Author:jiang
# 2020/12/21 16:21
# -*- coding: utf-8 -*-
# Author:jiang
# 2020/12/21 16:24
import wx
class MyMenu(wx.Frame):  # Frame 样式
    def __init__(self, parent):
        super(MyMenu, self).__init__(parent)
        self.InitUI()
    def InitUI(self):
        # 创建一个菜单栏
        menuBar = wx.MenuBar()
        # 创建一个菜单 1
        fileMenu = wx.Menu()

        # 创建一个菜单项 1-1
        newItem = wx.MenuItem(fileMenu, id=wx.ID_NEW, text='New', kind=wx.ITEM_NORMAL)
        fushItem = wx.MenuItem(fileMenu, id=11111, text='刷新缓存', kind=wx.ITEM_NORMAL)
        SqlItem = wx.MenuItem(fileMenu, id=22222, text='SQL查询', kind=wx.ITEM_NORMAL)
        fileMenu.Append(newItem)
        fileMenu.Append(fushItem)
        fileMenu.Append(SqlItem)
        # 添加一行线
        fileMenu.AppendSeparator()

        # 创建一个子菜单 1-2
        editMenu = wx.Menu()

        # 创建三个子菜单的菜单项目 1-2-1 and 1-2-2 and 1-2-3
        cutItem = wx.MenuItem(editMenu, id=122, text="Cut", kind=wx.ITEM_NORMAL)
        copyItem = wx.MenuItem(editMenu, id=121, text="Copy", kind=wx.ITEM_NORMAL)
        pasteItem = wx.MenuItem(editMenu, id=123, text="Paste", kind=wx.ITEM_NORMAL)
        editMenu.Append(copyItem)
        editMenu.Append(cutItem)
        editMenu.Append(pasteItem)

        # 把子菜单 1-2 添加到菜单 1 中
        fileMenu.AppendSubMenu(editMenu, "Edit")

        # 添加一行线
        fileMenu.AppendSeparator()

        # 添加两个单选框 1-3 and 1-4
        radio1 = wx.MenuItem(fileMenu, id=13, text="Radio_One", kind=wx.ITEM_RADIO)
        radio2 = wx.MenuItem(fileMenu, id=14, text="Radio_Two", kind=wx.ITEM_RADIO)
        fileMenu.Append(radio1)
        fileMenu.Append(radio2)
        # PS.单选框 只在自己区域之间（两行线之间） 相互作用

        # 添加一行线
        fileMenu.AppendSeparator()

        # 添加一个 可选中 的菜单项 1-5
        fileMenu.AppendCheckItem(id=15, item="Check")

        # 添加一个 菜单项 1-6 并注册快捷键
        quit = wx.MenuItem(fileMenu, id=wx.ID_EXIT, text="Quit\tCtrl+Q", kind=wx.ITEM_NORMAL)
        fileMenu.Append(quit)

        # 将 fileMenu 菜单添加到菜单栏中
        menuBar.Append(fileMenu, title='File')

        #设置窗口框架的菜单栏为 menuBar
        # self.SetMenuBar(menuBar)

        # 绑定事件处理

        #
        # # 让其在屏幕中间打开调整大小展示
        # self.SetSize((300, 400))
        # self.Centre()
        # self.Show()
        return menuBar
