import base64
from zhipuai import ZhipuAI

def encode_image(image_path):
    """Encode image to base64 format"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = ZhipuAI(api_key="your-api-key")
base64_image = encode_image("path/to/your/image.jpg")

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
