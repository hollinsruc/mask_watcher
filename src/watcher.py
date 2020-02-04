import sys
sys.path.append("..")

import os, time, json, platform
from selenium import webdriver
from logger import logger as log
from mail import send_mail
from config.mail_config import mail_config
from wechat_msg import send_msg

browser = None

def check_shop(url, keywords):
    browser.get(url)
    time.sleep(3)
    find_flag = False
    for keyword in keywords:
        if keyword in browser.page_source:
            find_flag = keyword
            break
    if not find_flag:
        log.warning("FIND!!!")
        log.warning(url)
        log.warning(keywords)
        send_mail(
             "发现口罩有货!!",
             url,
             mail_config.get("to")
         )
        #send_msg(url)


def check_all_shops():
    with open(os.path.join(os.path.dirname(__file__),"..","config","shop.json"), "r", encoding='UTF-8') as f:
        infos = json.loads(f.read())
        for info in infos:
            for shop in info["shop"]:
                log.info("checking {} / {}".format(shop, info.get("keyword")))
                keywords = info.get("key_word").split(",")
                check_shop(shop, keywords)


# 根据操作系统加载不同的chrome驱动
def load_browser():
    system = platform.system()
    if system =="Windows": #Windows系统
        driver_file_name = "chromedriver.exe"
    elif system =="Darwin": #MacOS系统
        driver_file_name = "chromedriver_mac64"
    else: #Linux系统
        driver_file_name = "chromedriver_linux64"

    return webdriver.Chrome(os.path.join(os.path.dirname(__file__), "chrome_drivers", driver_file_name))

if __name__ == "__main__":
    while True:
        browser = load_browser()
        check_all_shops()
        browser.quit()