# -*- coding: utf-8 -*-
# Author:jiang
# 2021/1/13 14:44
import base64
from CacheTool.core.tool import img
from CacheTool.MySQL.connectMySql import tool_ico_name
def codingTransImage():
    with open(tool_ico_name,"wb+")as f:
        f.write(base64.b64decode(img))
    return tool_ico_name
#codingTransImage()

