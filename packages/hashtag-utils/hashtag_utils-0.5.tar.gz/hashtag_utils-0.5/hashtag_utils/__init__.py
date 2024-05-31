import dotenv
import os
import sys
from .hashtag_utils import HashtagGenerator

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to the Python path
sys.path.append(parent_directory)

dotenv.load_dotenv()
