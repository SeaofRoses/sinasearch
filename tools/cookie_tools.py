# -*- coding: utf-8 -*-
import cookielib
import urllib2

class CookieTools:
    def initCookies(self):
        # 设置保存cookie的文件
        filename = 'cookie.txt'
        # 声明一个MozillaCookieJar对象来保存cookie，之后写入文件
        cookie = cookielib.MozillaCookieJar(filename)
        # 创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        # 构建opener
        opener = urllib2.build_opener(handler)

        urllib2.install_opener(opener)
        return cookie

    def saveCookie(self,cookie):
        # 设置保存cookie的文件
        filename = 'cookie.txt'
        cookie.save(filename,ignore_discard=True, ignore_expires=True)

    def getCookie(self):
        cookie = cookielib.MozillaCookieJar()
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        for item in cookie:
            print 'name:' + item.name + '-value:' + item.value

        cookie_support = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        return cookie