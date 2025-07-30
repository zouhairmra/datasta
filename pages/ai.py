from zhipuai import ZhipuAI

client = ZhipuAI(api_key="00d0e718244f4eb4a1c0c1fc85640a11.THXr41nPePMMx9z4")  # Uses environment variable ZHIPUAI_API_KEY
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is artificial intelligence?"}
    ],
    tools=[
        {
            "type": "web_search",
            "web_search": {
                "search_query": "Search the Zhipu",
                "search_result": True,
            }
        }
    ],
    extra_body={"temperature": 0.5, "max_tokens": 50}
)
print(response)
