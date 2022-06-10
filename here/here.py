"""

let a = false;
window.setInterval(function(){
    var refreshHours = new Date().getHours();
    var refreshMin = new Date().getMinutes();
    var refreshSec = new Date().getSeconds();
    if(refreshHours=='10' && refreshMin=='0' && refreshSec=='0' && !a){
        a = true;
        window.location.replace("https://hk.sz.gov.cn:8118/passInfo/detail");
    }
}, 10);

第一个预约按钮：document.getElementsByClassName('card_info')[0].childNodes[1].childNodes[6].childNodes[1].childNodes[1].click()
"""

# 上一节中
# 我们没有加任何修饰单纯几行python代码
# 请求的user-agent是Python-urllib
# 很遗憾，服务器很容易就识别出了你是机器人
# 所以我们要修改user-agent
import time
from urllib.request import urlopen
from urllib.request import Request
from random import choice

url = "https://hk.sz.gov.cn:8118/userPage/login"
with open("../whatismybrowser-user-agent-database.txt", "r") as tf:
    user_agents = tf.read().split('\n')

for i in range(len(user_agents)):
    headers = {
        "User-Agent": user_agents[i % 12],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "hk.sz.gov.cn:8118",
        "Pragma": "no-cache",
        "Referer": "https://hk.sz.gov.cn:8118/passInfo/detail",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Chrome OS"
    }
    # 使用request伪装自己
    request = Request(url, headers=headers)
    # print(request.get_header('User-agent'))
    response = urlopen(request)

    info = response.read()
    time.sleep(0.1)
    print(i, ":", response.status)
