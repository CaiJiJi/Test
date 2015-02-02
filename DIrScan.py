#! /usr/bin/python
#coding = utf-8
from multiprocessing.dummy import Pool as ThreadPool
import urlparse,argparse,requests

headers = {
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"
}


def ErrorGet(url):
    global errpage
    errpayload = "/0xFA.html"
    # errpayload2 = "/0xFA/"
    url1 = url+errpayload
    # url2 = url+errpayload2
    r = requests.get(url1, headers=headers)
    # u = requests.get(url2, headers=headers)
    errpage = r.text
    # errdic = u.text

def ScanDir(url):
    q = requests.get(url, headers=headers)
    page = q.text
    code = q.status_code
    if code == 200 or code == 301:
        if page != errpage:
            print url
    elif code == 403:
        print url
    return

def Scanno403(url):
    u = requests.get(url, headers=headers)
    page = u.text
    code = u.status_code
    if code == 200 or code == 301:
        if page != errpage:
            print url

def DirScan(url, Dictlist, moudle):
    hostuser = url.split('.')
    hostuser = hostuser[len(hostuser)-2]
    scan =  [hostuser+'.rar',hostuser+'.zip',hostuser+hostuser+'.rar',hostuser+'.rar',hostuser+'.tar.gz',hostuser+'.tar',hostuser+'123.zip',hostuser+'123.tar.gz',hostuser+hostuser+'.zip',hostuser+hostuser+'.tar.gz',hostuser+hostuser+'.tar',hostuser+'.bak']
    f = open(Dictlist,'r')
    lujing = f.read().split('\n')
    Wordlist = scan+lujing
    pool = ThreadPool(10)
    result = []
    for i in range(len(Wordlist)):
        Dict = Wordlist[i]
        url1 = urlparse.urljoin(url,Dict)
        result.append(url1)
    #print result
    #no403 = ['Yes']
    if moudle == 'Yes':
        #print 'a'
        pool.map(ScanDir, result)
        pool.close()
        pool.join()
    elif moudle != 'Yes':
        #print result
        pool.map(Scanno403, result)
        pool.close()
        pool.join()
    # for res in result:
    #     a = res
    #     print a
    print "All Dict Run Over"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='''--url http://www.baidu.com --Dictlist 1.txt (--no403)''', description='ScanTheWebDir')
    parser.add_argument('--url', action="store", dest="url", help="url")
    parser.add_argument('--Dictlist', action="store", dest="Dictlist", help="Dictlist")
    parser.add_argument('--no403', action="store", dest="moudle", help="no403", default="Yes")
    given_args = parser.parse_args()
    url = given_args.url
    Dictlist = given_args.Dictlist
    moudle = given_args.moudle
    print moudle
    if url:
        if Dictlist:
            ErrorGet(url)
            DirScan(url, Dictlist, moudle)
    
     
