# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/19 15:44
import wx,pyperclip,threading
from CacheTool.conf.setting import filename
from CacheTool.MySQL.connectMySql import MySql_go2
from CacheTool.core.flushCache import flushSupplierCache,flushProductCache,viewProductCache,viewSupplierCache

import re
class CacheFush(wx.Panel):  # tab1
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.id_text = wx.StaticText(self, label="请输入ID:", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(5, 5), size=(60, 20))
        self.id_input = wx.TextCtrl(self, -1, value="", pos=(65, 2), size=(85, 25), validator=wx.DefaultValidator)
        self.setIdinputStyle()
        # self.id_input.ForegroundColour = (192, 192, 192)
        self.id_input.Bind(wx.EVT_LEFT_DOWN, self.OnKillFocus)  # 失去焦点事件

        self.btn1 = wx.Button(self, label="刷新商家缓存", size=(85, 30), pos=(250, 2))
        self.btn2 = wx.Button(self, label="查看商家缓存", size=(85, 30), pos=(350, 2))
        self.btn3 = wx.Button(self, label="刷新产品缓存", size=(85, 30), pos=(450, 2))
        self.btn4 = wx.Button(self, label="查看产品缓存", size=(85, 30), pos=(550, 2))
        self.btn5 = wx.Button(self, label="刷新商家所有商品缓存", size=(150, 30), pos=(650, 2))
        self.btn6 = wx.Button(self, label="复制超级密码", size=(120, 30), pos=(820, 2))
        self.result = wx.TextCtrl(self, style=wx.TE_MULTILINE, pos=(5, 40), size=(985, 315))
        self.btn1.Bind(wx.EVT_BUTTON, self.button1)
        self.btn2.Bind(wx.EVT_BUTTON, self.button2)
        self.btn3.Bind(wx.EVT_BUTTON, self.button3)
        self.btn4.Bind(wx.EVT_BUTTON, self.button4)
        self.btn5.Bind(wx.EVT_BUTTON, self.button5)
        self.btn6.Bind(wx.EVT_BUTTON, self.button6)
    def setIdinputStyle(self):
        self.id_input.ForegroundColour = "#808080"  # 设置字体颜色
        self.id_input.SetLabel("请输入商家ID")

    def OnKillFocus(self,event):
        self.id_input.Clear()
        self.id_input.ForegroundColour = (19, 19, 19)
        event.Skip()
    def CacheFushIdInPut(self,event,buttonevent):
        i = self.id_input.GetValue()
        if len(i)==0:
            wx.MessageBox("商家ID不能为空")
        elif i=="请输入商家ID":
            wx.MessageBox("请输入商家ID")
        else:
            print(i)
            buttonevent(i)
        self.setIdinputStyle()
    def button1(self,event):
        self.CacheFushIdInPut(event,self.button1event)
    def button2(self, event):
        self.CacheFushIdInPut(event,self.button2event)
    def button3(self, event):
        self.CacheFushIdInPut(event,self.button3event)
    def button4(self, event):
        self.CacheFushIdInPut(event,self.button4event)
    def button5(self, event):
        self.CacheFushIdInPut(event,self.button5event)
    def button1event(self,i):
        try:
            r = flushSupplierCache(i)
            if r.status_code == 200:
                str=i+"-->:"+r.content.decode("utf-8")
                self.result.Value = str
            else:
                self.result.Value = r.status_code
        except(Exception) as e:
            self.result.Value = str(e)
    def button2event(self,i):
        try:
            r = viewSupplierCache(i)
            print(r.status_code)
            if r.status_code == 200:
                str=i+"-->:"+r.content.decode("utf-8")
                self.result.Value = str
            if r.status_code == 404:
                str=i+"-->:%s"%r
                self.result.Value = str
        except(Exception) as e:
            self.result.Value = e
    def button3event(self, values):
        ids=values.split(',')
        threads=[]
        for id in ids:
            t = threading.Thread(target=flushProductCache, args=(id,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        sql = "SELECT user_id from product where id in (%s)" % values
        result=MySql_go2(sql)
        threads = []
        for id in result:
            t = threading.Thread(target=flushSupplierCache, args=(id,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        self.result.Value = "刷新成功"
        self.setIdinputStyle()


    def button4event(self, i):
        r = viewProductCache(i)
        if r.status_code == 200:
            str = i + "-->:" + r.content.decode("utf-8")
            self.result.Value = str
        if r.status_code == 404:
            str = i + "-->:%s" % r
            self.result.Value = str
        # self.result.Value = r.content.decode("utf-8")
        self.setIdinputStyle()

    def button5event(self, i):
        sql = "select id from product where user_id=%s and state=1" % i
        ids=MySql_go2(sql)
        print(ids)
        threads = []
        for id in ids:
            t = threading.Thread(target=flushProductCache, args=(id,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        self.result.Value = "刷新成功"
        self.setIdinputStyle()

    def button6(self, event):
        res = re.compile(r'supperPassWord="(.*)"')
        with open(filename) as file:
            for line in file.readlines():
                result = res.findall(line)
                if len(result)>0:
                    supperPassWord=result[0]
        pyperclip.copy(supperPassWord)