import json
import requests
import pprint

# 构建添加 教室信息的 消息体，是json格式
payload = {
    "action":"add_classroom",
    "data":{
        "name":"B-302",
        "capacity":"133",
        "id":"2",
        "building":"西一",
        "district":"紫金港校区"
    }
}

# 发送请求给web服务
response = requests.post('http://localhost/mgr/classroom',
              json=payload)

pprint.pprint(response.json())

# 构建查看 客户信息的消息体
response = requests.get('http://localhost/mgr/classroom?action=list_classroom')

# 发送请求给web服务
pprint.pprint(response.json())