import base64
from zhipuai import ZhipuAI

response = client.chat.completions.create(
    model="glm-4v",
    extra_body={"temperature": 0.5, "max_tokens": 50},
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)
print(response)
