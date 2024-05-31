from openai import OpenAI
import os
import json


class HashtagGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_hashtags(self, content, temperature=0.5, num_tags=5):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an AI agent that generates hashtags for a given piece of content.\
                                           The content will be supplied to your in the form of a prompt.\
                                           Return the result as a JSON-array of the hashtags. \
                                           Generate {num_tags} hashtags for the following content.",
                },
                {"role": "user", "content": f"Content: {content}"},
            ],
            temperature=temperature,
            response_format={"type": "json_object"},
        )

        hashtags_json = completion.choices[0].message.content
        hashtags = json.loads(hashtags_json)

        return hashtags
