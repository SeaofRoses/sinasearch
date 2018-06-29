# -*- coding: utf-8 -*-
from info.get_imageinfo import GetInfo

if __name__ == '__main__':
#用户名，密码，登录类型
    getinfo = GetInfo('', '',0)
    uid = ''#用户id
    userinfo = getinfo.getpagebyuid(uid)
    data = getinfo.getphinfo(userinfo)
    # getinfo.getPhoto(info, uid)
    for i in range(4):
        getinfo.getphotoname(uid, i)

