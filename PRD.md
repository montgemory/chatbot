开发一个使用deepseek的api的聊天机器人。
请分别开发前端和后端，后端使用python，前端使用nextjs，然后帮助我部署到railway.com平台

deepseek api key: sk-b350dd333a474834a25af7c59186d0bd
请求格式：
# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)

stream如果设置为 True，将会以 SSE（server-sent events）的形式以流式发送消息增量。消息流以 data: [DONE] 结尾。

后端开发中增加调试代码，方便部署前后进行调试。完成后端开发，提供一个后端API接口文档，里面写清楚API，端口设置为3004.

前端开发时也增加调试代码，按照API接口文档内容，接入deepseek api，实现流式响应的deepseek聊天机器人。