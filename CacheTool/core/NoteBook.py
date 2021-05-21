# -*- coding: utf-8 -*-
# Author:jiang
# 2020/12/21 16:21
import wx
from CacheTool.core import TabCacheFush,TabDataInitialization,TabPostInterFace,TabSelectSql
class MyNoteBook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.AddPage(TabCacheFush.CacheFush(self), "刷新缓存", select=False)
        self.AddPage(TabSelectSql.SelectSql(self), "SQL查询",select=False)
        self.AddPage(TabDataInitialization.DataInitialization(self), "初始化数据", select=False)
        self.AddPage(TabPostInterFace.PostInterFace(self), "请求接口", select=False)
        # self.AddPage(PostInterFace(self), "接口请求", select=False)
        # self.SetSelection(1) #更改选择页面
        # self.getSelectSql()
    def getCacheFush(self):
        self.SetSelection(0)
        # self.SetSelection(self.GetPageCount()-3)
    def getSelectSql(self):
        self.SetSelection(1)

