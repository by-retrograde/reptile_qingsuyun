import os
import re
import time
import requests
from xml.sax.saxutils import unescape

from login.Login import Login

cookies = Login()


# 请求题目列表,获取全部题目数量
def ApiList():
    list_api = "https://api.qingsuyun.com/h5/api/exercise/list/library?classifyPath=&classifyName=&name=&pageNum=1&pageSize=100"
    r_listApi = requests.get(url=list_api, cookies=cookies)
    resData = r_listApi.json()
    listContent = resData["body"]["list"]
    listNum = resData["body"]["total"]
    return listNum, listContent


# 遍历列表并拼接每个apiUrl
def listUrl(listContent):
    url = "https://api.qingsuyun.com/h5/api/exercise/list/mainSwatch?libraryId="
    NewList = []
    for i in listContent:
        id = i["id"]
        NewUrl = url + id
        NewObject = {"name": i["name"], "url": NewUrl}
        NewList.append(NewObject)
    return NewList


# 遍历新的数组对象，爬取每个对象的url内容
def StartMain(NewList):
    pagesList = len(NewList[8:])
    # 遍历所有卷子
    for index, val in enumerate(NewList[8:]):
        pagesNum = index + 1
        fileName = str(val["name"])
        url = val["url"]
        # 请求并获取题目数量
        r_listApi = requests.get(url=url, cookies=cookies)
        resData = r_listApi.json()["body"]["main"]["total"]
        # Num = resData + 1
        # 遍历每个卷子中的题目
        for x in range(1, resData):
            f = open(fileName + ".txt", "a+", encoding="utf-8")  # 创建空文件
            topicUrl = url + "&pageNum=" + str(x)
            r_res = requests.get(url=topicUrl, cookies=cookies)
            listNum = str(x)
            # 过滤试题解析的html换行标签
            dr = re.compile('<[^>]*>', re.S)
            # 试题解析
            ParsingTrue = r_res.json()["body"]["main"]["list"][0]
            if hasattr(ParsingTrue, "analysis"):
                Parsing = r_res.json()["body"]["main"]["list"][0]["analysis"]
                # 过滤试题解析的html换行标签
                problemStr = unescape(dr.sub('', Parsing))
                f.write(str("试题解析：\n" + problemStr + "\n\n"))
            # 问题
            problem = r_res.json()["body"]["main"]["list"][0]["questionContent"]
            problemStr = unescape(dr.sub('', problem))

            f.write(str(listNum + ". " + problemStr + "\n\n"))

            # 获取题目类型
            problemType = r_res.json()["body"]["main"]["list"][0]["questionType"]
            if problemType == 2:
                # 多选题
                problemTypeContent = "multiple"
                # 答案
                answer = r_res.json()["body"]["main"]["list"][0]["jsonData"][problemTypeContent]["options"]
                for i, y in enumerate(answer):
                    # 遍历题目答案选项
                    answerContent = unescape(dr.sub('', y["optionsContent"]))

                    if i == 0:
                        answerNum = "A"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 1:
                        answerNum = "B"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 2:
                        answerNum = "C"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 3:
                        answerNum = "D"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 4:
                        answerNum = "E"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 5:
                        answerNum = "F"
                        f.write(answerNum + ". " + answerContent + "\n")
                    if y["rightAnswers"] == True:
                        f.write(str("正确\n"))
                f.write("\n\n")
                f.close()
                print("正在爬取第" + str(pagesNum) + "套题目，" + "共" + str(pagesList) + "套题目，" + "爬虫完成第" + listNum + "题")
                time.sleep(1)
            elif problemType == 1:
                # 单选题
                problemTypeContent = "single"
                # 答案
                answer = r_res.json()["body"]["main"]["list"][0]["jsonData"][problemTypeContent]["options"]
                for i, y in enumerate(answer):
                    # 遍历题目答案选项
                    answerContent = unescape(dr.sub('', y["optionsContent"]))

                    if i == 0:
                        answerNum = "A"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 1:
                        answerNum = "B"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 2:
                        answerNum = "C"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 3:
                        answerNum = "D"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 4:
                        answerNum = "E"
                        f.write(answerNum + ". " + answerContent + "\n")
                    elif i == 5:
                        answerNum = "F"
                        f.write(answerNum + ". " + answerContent + "\n")
                    if y["rightAnswers"] == True:
                        f.write(str("正确\n"))
                f.write("\n\n")
                f.close()
                print("正在爬取第" + str(pagesNum) + "套题目，" + "共" + str(pagesList) + "套题目，" + "爬虫完成第" + listNum + "题")
                time.sleep(1)
            elif problemType == 4:
                # 判断题
                # 答案
                answer = r_res.json()["body"]["main"]["list"][0]["rightAnswers"]
                if answer == "true":
                    f.write("正确\n")
                else:
                    f.write("错误\n")

                f.write("\n\n")
                f.close()
                print("正在爬取第" + str(pagesNum) + "套题目，" + "共" + str(pagesList) + "套题目，" + "爬虫完成第" + listNum + "题")
                time.sleep(1)

    return
