import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from response import pairs
import re
import random

# Check if NLTK resources are downloaded, and if not, download them
nltk.download('treebank')
if not nltk.corpus.stopwords.fileids():
    nltk.download('stopwords')
if not nltk.corpus.wordnet.fileids():
    nltk.download('wordnet')
if not nltk.corpus.treebank.fileids():
    nltk.download('punkt')

user_info = {
    "name": "",
    "age": "",
    "intrests": "",
}


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
    global user_name

    # Preprocess user input
    tokens = preprocess_input(user_input)

    # Check if the user input matches the "my name is" pattern
    response = check_name_pattern(user_input)
    if response:
        return response

    # Check if the user input matches the "my name is" pattern
    response = check_age_pattern(user_input)
    if response:
        return response

    # Check if the user input matches the "my name is" pattern
    response = check_intrests_pattern(user_input)
    if response:
        return response

    # Check for other specific patterns
    response = match_pattern(user_input, pairs)
    if response:
        return response

    # Fallback response if no specific pattern matches
    response = "I'm sorry, I don't understand. Can you please rephrase?"
    return response





def check_name_pattern(user_input):
    """
    Check if the user input matches the name pattern and provide a response accordingly.
    """
    # Check if the user input matches the "my name is" pattern
    name_match = re.match(r"my name is (.*)", user_input, re.IGNORECASE)
    if name_match:
        user_info["name"] = name_match.group(1)
        response = random.choice(pairs[0][1]).replace("%1", user_info["name"])  # Use the stored name in the response
        return response

    # Check if the user input asks for their name
    if re.match(r"(What is my name|whats my name)\??", user_input, re.IGNORECASE):
        if user_info["name"]:
            response = random.choice(pairs[1][1]).replace("%1", user_info["name"])
        else:
            response = "I don't know your name yet. Can you please tell me?"
        return response


def check_age_pattern(user_input):
    """
    Check if the user input matches the age pattern and provide a response accordingly.
    """
    # Check if the user input matches the "my age is" pattern
    age_match = re.match(r"my age is (\d+)", user_input, re.IGNORECASE)
    if age_match:
        user_info["age"] = age_match.group(1)
        response = random.choice(pairs[2][1]).replace("%1", user_info["age"])
        return response

    # Check if the user input asks for their age
    if re.match(r"(What is my age|whats my age|how old am i)\??", user_input, re.IGNORECASE):
        if user_info["age"]:
            response = random.choice(pairs[3][1]).replace("%1", user_info["age"])
        else:
            response = "I don't know your age yet. Can you please tell me?"
        return response


def check_intrests_pattern(user_input):
    """
    Check if the user input matches the name pattern and provide a response accordingly.
    """
    # Check if the user input matches the "my name is" pattern
    name_match = re.match(r"my intrests are (.*)", user_input, re.IGNORECASE)
    if name_match:
        user_info["intrests"] = name_match.group(1)
        response = random.choice(pairs[4][1]).replace("%1", user_info["name"])  # Use the stored name in the response
        return response

    # Check if the user input asks for their name
    if re.match(r"What are my intrests\??", user_input, re.IGNORECASE):
        if user_info["intrests"]:
            response = random.choice(pairs[5][1]).replace("%1", user_info["name"])
        else:
            response = "I don't know your intrests yet. Can you please tell me?"
        return response
