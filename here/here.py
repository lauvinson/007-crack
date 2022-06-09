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

https://hk.sz.gov.cn:8118/passInfo/detail

第一个预约按钮：document.getElementsByClassName('card_info')[0].childNodes[1].childNodes[6].childNodes[1].childNodes[1].click()
"""