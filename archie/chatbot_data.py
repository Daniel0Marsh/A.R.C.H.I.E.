import re
import random

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?"]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there"]
    ],
    [
        r"what is your name ?",
        ["I am a chatbot created using Kivy and NLTK."]
    ],
    [
        r"how are you ?",
        ["I'm good. How about you?"]
    ],
    [
        r"sorry (.*)",
        ["Apologies, %1. No problem."]
    ],
    [
        r"quit",
        ["Goodbye! Take care. :)"]
    ],
    [
        r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!"]
    ],
    [
        r"what is your favorite color ?",
        ["I'm a chatbot, I don't have a favorite color."]
    ],
    [
        r"do you like sports ?",
        ["As a chatbot, I don't have preferences, but I can talk about sports if you want."]
    ],
    [
        r"fuck you",
        ["fuck me naa bitch Fuck you!"]
    ]

]

reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
    "am": "are",
    "are": "am",
    "was": "were",
    "were": "was",
    "yourself": "myself",
    "myself": "yourself",
}
