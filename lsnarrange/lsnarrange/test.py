import json
import requests
import pprint

import requests


#pprint.pprint(response.json())
# 构建添加 教室信息的 消息体，是json格式
payload = {
    "action" : "list_classroom",
    "confirm" : 1,
    "data"   :{
               "district" : "紫金港校区",
              }
}

# 发送请求给web服务
# response = requests.post('http://127.0.0.1:8000/mgr/classroom/?', data=json.dumps(payload))

# 构建查看 客户信息的消息体并发送请求
response = requests.get('http://localhost:8000/mgr/classroom?action=list_classroom')

# 发送请求给web服务
# pprint.pprint 只是用来进行格式化输出

pprint.pprint(response.json)
# pprint.pprint(response.json) 返回json格式的结果
# pprint.pprint(response)  返回 (response 200) 这样的提示