import json

import requests

from model.ListApi import ApiList, listUrl, StartMain

# 返回题目列表与数量
listNum, listContent = ApiList()
# 拼接新的url并返回
NewList = listUrl(listContent)
# 测试
content = StartMain(NewList)
print(content)
