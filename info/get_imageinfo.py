# -*- coding: utf-8 -*-
from tools.sina_login import weiboLogin
import urllib2
import re
import json
import requests
import os


class GetInfo:
    #参数说明username：用户名，password：密码，logintype:1为密码登录0为cookie登录，
    def __init__(self, username, password,logintype):
        wblogin = weiboLogin()
        if logintype==1:
            wblogin.login(username,password)
        if logintype==0:
            wblogin.loginbycookies(username, password)

    def getpagebyuid(self, uid):
        userinfo = {}
        url = 'https://weibo.com/u/' + uid + '?from=myfollow_all&is_all=1'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        text = response.read()
        print text
        mid = re.findall(r'&uid=' + uid + '&mid=(.*?)\&', text, re.S)
        uid = re.findall(r'uid\']=\'(.*?)\';', text)
        pid = re.findall(r'pid\']=\'(.*?)\';', text)
        userinfo['mid'] = mid[1]
        userinfo['uid'] = uid[0]
        userinfo['pid'] = pid[0]
        # 4251973823647185
        print userinfo['mid']
        print userinfo['pid']
        return userinfo

    def getphinfo(self, userinfo):
        url = 'https://weibo.com/aj/photo/popview?mid=' + userinfo['mid'] + '&pid=' + userinfo['pid'] + '&type=0&uid=' + \
              userinfo['uid'] + ''
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        html = html.decode('utf-8')
        data = json.loads(html)

        data = data['info']
        pic_list = data['pic_list']
        pic_list = pic_list[0]
        pid = pic_list['pid']
        # htmljson=json.load(html)

        userinfo['pid'] = pid
        url = 'https://weibo.com/aj/photo/popview?mid=' + userinfo['mid'] + '&pid=' + userinfo['pid'] + '&type=0&uid=' + \
              userinfo['uid'] + ''

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        html = html.decode('utf-8')
        data = json.loads(html)
        return data

    def savePhoto(self,name,uid):
        path='pic/'+uid+'/'
        for i in range(len(name)):
            try:
                if not os.path.exists(path):
                    os.mkdir(path)
                if not os.path.exists(path + name[i]):
                    r = requests.get('http://wx4.sinaimg.cn/mw1024/' + name[i])
                    r.raise_for_status()
                    with open(path + name[i], "wb") as f:
                        f.write(r.content)
                    print('finish')
                else:
                    print("ex")
            except Exception as e:
                print('f' + str(e))

    def getphotoname(self, uid, page):

        album_id = ''
        url = 'http://photo.weibo.com/photos/get_all?uid=' \
              + uid + '&album_id=' \
              + album_id + '&count=30&page=' + str(page) \
              + '&type=3&__rnd=1530073299047'

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        html = html.decode('utf-8')
        data = json.loads(html)
        data = data['info']
        total = data['total']
        if int(total)==0:
            #print 'meil'
            return 1
        pic_name = []
        photo_list = data['photo_list']
        for i in range(len(photo_list)):
            if photo_list[i] != None:
                pic_name.append(photo_list[i]['pic_name'])

        self.savePhoto(pic_name, uid)