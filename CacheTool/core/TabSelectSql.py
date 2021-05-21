# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/19 15:52
import wx,MySQLdb,re
from CacheTool.conf.setting import filename
from CacheTool.MySQL.connectMySql import MySql_drop_shipping,MySqlConfig_drop_shipping
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
        self.art_no_inputstyle()
        self.amount_updatestyle()
        self.password_inputstyle()
        self.var_inputstyle()
        self.userid_inputstyle()
        self.phone_inputstyle()
        self.username_inputstyle()

        self.art_no_input.Bind(wx.EVT_LEFT_DOWN, self.artnoinputOnKillFocus)
        self.amount_update.Bind(wx.EVT_LEFT_DOWN, self.amountupdateOnKillFocus)
        self.password_input.Bind(wx.EVT_LEFT_DOWN, self.passwordinputOnKillFocus)
        self.var_input.Bind(wx.EVT_LEFT_DOWN, self.varinputOnKillFocus)
        self.userid_input.Bind(wx.EVT_LEFT_DOWN, self.userid_inputOnKillFocus)
        self.phone_input.Bind(wx.EVT_LEFT_DOWN, self.phone_inputOnKillFocus)
        self.username_input.Bind(wx.EVT_LEFT_DOWN, self.username_inputOnKillFocus)

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

    def art_no_inputstyle(self):
        self.art_no_input.ForegroundColour = "#808080"
        self.art_no_input.SetLabel("货号")
    def amount_updatestyle(self):
        self.amount_update.ForegroundColour = "#808080"
        self.amount_update.SetLabel("登录名")
    def password_inputstyle(self):
        self.password_input.ForegroundColour = "#808080"
        self.password_input.SetLabel("超级密码")
    def var_inputstyle(self):
        self.var_input.ForegroundColour = "#808080"
        self.var_input.SetLabel("货号")
    def userid_inputstyle(self):
        self.userid_input.ForegroundColour = "#808080"
        self.userid_input.SetLabel("USERID")

    def phone_inputstyle(self):
        self.phone_input.ForegroundColour = "#808080"
        self.phone_input.SetLabel("电话号码")

    def username_inputstyle(self):
        self.username_input.ForegroundColour = "#808080"
        self.username_input.SetLabel("USERNAME")

    def artnoinputOnKillFocus(self,event):
        self.art_no_input.Clear()
        self.art_no_input.ForegroundColour = (19, 19, 19)
        event.Skip()
    def amountupdateOnKillFocus(self,event):
        self.amount_update.Clear()
        self.amount_update.ForegroundColour = (19, 19, 19)
        event.Skip()

    def passwordinputOnKillFocus(self,event):
        self.password_input.Clear()
        self.password_input.ForegroundColour = (19, 19, 19)
        event.Skip()

    def varinputOnKillFocus(self, event):
        self.var_input.Clear()
        self.var_input.ForegroundColour = (19, 19, 19)
        event.Skip()

    def userid_inputOnKillFocus(self, event):
        self.userid_input.Clear()
        self.userid_input.ForegroundColour = (19, 19, 19)
        event.Skip()
    def phone_inputOnKillFocus(self, event):
        self.phone_input.Clear()
        self.phone_input.ForegroundColour = (19, 19, 19)
        event.Skip()
    def username_inputOnKillFocus(self, event):
        self.username_input.Clear()
        self.username_input.ForegroundColour = (19, 19, 19)
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
            self.result.Value = "货号对应登录名:<%s>,user_id:%s" % (result[0][0],id)
        self.art_no_inputstyle()
            # pyperclip.copy(result) #复制
        # cur.close()
        # conn.close()
    def button2(self, event):
        i = self.amount_update.GetValue()
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur=conn.cursor()
        query = "select username from userinfo where username='%s'" % i
        cur.execute(query)
        result=cur.fetchall()
        updatesql = "update account set balance=500000 where id=(select id from userinfo where username='%s')" % i
        if len(result) == 0:
            self.modify_result.Value = "你输入的用户：%s不存在，请重新输入" % i
        else:
            cur.execute(updatesql)
            conn.commit()
            self.modify_result.Value = "账户%s余额修改为：500000" % i
        self.amount_updatestyle()
        cur.close()
        conn.close()
    def button3(self,event):
        newpasswd = self.password_input.GetValue()
        file_data = ""
        res = re.compile(r'(supperPassWord=)".*"')
        with open(filename)as file:
            for line in file.readlines():
                result = res.findall(line)
                if len(result) > 0:
                    line = "supperPassWord="+'"'+newpasswd+'"'
                file_data += line
        with open(filename, "w") as file:
            file.write(file_data)
        msg="超级密码已经更新:"+"'"+newpasswd+"'"
        self.update_result.Value=msg
        self.password_inputstyle()
    def button4(self,event):
        vars=self.var_input.GetValue()
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        query_userid_sql="select user_id from  gsb_item where art_no='%s'"%vars
        cur.execute(query_userid_sql)
        result=cur.fetchall()
        if len(result)==0:
            self.procuct_update_result.SetValue("你输入的货号不存在")

        else:
            query_userid = result[0][0]
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
        self.var_inputstyle()
        cur.close()
        conn.close()
    def button5(self,event):
        userid=self.userid_input.GetValue()
        phone=self.phone_input.GetValue()
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        user_sql="select username from userinfo where out_id='%s'"%userid
        cur.execute(user_sql)
        result=cur.fetchall()

        if len(result)==0:
            self.phone_update_result.SetValue("用户不存在，请重新输入")
        else:
            username=result[0][0]
            update_userinfo_sql="update  userinfo set mobile='%s',mobile_verified=1 where out_id=%s"%(phone,userid)
            update_gsb_supplier_info_sql="update gsb_supplier_info set phone='%s' where out_user_id=%s"%(phone,userid)
            update_gsb_item_sql="update gsb_item set supplier_mobile='%s' where user_id=%s"%(phone,userid)
            cur.execute(update_userinfo_sql)
            cur.execute(update_gsb_supplier_info_sql)
            cur.execute(update_gsb_item_sql)
            conn.commit()
            self.userid_input.Clear()
            self.phone_input.Clear()
            msg="<%s>电话更新为：%s"%(username,phone)
            self.phone_update_result.SetValue(msg)
        self.userid_inputstyle()
        self.phone_inputstyle()
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
        self.username_inputstyle()