# Hashtag Utilities 🏷️

An LLM-powered multi-purpose hashtag utilities library written in Python. 

![Hashtag Utilities Hero](https://raw.githubusercontent.com/AdiPat/hashtag_utils/main/images/hero.png)

Hashtags are used on almost every content platform today. This makes it a vital tool for creating & analyzing content. 
This utilities library makes it easy to do things with hashtags. Ideally, this module is intended to be used within a larger system where more specific problems are solved. 

**Feel free to suggest features, ideas and improvements! If you want to contribute, feel free to fork and send a Pull Request. I'm actively working on this project.**

# Features 
- **Hashtag Generator:** Generates hashtags for a content piece.
- **Hashtag Relevance:** Returns the percentage relevance of a hashtag with respect to a content piece.
- **Similar Hashtags:** Generates hash tages similar to the provided ones.
- **Hashtag Distance:** Computes how close two hashtags are.
- **Hashtag Definitions**: Get hashtag definitions. 

# Usage: HashtagUtils API

## Methods

### `get_hashtags(text: str, temperature: float = 1.0, num_tags: int = 5) -> List[str]`

Generates a list of hashtags based on the given text. 

- `text`: The input text to generate hashtags from.
- `temperature`: Controls the randomness of the hashtag generation. Lower values make the output more deterministic. Default is 1.0.
- `num_tags`: The number of hashtags to generate. Default is 5.

### `get_similar_hashtags(hashtags: List[str], temperature: float = 1.0, num_tags: int = 5) -> List[str]`

Generates a list of hashtags that are similar to the given hashtags.

- `hashtags`: The input hashtags to find similar hashtags for.
- `temperature`: Controls the randomness of the hashtag generation. Lower values make the output more deterministic. Default is 1.0.
- `num_tags`: The number of hashtags to generate. Default is 5.

### `get_hashtag_definition(hashtag: str) -> str`

Returns the definition of the given hashtag.

- `hashtag`: The hashtag to get the definition for.

### `get_hashtags_relevance(hashtags: List[str], text: str) -> Dict[str, float]`

Returns a dictionary mapping each hashtag to its relevance to the given text.

- `hashtags`: The hashtags to check the relevance of.
- `text`: The text to check the relevance against.

### `get_hashtag_distance(hashtag1: str, hashtag2: str) -> float`

Returns the semantic distance between two hashtags.

- `hashtag1`: The first hashtag.
- `hashtag2`: The second hashtag.

# Contributors 
- [Aditya Patange (AdiPat)](https://wwww.github.com/AdiPat)