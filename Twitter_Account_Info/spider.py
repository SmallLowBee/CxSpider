# coding:utf-8

"""
Twitter账号信息爬虫

@Update: 2020.10.23
"""

import re
import time
from typing import List, Dict

import crawlertool as tool
from Selenium4R import Chrome


class SpiderTwitterAccountInfo(tool.abc.SingleSpider):
    """
    Twitter账号信息爬虫

    最近有效性检验时间:2020.12.28
    """

    def __init__(self, driver):
        self.driver = driver

        # 爬虫实例的变量
        self.user_name = None

    @staticmethod
    def get_twitter_user_name(page_url: str) -> str:
        """提取Twitter的账号用户名称

        主要用于从Twitter任意账号页的Url中提取账号用户名称

        :param page_url: Twitter任意账号页的Url
        :return: Twitter账号用户名称
        """
        if pattern := re.search(r"(?<=twitter.com/)[^/]+", page_url):
            return pattern.group()

    def running(self, user_name: str) -> List[Dict]:
        """执行Twitter账号信息爬虫

        :param user_name: Twitter的账号用户名称（可以通过get_twitter_user_name获取）
        :return: Json格式的Twitter账号数据
        """
        self.user_name = user_name
        actual_url = "https://twitter.com/" + user_name

        self.console("开始抓取,实际请求的Url:" + actual_url)

        self.driver.get(actual_url)
        time.sleep(3)

        item = {}

        if label := self.driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[5]/div[1]/a"):
            item["following"] = tool.extract.number(label.text)
        elif label := self.driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[4]/div[1]/a"):
            item["following"] = tool.extract.number(label.text)
        else:
            self.log("Twitter账号:" + user_name + "|账号正在关注数抓取异常")
            item["following"] = 0

        if label := self.driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[5]/div[2]/a"):
            item["followers"] = tool.extract.number(label.text)
        elif label := self.driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[4]/div[2]/a"):
            item["followers"] = tool.extract.number(label.text)
        else:
            self.log("Twitter账号:" + user_name + "|账号粉丝数抓取异常")
            item["following"] = 0

        return [item]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\Temp")
    print(SpiderTwitterAccountInfo(driver).running(SpiderTwitterAccountInfo.get_twitter_user_name("https://twitter.com/zaobaosg")))
    driver.quit()
