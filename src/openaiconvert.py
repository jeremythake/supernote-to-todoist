import json
import os
import openai
import base64

def extract_handwritten_text_from_image(api_key, image_path):
    client = openai.OpenAI(api_key=api_key)

    def encode_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Please extract the handwritten text from this image."
                    }
                ]
            }
        ],
        max_tokens=1024
    )

    return response.choices[0].message.content
