import os
from kwnn import KwnnAI


client = KwnnAI(
    api_key=os.environ.get("KWNN_API_KEY"),
)

stream = True
response = client.chat.completions.create(
    content="你是谁",
    stream=stream,
)

if stream:
    for chunk in response:
        if chunk.message[0].content is not None:
            print("test chunk: ", chunk.message[0].content)
else:
    print(response.message[0].content)
