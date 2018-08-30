from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
import os
import smtplib
import sys
import time
import urllib.request
import random

# set browser parameters
url = 'https://f.youdao.com/ds/task.do?method=index'
cookie = 'NTES_SESS=kEjiMGYSeOcpoHHZEI7rKQQtRKMy_EuulbdSEYuhgqt8ybvYyrnuZzvezjzhxdc5kWfY4o27sZiE06.vVj_b7PJmTHDPRUfM6ycMkjlp9HphlCjCEzXXkLQ8lzKOCt.SDaN.mnyoyTo1uYi03mZpqjVqXj2Sgnv0JUYBE54noe5MfF7VfYI58b2E5iqPLIyYynBk4IpX2dBUz; OUTFOX_SEARCH_USER_ID=870989102@223.11.237.87; __utmc=83671489; __ar_v4=WDR2FXVQQJDMFC6ICOL7OE%3A20180803%3A2%7CRLBFEI7CUZATHM373AWPCD%3A20180803%3A2%7CLU2Y3AKPINAIFF2KISP2OT%3A20180803%3A2; JSESSIONID=aaaDQY9OFzFBj8KHR_Euw; JSESSIONID=abcmkGevRTj7lfmwnhFuw; _ntes_nnid=a37fdf06b77131d1a2d6a26a99d9df03,1533825308948; OUTFOX_SEARCH_USER_ID_NCOO=215225012.53930488; DICT_FORCE=true; _ga=GA1.2.649750662.1534843294; __utma=83671489.1579756991.1533285204.1534317956.1534858862.8; __utmz=83671489.1534858862.8.3.utmcsr=fanyi.youdao.com|utmccn=(referral)|utmcmd=referral|utmcct=/; SESSION_FROM_COOKIE=fanyi.youdao.com; VENDOR_FROM=new-fanyicover; Hm_lvt_daca80f0a1ae8b264a9d758c0d7a1bab=1534255137,1534858864,1534858944,1534858948; Hm_lpvt_daca80f0a1ae8b264a9d758c0d7a1bab=1534858948; DICT_LOGIN=8||1535515016983; NTES_SESS=oM4spDQbtEjgEe5wnrk3MxBPJU.fG8QFsGqlZfLZvrTPbX4tbOxW2S4yS0Sza3eErhDt9fwLH2AoC3JPtQGrcq7kjbJZIgyiQQFpXXVzxn.GHjI5uU7dmPVocu8CfELX6wQNzxjB_e7XWuCEhuuw3gcyFXjYEhcnK88RwOitxgnvcNrxIC.nkxXr8dh6vJ.KJKlq3fQGUdbiLJCmRC.PejQKL; NTES_PASSPORT=4GqHlYrcyoHUsZZCG35hv1PEzY8IbRwX6lRa6JVrAmtnUGQvUZBPoCQ0CuCqlOjsA_Nvkgf6Jo5Mf4rJqtVglxGvqwEgdwSGkakWi9.9wdmPftb3p7.JCPjKXz.EuGw5Q.MCIPids6l_t4J1SpVG0Z7xIqVopu1Iqh6KVunEFux7X0BqWD9_m9NMpLsDjsrqA; S_INFO=1535640231|0|##|jingyang_carl@qq.com; P_INFO=jingyang_carl@qq.com|1535640231|1|dict_hts|00&99|CN&1535621855&dict_hts_m#shx&140100#10#0#0|&0|search&dict_hts_m|jingyang_carl@qq.com'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

# set email parameters
sender = 'jingyang_carl@qq.com'
password = 'rhcxlnvlatsuddie'
receiver = 'jingyang_carl@qq.com'

# set while parameters
time_start = time.time()
whileCount = 0
taskIDPool = set()

# initialization
proxy_list = [
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"}
]
proxy = random.choice(proxy_list)
request = urllib.request.Request(url)
request.add_header('cookie', cookie)
request.add_header('User-Agent', userAgent)

try:
    # go into the while
    while True:
        sleepTime = random.randint(1,3)
        time.sleep(sleepTime)

        # print running info
        time_current = time.time()
        whileCount = whileCount+1
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: beginning')

        # open url
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: open URL')
        #opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        #urllib.request.install_opener(opener)
        html = urllib.request.urlopen(request, timeout=10).read().decode()
        soup = BeautifulSoup(html, 'html.parser')

        ############################################################
        # find unfinishedTask
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: unfinished task')
        unfinishedTask = soup.find_all(class_='unfinsh-task')[1]

        ############################################################
        # find fastTask and documentTask
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: document task')
        claimTask = soup.find_all(class_='claim-task')
        # fastTask = claimTask[0]
        documentTask = BeautifulSoup(claimTask[1].prettify(), 'html.parser')

        # find detail tasks
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: task detail')
        tasks = documentTask.find_all(class_='detail-task')
        tempTaskIDPool = set()

        if len(tasks):
            # there are tasks in the list
            # find taskID for each tasks
            for task in tasks:
                task = BeautifulSoup(task.prettify(), 'html.parser')
                taskID = task.find('a')
                tempTaskIDPool.add(taskID.string)

            print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: status update')
            if len(tempTaskIDPool.symmetric_difference(taskIDPool)):
                # there is an update, write the update task and unfinished task into the messagex`
                message = MIMEText(taskID.__str__() + unfinishedTask.__str__(), 'html', 'utf-8')
                message['From'] = Header('jingyang.auto', 'utf-8')
                message['To'] = Header('jingyang_carl', 'utf-8')
                message['Subject'] = Header('Carl: Task Report', 'utf-8')

                # send the email
                print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: email sending')
                server = smtplib.SMTP_SSL('smtp.qq.com')
                server.login(sender, password)
                server.sendmail(sender, receiver, message.as_string())
                print("EMAIL SENDING FINISHED")

                # update the taskIDPool
                taskIDPool = tempTaskIDPool

            else:
                # there isn't a update, redo the while
                print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: no update')
                continue

        else:
            # there isn't any task in the list
            print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: no task')
            continue

finally:
    # the program meet some problem and need to report
    message = MIMEText('The Program meet some Problem', 'html', 'utf-8')
    message['From'] = Header('jingyang.auto', 'utf-8')
    message['To'] = Header('jingyang_carl', 'utf-8')
    message['Subject'] = Header('Carl: Problem Report', 'utf-8')

    # send the email
    server = smtplib.SMTP_SSL('smtp.qq.com')
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())
    print("email sending finished")

    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)
