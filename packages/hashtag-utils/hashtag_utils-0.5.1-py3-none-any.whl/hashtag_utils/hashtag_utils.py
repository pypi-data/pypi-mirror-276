import traceback
from typing import List
from openai import OpenAI
import os
import json
from .common import is_alphanumeric



class HashtagUtils:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_hashtags(self, content: str, temperature=0.5, num_tags=5) -> List[str]:
        try:
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
        except Exception as e:
            traceback.print_exc()
            return None
        
    def get_similar_hashtags(self, tags: List[str], temperature=0.5, num_tags=5) -> List[str]:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI agent that analyses hashtags and generates similar hashtags.\
                                            The hashtags will be supplied to your in the form of a prompt.\
                                            Return the result as a JSON-array of the similar hashtags. \
                                            Generate {num_tags} hashtags for the following hashtags.",
                    },
                    {"role": "user", "content": f"Hashtags: {",".join(tags)}"},
                ],
                temperature=temperature,
                response_format={"type": "json_object"},
            )

            hashtags_json = completion.choices[0].message.content
            hashtags = json.loads(hashtags_json)

            return hashtags
        except Exception as e:
            traceback.print_exc()
            return None

    def get_hashtag_definition(self, hashtag: str, temperature=0.5) -> str:
        try:
            if not hashtag or len(hashtag) == 0:
                return None
            
            if not hashtag.startswith("#"):
                hashtag = f"#{hashtag}"

            if not is_alphanumeric(hashtag[1:]):
                raise ValueError("Hashtag should contain only alphanumeric characters")

            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI agent that defines hashtags.\
                                            The hashtag will be supplied to your in the form of a prompt.\
                                            Return the result as a JSON with hashtag (string), confidence_percent (0 to 1 range,float) and definition (string). \
                                            The confidence percent indicates how accurate the definition is in defining the hashtag. \
                                            Define the following hashtag.",
                    },
                    {"role": "user", "content": f"Hashtag: {hashtag}"},
                ],
                temperature=temperature,
                response_format={"type": "json_object"},
            )

            definition = completion.choices[0].message.content

            return definition
        except Exception as e:
            traceback.print_exc()
            return None
        
    def get_one_hashtag_relevance(self, tag: str, content: str, temperature=0.5) -> List[str]:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI agent that analyses hashtags and content to determine relevance.\
                                            The hashtag and content will be supplied to your in the form of a prompt.\
                                            Return the result as a JSON object with hashtag (string) and relevance_score (float) \
                                            The relevance score is the degree with which there's a match between the hashtag and the content. \
                                            Determine the relevance of the following hashtag to the content.",
                    },
                    {"role": "user", "content": f"Hashtag: {tag} \nContent: {content}"},
                ],
                temperature=temperature,
                response_format={"type": "json_object"},
            )

            hashtags_json = completion.choices[0].message.content
            hashtags = json.loads(hashtags_json)

            return hashtags
        except Exception as e:
            traceback.print_exc()
            return None
        
    def get_hashtags_relevance(self, tags: List[str], content: str, temperature=0.5) -> List[str]:
        try:
            result = [self.get_one_hashtag_relevance(tag, content, temperature) for tag in tags]
            return result 
        except Exception as e:
            traceback.print_exc()
            return None
        
    def get_hashtag_distance(self, hashtag_source: str, hashtag_dest: str) -> float:
        try:
            h1_def = self.get_hashtag_definition(hashtag_source)
            h2_def = self.get_hashtag_definition(hashtag_dest)
            if not h1_def or not h2_def:
                return -1
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI agent that analyses hashtags and content to determine the distance between them.\
                                            2 hashtags will be supplied to you along with their definitions in the form of a prompt.\
                                            Return the result as a JSON object with hashtag1 (string), hashtag2 (string) and distance (float, range 0 to 1) \
                                            The distance is how similar the hashtags are. Greater distance means dissimilar, and lower distance means they are alike. \
                                            Determine the relevance of the following hashtag to the content.",
                    },
                    {"role": "user", "content": json.dumps({
                                            "hashtag_1": hashtag_source,
                                            "hashtag_definition_1": h1_def,
                                            "hashtag_2": hashtag_dest,
                                            "hashtag_definition_2": h2_def
                                            }),
                    }
                ],
                response_format={"type": "json_object"},
            )

            result_json = completion.choices[0].message.content
            result = json.loads(result_json)
            return result
        except Exception as e:
            traceback.print_exc()
            return -1

