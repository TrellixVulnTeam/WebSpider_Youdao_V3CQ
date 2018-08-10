import urllib.request

url = 'https://f.youdao.com/ds/task.do?method=index'
cookie = 'OUTFOX_SEARCH_USER_ID=870989102@223.11.237.87; __utmz=83671489.1533285204.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SESSION_FROM_COOKIE=unknown; VENDOR_FROM=unknown; Hm_lpvt_daca80f0a1ae8b264a9d758c0d7a1bab=1533823057; Hm_lvt_daca80f0a1ae8b264a9d758c0d7a1bab=1533285204,1533823057; __utmc=83671489; __ar_v4=WDR2FXVQQJDMFC6ICOL7OE%3A20180803%3A2%7CRLBFEI7CUZATHM373AWPCD%3A20180803%3A2%7CLU2Y3AKPINAIFF2KISP2OT%3A20180803%3A2; NTES_SESS=VoFEyycim_Q5nukRIq64nTwOg73RDNJbi1aBuDk4q.wjxaw1xYbLvewneIecXgSmJRk1sQ4WdvKVjgr61flJzFuDCxrp03nNf5gyB2pqmcySmLBOvUXHr6fj8gxVkquyRxL94CHOwjFZ3hrodFls4vNovQ3vgUc6zsAofmhaAifyREuzt8M4JsM87aZvp6Hmocc0BZ6685aK0iPnWVh_uffAW; S_INFO=1533823071|0|##|jingyang_carl@qq.com; P_INFO=jingyang_carl@qq.com|1533823071|0|dict_hts|00&99|shx&1533375402&dict_hts#shx&140100#10#0#0|&0|dict_hts|jingyang_carl@qq.com; JSESSIONID=aaaDQY9OFzFBj8KHR_Euw; JSESSIONID=abcmkGevRTj7lfmwnhFuw; _ntes_nnid=a37fdf06b77131d1a2d6a26a99d9df03,1533825308948; OUTFOX_SEARCH_USER_ID_NCOO=215225012.53930488; __utma=83671489.1579756991.1533285204.1533823057.1533890323.5; __utmb=83671489.1.10.1533890323'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

request = urllib.request.Request(url)
request.add_header('cookie', cookie)
request.add_header('User-Agent', userAgent)

html = urllib.request.urlopen(request).readlines()

for line in html:
    line = bytes.decode(line)
    print(line)