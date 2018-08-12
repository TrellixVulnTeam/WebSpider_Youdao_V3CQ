from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
import os
import smtplib
import sys
import time
import urllib.request

# set browser parameters
url = 'https://f.youdao.com/ds/task.do?method=index'
cookie = 'OUTFOX_SEARCH_USER_ID=870989102@223.11.237.87; __utmz=83671489.1533285204.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SESSION_FROM_COOKIE=unknown; VENDOR_FROM=unknown; Hm_lpvt_daca80f0a1ae8b264a9d758c0d7a1bab=1533823057; Hm_lvt_daca80f0a1ae8b264a9d758c0d7a1bab=1533285204,1533823057; __utmc=83671489; __ar_v4=WDR2FXVQQJDMFC6ICOL7OE%3A20180803%3A2%7CRLBFEI7CUZATHM373AWPCD%3A20180803%3A2%7CLU2Y3AKPINAIFF2KISP2OT%3A20180803%3A2; NTES_SESS=VoFEyycim_Q5nukRIq64nTwOg73RDNJbi1aBuDk4q.wjxaw1xYbLvewneIecXgSmJRk1sQ4WdvKVjgr61flJzFuDCxrp03nNf5gyB2pqmcySmLBOvUXHr6fj8gxVkquyRxL94CHOwjFZ3hrodFls4vNovQ3vgUc6zsAofmhaAifyREuzt8M4JsM87aZvp6Hmocc0BZ6685aK0iPnWVh_uffAW; S_INFO=1533823071|0|##|jingyang_carl@qq.com; P_INFO=jingyang_carl@qq.com|1533823071|0|dict_hts|00&99|shx&1533375402&dict_hts#shx&140100#10#0#0|&0|dict_hts|jingyang_carl@qq.com; JSESSIONID=aaaDQY9OFzFBj8KHR_Euw; JSESSIONID=abcmkGevRTj7lfmwnhFuw; _ntes_nnid=a37fdf06b77131d1a2d6a26a99d9df03,1533825308948; OUTFOX_SEARCH_USER_ID_NCOO=215225012.53930488; __utma=83671489.1579756991.1533285204.1533823057.1533890323.5; __utmb=83671489.1.10.1533890323'
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
request = urllib.request.Request(url)
request.add_header('cookie', cookie)
request.add_header('User-Agent', userAgent)

try:
    # go into the while
    while True:
        time.sleep(1)

        # print running info
        time_current = time.time()
        whileCount = whileCount+1
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: beginning')

        # open url
        print('running time: ' + str(time_current - time_start) + '; count: ' + str(whileCount) + '; status: open URL')
        html = urllib.request.urlopen(request).read().decode()
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

    os.execl(sys.executable, sys.executable, *sys.argv)
