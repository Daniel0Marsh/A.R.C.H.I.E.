import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import random
import json


# Check if NLTK resources are downloaded, and if not, download them
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Import custom modules
from response import pairs, user_data_patterns

# Custom user input data
user_info = {
    "name": "",
    "age": "",
    "interests": ""
}


def preprocess_input(user_input):
    """
    Preprocesses user input by removing punctuation, tokenizing, removing stopwords, and lemmatizing.
    """
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


def match_pattern(user_input, patterns):
    """
    Matches user input with patterns and returns a random response.
    """
    for pattern, responses in patterns:
        match = re.match(pattern, user_input, re.IGNORECASE)
        if match:
            response = random.choice(responses)
            # Check if the response contains a group
            if "%1" in response:
                return response.replace("%1", match.group(1))
            else:
                return response


def generate_response(user_input):
    """
    Generates a response based on user input.
    """
    # Preprocess user input
    tokens = preprocess_input(user_input)

    # Check if the user input requires custom data patterns
    response = custom_data_pattern(user_input)
    if response:
        return response

    # Check for other specific patterns
    response = match_pattern(user_input, pairs)
    if response:
        return response

    # Fallback response if no specific pattern matches
    response = "I'm sorry, I don't understand. Can you please rephrase?"
    return response


def custom_data_pattern(user_input):
    """
    Checks if the user input matches the custom user data patterns and provides a response accordingly.
    """
    for pattern, data in user_data_patterns.items():
        match = re.match(pattern, user_input, re.IGNORECASE)
        if match:
            return custom_data_pattern_response(data["key"], pairs[data["index"]][1], match, data["save"], data["default_response"])

    # No match found
    return None


def custom_data_pattern_response(key, pattern, match, save, default_response):
    """
    Generates a response based on the provided parameters and user input match.
    """
    if save:
        # Save the user's input data in the user_info JSON file
        data = match.group(1)
        save_user_data('data/user_info.json', key, data)
        user_info_json = load_user_data('data/user_info.json')
        response = random.choice(pattern).replace("%1", user_info_json[key])
    else:
        # Load user information from the JSON file
        user_info_json = load_user_data('data/user_info.json')

        if key != "all" and user_info_json.get(key):
            # Use the stored user data in the response if available
            response = random.choice(pattern).replace("%1", user_info_json[key])
        elif user_info_json.get("name") and user_info_json.get("age") and user_info_json.get("interests"):
            # Use the stored user data in the response if available
            response = random.choice(pattern).replace("%1", user_info_json["name"]).replace("%2", user_info_json["age"]).replace("%3", user_info_json["interests"])
        else:
            # Use the default response if the user data is not available
            response = default_response

    return response


def load_user_data(filename):
    """
    Loads user information from a JSON file.
    """
    with open(filename, 'r') as file:
        return json.load(file)


def save_user_data(filename, key, data):
    """
    Saves the user_info dictionary to a JSON file.
    """
    try:
        # Load the existing data
        with open(filename, "r") as file:
            user_info_json = json.load(file)
    except FileNotFoundError:
        user_info_json = {}

    user_info_json[key] = data

    # Write the updated data to the file
    with open(filename, "w") as file:
        json.dump(user_info_json, file, indent=4)  # Write the entire data with indentation
