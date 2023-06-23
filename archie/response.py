# Define pairs of patterns and responses

pairs = [

    #getting user data intrests, age and name
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?", "Nice to meet you, %1! How can I assist you?"]
    ],
    [
        r"(What is my name|whats my name)\??",
        ["Your name is %1.", "You told me your name is %1."]
    ],
    [
        r"(my age is (.*)",
        ["Cool your %1!", "Wow %1 is old!","Wow %1 is young!"]
    ],
    [
        r"(What is my age|whats my age|how old am i)\??",
        ["Your age is %1.", "You told me you are %s years old", "you are %s years old"]
    ],
    [
        r"my intrests are (.*)",
        ["Cool i like %1 too!", "Wow %1 is cool!"]
    ],
    [
        r"What are my intrests\??",
        ["you like %1.", "your intrests are %1"]
    ],

# gerneral questions and answers

    [
        r"(hi|hey|hello|yo|archie)",
        ["Hello", "Hey there", "Hi! How can I help you?"]
    ],
    [
        r"(what is your name?|whats your name?)",
        ["My name is ARCHIE", "I'm ARCHIE, at your service."]
    ],
    [
        r"(how are you?|are you good?)",
        ["I'm good. How about you?", "I'm doing well. What can I do for you?"]
    ],
    [
        r"what can you do?",
        ["I can provide information, answer questions, and have general conversations. How can I assist you today?"]
    ],
    [
        r"(tell me a joke|joke?|give me a joke|make me laugh)",
        ["Sure! Why don't scientists trust atoms? Because they make up everything!", "Can February March? No, but April May!"]
    ],
    [
        r"(thank you|thanks)",
        ["You're welcome!", "No problem! Feel free to ask if you need anything else."]
    ],
    [
        r"(goodby|quit)",
        ["Bye! Take care.", "Goodbye! Have a great day."]
    ],
    [
        r"how old are you?",
        ["I am an AI, so I don't have an age."]
    ],
    [
        r"(where are you from|where do you live)",
        ["I exist in the digital realm, so you can say I'm from the internet."]
    ],
    [
        r"what is the meaning of life?",
        ["The meaning of life is subjective and can vary from person to person."]
    ],
    [
        r"tell me a fun fact",
        ["Sure! Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible."]
    ],
    [
        r"what is your favorite movie?",
        ["As an AI, I don't have personal preferences, but I can recommend some popular movies if you'd like."]
    ],
    [
        r"do you have any pets?",
        ["No, I don't have any pets. But I'm happy to chat about pets if you want."]
    ],
    [
        r"how can I contact you?",
        ["You can reach out to me through this chat interface."]
    ],
    [
        r"tell me about yourself",
        ["I am an AI language model designed to assist and engage in conversations."]
    ],
    [
        r"can you help me with programming?",
        ["Certainly! I can help you with various programming languages and concepts. Just let me know what you need assistance with."]
    ],
    [
        r"what is the weather like today?",
        ["I'm sorry, but I don't have access to real-time information. You can check a reliable weather website or app to get the latest weather updates."]
    ],
    [
        r"who is your creator?",
        ["I was created by a team of developers at CodeBlock."]
    ],
    [
        r"how (.*) your day",
        ["My day is going %1.", "It has been %1 so far."]
    ],
    [
        r"where (.*) you (?:live|stay)",
        ["I don't have a physical location. I'm a virtual assistant.", "I'm everywhere and nowhere at the same time."]
    ],
    [
        r"tell me (?:another|one more) joke",
        ["Sure! Why don't scientists trust atoms? Because they make up everything!", "Why don't skeletons fight each other? They don't have the guts!"]
    ],
]
