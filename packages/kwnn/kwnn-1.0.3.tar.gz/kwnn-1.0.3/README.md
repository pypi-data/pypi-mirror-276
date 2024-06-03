## 会问牛牛 Python3 SDK

> api key 请联系商务开通。

### 1、安装sdk

```
pip install kwnn
```


### 2、发起一个请求
```python
import os
from kwnn import KwnnAI

client = KwnnAI(
    base_url="可选代理url",
    api_key=os.environ.get("KWNN_API_KEY"),
    timeout=120, # default
)
```

#### 请求参数

|参数|类型|是否必填|说明|
|----|----|-------|---|
|cid|uuid|否|会话id，带上第一次响应的cid可支持上下文|
|content|str|是|问题内容|
|stream|bool|否|流式输出|

#### 响应参数
|参数|类型|说明|
|----|----|---|
|cid|uuid|会话id，用于上下文|
|mid|uuid|消息id|
|message|array|响应的内容|
|content|str|AI生成的内容|

```json
{
    "cid": "1639a26f-fbcb-499f-823e-826fb3e448e1",
    "mid": "b15aef9e-5512-4d5f-8b22-04a3c57fcacf",
    "message": [
        {
            "content": "我是会问牛牛，专注于回答关于财务内容的问题。"
        }
    ]
}
```

### 3、调用对话API
#### 流式输出
```python
import os
from kwnn import KwnnAI

client = KwnnAI(
    api_key=os.environ.get("KWNN_API_KEY")
)

stream = client.chat.completions.create(
    content="你好！",
    stream=True,
)

for chunk in stream:
    if chunk.message[0].content is not None:
        print(chunk.message[0].content)
```
#### 非流式输出
```python
import os
from kwnn import KwnnAI

client = KwnnAI(
    api_key=os.environ.get("KWNN_API_KEY")
)

completion = client.chat.completions.create(
    content="你好！",
)

print(completion.message[0].content)
```