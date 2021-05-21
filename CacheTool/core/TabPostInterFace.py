# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/19 15:24
import wx,logging,threading,MySQLdb
from CacheTool.core.logginginfo import MyLogHandler
from CacheTool.core.flushCache import flushSupplierCache,flushProductCache
from CacheTool.MySQL.connectMySql import MySql_go2,MySqlConfig_drop_shipping
class PostInterFace(wx.Panel):
    msg = "请输入商家ID,多个商家ID用英文,隔开"
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.id_text = wx.StaticText(self, label="POST:", style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(5, 5), size=(60, 20))
        self.id_input = wx.TextCtrl(self, -1, value="", pos=(65, 2), size=(600, 25), validator=wx.DefaultValidator)
        self.setIdinputStyle()
        self.id_input.Bind(wx.EVT_LEFT_DOWN, self.OnKillFocus)  # 失去焦点事件
        self.result = wx.TextCtrl(self, style=wx.TE_MULTILINE, pos=(5, 40), size=(985, 315))
        self.btn1 = wx.Button(self, label="确认", size=(85, 30), pos=(700, 2))
        self.btn1.Bind(wx.EVT_BUTTON, self.buttonFuntion)
        hander=MyLogHandler(self.result)
        logging.getLogger().addHandler(hander)
    def buttonFuntion(self,event):
        self.btn1.Disable() #确认键不可用
        i = self.id_input.GetValue()
        if len(i)==0 or i==self.msg:
            wx.MessageBox("ID不能为空")
        else:
            ids=self.judjeUserId(i)
            if ids==False:
                wx.MessageBox("输入的ID不存在")
            else:
                logging.info("start...")
                supplierids=ids[0]
                purchaserids=ids[1]
                for id in supplierids:
                    msg="--------厂商(%s)信息初始化--------"%(id)
                    logging.info(msg)
                    self.flushSuplier(id)
                    self.flushProduct(id)
                    self.perfectProductInfomation(id)
                    self.updateMoney(id)
                    self.updatePassWord(id)
                for i in purchaserids:
                    msg = "--------采购商(%s)信息初始化--------" % (id)
                    logging.info(msg)
                    self.updateMoney(id)
                    self.updatePassWord(id)
                self.end()
        self.setIdinputStyle()
    def setIdinputStyle(self):
        self.id_input.ForegroundColour = "#808080"  # 设置字体颜色
        self.id_input.SetLabel(self.msg)
    def flushSuplier(self,id):
        try:
            r =flushSupplierCache(id)
            if r.status_code == 200:
                str=id+":-->刷新商家缓存"
                logging.info(str)
            else:
                logging.info(r.status_code)
        except(Exception) as e:
            logging.info(str(e))
    def judjeUserId(self,id):
        userids=id.split(',')
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        supplierid=[]
        purchaserid=[]
        for id in userids:
            print("id",id)
            sql="select user_type from userinfo where out_id='%s'"%id
            cur.execute(sql)
            results=cur.fetchall()
            if len(results)>0:
                result=(results[0][0])
                if result=="PURCHASER":
                    purchaserid.append(id)
                    print("purchaser",id)
                elif result=="SUPPLIER":
                    supplierid.append(id)
                    print("SUPPLIER", id)
            else:
                msg="%s商家ID不存在"%id
                logging.info(msg)
        cur.close()
        conn.close()
        if len(supplierid)==0 and len(purchaserid)==0:
            return False
        else:
            return supplierid,purchaserid
    def flushProduct(self,id):
        sql = "select id from product where user_id=%s and state=1" % id
        ids=MySql_go2(sql)
        print(ids)
        threads = []
        for i in ids:
            t = threading.Thread(target=flushProductCache, args=(i,))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        str=id+":--> 刷新商家产品缓存"
        logging.info(str)
    def perfectProductInfomation(self,id):
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        query_megs_sql="select name,phone,stall_address from gsb_supplier_info where out_user_id=%s"%id
        cur.execute(query_megs_sql)
        query_megs = cur.fetchall()[0]
        supplier_name=query_megs[0]
        supplier_linkman=query_megs[0]
        supplier_phone=query_megs[1]
        supplier_address=query_megs[2]
        update_sql="update gsb_item set supplier_name='%s',supplier_linkman='%s',supplier_mobile='%s',supplier_address='%s'," \
                       "supply_state='ONSALE' where user_id=%s"%(supplier_name,supplier_linkman,supplier_phone,supplier_address,id)
        cur.execute(update_sql)
        conn.commit()
        cur.close()
        conn.close()
        str=id+":-->完善商品信息"
        logging.info(str)
    def updateMoney(self,id):
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        sql = "update account set balance=1000000 where id=(select id from userinfo where username='%s')" % id
        cur.execute(sql)
        conn.commit()
        str =id+ ":-->账户余额初始化金额为：1000000"
        logging.info(str)
        cur.close()
        conn.close()
    def updatePassWord(self,id):
        conn = MySQLdb.Connect(**MySqlConfig_drop_shipping)
        cur = conn.cursor()
        password="9cc2253af4a2fe1a62ab842beaf7cdbe"
        accountupdatesql="update account set account_pwd='%s'where out_id='%s'"%(password,id)
        cur.execute(accountupdatesql)
        conn.commit()
        str = id + ":-->初始化支付密码：123456"
        logging.info(str)
        cur.close()
        conn.close()
    def OnKillFocus(self,event):
        self.id_input.Clear()
        self.id_input.ForegroundColour = (19, 19, 19)
        event.Skip()
    def end(self):
        logging.info("end...")
        self.btn1.Enable() #确认键可用