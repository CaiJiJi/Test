import requests,random,re,json

def DomainGet(target):
    Query = 'http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=1&_=1422858334980' % target
    print Query
    ip = str(random.randint(1,100))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))
    headers = {
    'Accept': 'image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
    'X-Forwarded-For': ip,
    'Referer': Query,
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'
    }
    q = requests.get(Query, headers=headers)
    result = q.text
    decoded = json.loads(result)
    json.dumps(decoded, sort_keys=True, indent=4)
    print decoded['domains'][0]
