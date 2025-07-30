from zhipuai import ZhipuAI

client = ZhipuAI(api_key="00d0e718244f4eb4a1c0c1fc85640a11.THXr41nPePMMx9z4")
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a story about AI."}
    ],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta)
