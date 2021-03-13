import selenium
import re

import os
import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# 解决点不动的问题
# https://stackoverflow.com/questions/21350605/python-selenium-click-on-button

from selenium.webdriver.support.ui import WebDriverWait

# 一出现就马上点，这个操作好啊！！！

# https://stackoverflow.com/questions/62868434/button-click-only-works-when-time-sleep-added-for-selenium-python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

options = Options()
# options.headless = True
options.headless=False

# comm="taskkill /f /im firefox.exe"
# os.system(comm)


# proxy="127.0.0.1:10086"
# proxy="120.232.193.208:10087"

# 注意：你用http的时候要开启http全局代理（v2rayN红色图标）！！

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)

# proxies = {
#     'https': 'https://127.0.0.1:64708',  # 查找到你的vpn在本机使用的https代理端口
#     'http': 'http://127.0.0.1:64708',  # 查找到vpn在本机使用的http代理端口
# }

# 换用chrome好了，还是更喜欢chrome一些些...

# driver=webdriver.Chrome(executable_path=r"C:\Users\linsi\AppData\Local\CentBrowser\Application\chromedriver.exe")

# chrome_path=


max_delay=10

def find_element_by_xpath2(patt):
    try:
        res=WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
    except selenium.common.exceptions.TimeoutException:
        res=""
    return res

# import requests

# def find_element_by_xpath2(patt):
#     try:
#         res=WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
#     except selenium.common.exceptions.TimeoutException:
#         res=""
#     return res



def check_IsUploaded(some_link):
    # 会慢一些，设为30s
    driver.get(some_link)
    patt="//div[@class='error error-border']"
    text_node=find_element_by_xpath2(patt)
    if text_node:
        print("fail:",some_link)
        return False
    else:
        print("pass:",some_link)
        return True

# print(check_IsUploaded("https://web.archive.org/web/*/https://lgulife.com/bbs/post/3260/"))
# sys.exit(0)

# with open(r"D:\get_and_check_waybackpacks\latest_links.txt","r",encoding="utf-8") as f:
#     already_links=[each.strip("\n") for each in f.readlines() if each!="\n"]

# for each_link in already_links:
#     check_uploaded(each_link)

# sys.exit(0)

# check_uploaded("http://web.archive.org/web/*/https://linkeer365.github.io/Linkeer365ColorfulLife2/82413386/")
# sys.exit(0)

with open(r"D:\win2vultr\outer_links.txt","r",encoding="utf-8") as f:
    links=[each.strip('\n') for each in f.readlines() if each!='\n']

# def set_proxy():
#     comm1="set http_proxy=socks5://127.0.0.1:10086"
#     comm2="set https_proxy=socks5://127.0.0.1:10086"
#     os.system(comm1)
#     os.system(comm2)

# set_proxy()

comm1="set http_proxy=socks5://127.0.0.1:10086"
comm2="set https_proxy=socks5://127.0.0.1:10086"

waybackpack_path=r"D:\get_and_check_waybackpacks\already_links.txt"
wayback_fail_path=r"D:\get_and_check_waybackpacks\fail_links.txt"
wayback_visited_path=r"D:\get_and_check_waybackpacks\visited_links.txt"

with open(wayback_visited_path,"r",encoding="utf-8") as f:
    visited_links=[each.strip('\n') for each in f.readlines() if each!='\n']

with open(waybackpack_path,"r",encoding="utf-8") as f:
    latest_links=[each.strip('\n') for each in f.readlines() if each!='\n']

visited_set=set(visited_links)

cnt=0

for link in links:
    if link in visited_set:
        print("visited.")
        cnt+=0
        continue
    else:
        comm=f"waybackpack {link} --list --uniques-only"
        total_comm=f"{comm1}&&{comm2}&&{comm}"
        out=os.popen(total_comm)
        links=out.readlines()
        print(links)
        if links:
            latest_link=links[-1]
            # 怎么会读都读不出来呢？
            if "Active code page" in latest_link or "\n" in latest_link:
                if len(links)==1:
                    latest_link=link
                    with open(wayback_fail_path,"a",encoding="utf-8") as f:
                        f.write(latest_link.strip("\n")+"\n")
                    cnt+=1
                    print("gan1!")
                    continue
                else:
                    latest_link=None
                    for i in range(len(links)-1,-1,-1):
                        if "https://web.archive.org" in links[i]:
                            latest_link=links[i]
                            print("yes.")
                            break
                    if latest_link==None:
                        latest_link=link
                        with open(wayback_fail_path,"a",encoding="utf-8") as f:
                            f.write(latest_link.strip("\n")+"\n")
                        print("gan2!")
                        cnt+=1
                        continue
        else:
            latest_link=link
            with open(wayback_fail_path,"a",encoding="utf-8") as f:
                f.write(latest_link.strip("\n")+"\n")
            cnt+=1
            continue
        # print(latest_link)
    if check_IsUploaded(latest_link.strip("\n")):
        with open(waybackpack_path,"a",encoding="utf-8") as f:
            f.write(latest_link.strip("\n")+"\n")
    else:
        with open(wayback_fail_path,"a",encoding="utf-8") as f:
            f.write(latest_link.strip("\n")+"\n")
    with open(wayback_visited_path,"a",encoding="utf-8") as f:
        f.write(link+"\n")
    
    cnt+=1

    if (cnt+1)%40==0:
        comm="taskkill /f /im firefox.exe"
        os.system(comm)
        time.sleep(5)
        driver=webdriver.Firefox(options=options,executable_path=firefox_path)
        print("driver reflesh!")


print("done.")

    # print("cc:",cc)

