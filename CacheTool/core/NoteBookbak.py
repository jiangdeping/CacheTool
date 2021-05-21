# -*- coding: utf-8 -*-
# Author:jiang
# 2020/12/21 16:21
import wx,MySQLdb,requests,pyperclip,threading
from CacheTool.MySQL.connectMySql import MySql_go2,MySql_drop_shipping,MySqlConfig_drop_shipping
import re

class MyNoteBook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.AddPage(CacheFush(self), "刷新缓存", select=False)
        self.AddPage(SelectSql(self), "SQL查询",select=False)
        # self.AddPage(PostInterFace(self), "接口请求", select=False)
        """  
        list = {CacheFush: "刷新缓存", SelectSql: "SQL查询"}
        for k,v in list.items():
            self.AddPage(k(self),v)
        """
        # self.SetSelection(1) #更改选择页面
        # self.getSelectSql()
    def getCacheFush(self):
        self.SetSelection(0)
        # self.SetSelection(self.GetPageCount()-3)
    def getSelectSql(self):
        self.SetSelection(1)
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
    def flushSupplierCache(self,id):
        return requests.get("http://192.168.10.35:12300/producer/user/go2/%s"%id,timeout=5)

    def viewSupplierCache(self, id):
        return requests.get("http://192.168.10.37:16100/go2.cn/cache/supplier/%s" % id, timeout=5)

    def flushProductCache(self, id):
        return requests.get("http://192.168.10.35:12300/producer/product/go2/%s" % id, timeout=5)

    def viewProductCache(self,id):
        return requests.get("http://192.168.10.37:16100/go2.cn/cache/product/%s" % id, timeout=5)
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
            r = self.flushSupplierCache(i)
            if r.status_code == 200:
                str=i+"-->:"+r.content.decode("utf-8")
                self.result.Value = str
            else:
                self.result.Value = r.status_code
        except(Exception) as e:
            self.result.Value = str(e)
    def button2event(self,i):
        try:
            r = self.viewSupplierCache(i)
            if r.status_code == 200:
                str=i+"-->:"+r.content.decode("utf-8")
                self.result.Value = str
            else:
                self.result.Value = r.status_code
        except(Exception) as e:
            self.result.Value = str(e)
    def button3event(self, values):
        ids=values.split(',')
        print("ids--length",len(ids))
        threads=[]
        for id in ids:
            t = threading.Thread(target=self.flushProductCache, args=(id,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        sql = "SELECT user_id from product where id in (%s)" % values
        print(sql)
        result=MySql_go2(sql)

        #根据产品id获取商家名
        #SELECT user_id from product where id=2224886;
        threads = []
        for id in result:
            t = threading.Thread(target=self.flushSupplierCache, args=(id,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        self.result.Value = "刷新成功"
        self.setIdinputStyle()


    def button4event(self, i):
        r = self.viewProductCache(i)
        self.result.Value = r.content.decode("utf-8")
        self.setIdinputStyle()

    def button5event(self, i):
        sql = "select id from product where user_id=%s and state=1" % i
        ids=MySql_go2(sql)
        print(ids)
        threads = []
        for id in ids:
            t = threading.Thread(target=self.flushProductCache, args=(id,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        self.result.Value = "刷新成功"
        self.setIdinputStyle()

    def button6(self, event):
        res = re.compile(r'supperPassWord="(.*)"')
        with open("../conf/sup.txt") as file:
            for line in file.readlines():
                result = res.findall(line)
                if len(result)>0:
                    supperPassWord=result[0]
        pyperclip.copy(supperPassWord)
class SelectSql(wx.Panel):  # tab2
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.icon=wx.Icon("Refresh.ico",wx.BITMAP_TYPE_ICO)
        # self.SetIcon(self.icon)
        self.id_text = wx.StaticText(self, label="货号查登录名", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(2, 5), size=(80, 25))
        self.id_text = wx.StaticText(self, label="修改账户余额", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(2, 30), size=(80, 25))
        self.id_text = wx.StaticText(self, label="更新超级密码", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(2, 55), size=(80, 25))
        self.id_text = wx.StaticText(self, label="完善商品数据", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(2, 80), size=(80, 25))
        self.id_text = wx.StaticText(self, label="更新电话号码", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(2, 105), size=(80, 25))
        self.id_text = wx.StaticText(self, label="登录名查ID", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(2, 130), size=(80, 25))

        self.art_no_input = wx.TextCtrl(self, pos=(92, 2), size=(160, 25))
        self.amount_update = wx.TextCtrl(self, pos=(92,28), size=(160, 25))
        self.password_input = wx.TextCtrl(self, pos=(92,54), size=(160, 25))
        self.var_input = wx.TextCtrl(self, pos=(92, 80), size=(160, 25))
        self.userid_input = wx.TextCtrl(self,pos=(92,106), size=(65,25))
        self.phone_input = wx.TextCtrl(self,pos=(162,106), size=(90,25))
        self.username_input = wx.TextCtrl(self, pos=(92, 132), size=(160, 25))
        # font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        # self.id_text.SetFont(font)
        # self.id_text.BackgroundColour="blue"
        # self.textCtrls=self.GetChildren()
        # self.userid_input.Bind(wx.EVT_LEFT_DOWN, self.OnKillFocus)  # 失去焦点事件
        # self.userid_input.ForegroundColour ="#808080"  # 设置字体颜色
        # self.phone_input.Bind(wx.EVT_LEFT_DOWN, self.OnKillFocus)  # 失去焦点事件
        # self.phone_input.ForegroundColour ="#808080"  # 设置字体颜色
        self.btn1 = wx.Button(self, label="查询", size=(60, 25), pos=(262, 2))
        self.btn2 = wx.Button(self, label="修改", size=(60, 25), pos=(262, 28))
        self.btn3 = wx.Button(self, label="更新", size=(60, 25), pos=(262, 54))
        self.btn4 = wx.Button(self, label="完善", size=(60, 25), pos=(262, 80))
        self.btn5 = wx.Button(self, label="更新", size=(60, 25), pos=(262, 106))
        self.btn6 = wx.Button(self, label="查询", size=(60, 25), pos=(262, 132))

        self.result = wx.TextCtrl(self, pos=(332, 2), size=(300, 25), style=wx.TE_READONLY)
        self.modify_result = wx.TextCtrl(self, pos=(332, 28), size=(300, 25), style=wx.TE_READONLY)
        self.update_result = wx.TextCtrl(self, pos=(332, 54), size=(300, 25), style=wx.TE_READONLY)
        self.procuct_update_result = wx.TextCtrl(self, pos=(332, 80), size=(300, 25), style=wx.TE_READONLY)
        self.phone_update_result = wx.TextCtrl(self, pos=(332,106), size=(300, 25), style=wx.TE_READONLY)
        self.username_input_result=wx.TextCtrl(self, pos=(332,132), size=(300, 25), style=wx.TE_READONLY)
        self.Bind(wx.EVT_BUTTON, self.button1, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.button2, self.btn2)
        self.Bind(wx.EVT_BUTTON, self.button3, self.btn3)
        self.Bind(wx.EVT_BUTTON, self.button4, self.btn4)
        self.Bind(wx.EVT_BUTTON, self.button5, self.btn5)
        self.Bind(wx.EVT_BUTTON, self.button6, self.btn6)
    def OnKillFocus(self,event):
        # print(self.textCtrls)
        self.userid_input.Clear()
        self.phone_input.Clear()
        event.Skip()
    def button1(self, event):
        i = self.art_no_input.GetValue()
        # conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        query = "select user_id  from gsb_item where art_no='%s'" % i
        # # sql="select username from userinfo where id=(select uid  from gsb_item where art_no='%s')"%i
        # cur = conn.cursor()
        # cur.execute(query)
        # result = cur.fetchall()
        result=MySql_drop_shipping(query)
        if len(result) == 0:
            self.result.Value = "对不起,你所输入的货号<%s>不存在" % i
        else:
            id = result[0][0]
            sql = "select username from userinfo where out_id=%s" % id
            # cur.execute(sql)
            # results = cur.fetchall()
            result = MySql_drop_shipping(sql)
            self.result.Value = "货号对应登录名:<%s>,user_id:%s" % (result,id)
            # pyperclip.copy(result) #复制
        # cur.close()
        # conn.close()

    def button2(self, event):
        i = self.amount_update.GetValue()
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        query = "select username from userinfo where username='%s'" % i
        sql = "update account set balance=500000 where id=(select id from userinfo where username='%s')" % i
        cur = conn.cursor()
        cur.execute(query)
        result = MySql_drop_shipping(sql)
        if len(result) == 0:
            self.modify_result.Value = "你输入的用户：%s不存在，请重新输入" % i
        else:
            cur.execute(sql)
            conn.commit()
            self.modify_result.Value = "账户%s余额修改为：500000" % i
        cur.close()
        conn.close()
    def button3(self,event):
        newpasswd = self.password_input.GetValue()
        file_data = ""
        res = re.compile(r'(supperPassWord=)".*"')
        with open("../conf/sup.txt")as file:
            for line in file.readlines():
                result = res.findall(line)
                if len(result) > 0:
                    line = "supperPassWord="+'"'+newpasswd+'"'
                file_data += line
        with open("../conf/sup.txt", "w") as file:
            file.write(file_data)
        msg="超级密码已经更新:"+"'"+newpasswd+"'"
        self.update_result.Value=msg
    def button4(self,event):
        vars=self.var_input.GetValue()
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        query_userid_sql="select user_id from  gsb_item where art_no='%s'"%vars

        cur.execute(query_userid_sql)

        query_userid = cur.fetchall()[0][0]

        query_megs_sql="select name,phone,stall_address from gsb_supplier_info where out_user_id=%s"%query_userid

        cur.execute(query_megs_sql)
        query_megs = cur.fetchall()[0]
        supplier_name=query_megs[0]
        supplier_linkman=query_megs[0]
        supplier_phone=query_megs[1]
        supplier_address=query_megs[2]
        update_sql="update gsb_item set supplier_name='%s',supplier_linkman='%s',supplier_mobile='%s',supplier_address='%s'," \
                   "supply_state='ONSALE' where user_id=%s"%(supplier_name,supplier_linkman,supplier_phone,supplier_address,query_userid)

        cur.execute(update_sql)
        conn.commit()
        self.procuct_update_result.SetValue("商品信息完善成功")
        cur.close()
        conn.close()
    def button5(self,event):
        userid=self.userid_input.GetValue()
        phone=self.phone_input.GetValue()
        update_userinfo_sql="update  userinfo set mobile='%s' where out_id=%s"%(phone,userid)
        update_gsb_supplier_info_sql="update gsb_supplier_info set phone='%s' where out_user_id=%s"%(phone,userid)
        update_gsb_item_sql="update gsb_item set supplier_mobile='%s' where user_id=%s"%(phone,userid)
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        cur.execute(update_userinfo_sql)
        cur.execute(update_gsb_supplier_info_sql)
        cur.execute(update_gsb_item_sql)
        conn.commit()
        self.userid_input.Clear()
        self.phone_input.Clear()
        self.phone_update_result.SetValue("更新电话成功")
        cur.close()
        conn.close()
    def button6(self,event):
        username = self.username_input.GetValue()
        sql="select out_id from userinfo where username='%s'"%username
        result=MySql_drop_shipping(sql)
        if len(result) == 0:
            self.username_input_result.Value = "对不起,你所输入的用户<%s>不存在" %username
        else:
            id = result[0][0]
            self.username_input_result.Value ="当前用户%s的userID:%s"%(username,id)

class PostInterFace(wx.Panel):
    pass
