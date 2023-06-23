import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from response import pairs
import re
import random

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Preprocess user input
def preprocess_input(user_input):
    # Remove punctuation
    user_input = re.sub(r'[^\w\s]', '', user_input)

    # Tokenize the input
    tokens = nltk.word_tokenize(user_input.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

# Function to match patterns and return a random response
def match_pattern(user_input, patterns):
    for pattern, responses in patterns:
        match = re.match(pattern, user_input, re.IGNORECASE)
        if match:
            response = random.choice(responses)
            # Check if the response contains a group
            if "%1" in response:
                return response.replace("%1", match.group(1))
            else:
                return response

# Function to take user input and return bot's response
def generate_response(user_input):
    # Preprocess user input
    tokens = preprocess_input(user_input)

    # Check for specific patterns
    response = match_pattern(user_input, pairs)
    if response:
        return response

    # Fallback response if no specific pattern matches
    response = "I'm sorry, I don't understand. Can you please rephrase?"
    return response
