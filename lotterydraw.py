# -*- coding: utf-8 -*-
# Author:jiang
# 2021/4/25 14:07
import requests,threading
sem=threading.Semaphore(30)
def lotteryDraw(id,userid):
    with sem:
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        url="http://sept.3e3e.cn/base/test-hit?id=%s&userId=%s"%(id,userid)
        reslut=requests.get(url).text
        if (len(reslut))<3000:
            print(userid,">>>>",reslut)
threads=[]
userids=[209188,294074,310406,305006,393352,498632,306846]
#金牌 305006,393352,310406,306846
#服务 294074 209188 498632
id=4
for i in range(200):
    for userid in userids:
        t=threading.Thread(target=lotteryDraw, args=(id,userid))
        threads.append(t)
        t.start()
for i in threads:
    i.join()
