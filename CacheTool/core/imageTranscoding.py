# -*- coding: utf-8 -*-
# Author:jiang
# 2021/1/13 14:08
import base64
def imageTranscoding(image_name):
    with open(image_name,"rb") as f:
        image_data=base64.b64encode(f.read())
    # write_data=base64.b64decode(image_data)
    write_data = "img = %s" % image_data
    newimagename=image_name.replace("ico","py")
    print(newimagename)
    print(write_data)
    with open(newimagename,"w+")as f:
        f.write(write_data)

# imageTranscoding("log.ico")
