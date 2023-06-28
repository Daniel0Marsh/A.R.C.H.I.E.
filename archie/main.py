import json
import os
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from nltk.chat.util import Chat, reflections
from brain import generate_response, load_user_data

Builder.load_file('static/chathistory.kv')
Builder.load_file('static/chatbubble.kv')
Builder.load_file('static/newchat.kv')
Builder.load_file('static/chatscreen.kv')

Window.size = (400, 600)


class ChatBubble(MDBoxLayout):
    '''A widget for the chat bubbles'''

    msg = StringProperty('')
    icon = StringProperty('')
    bubble_color = ObjectProperty()


class ChatHistory(BoxLayout):
    '''A widget for displaying saved chats'''

    title = StringProperty('')


    def open(self, title):
        # Get a reference to the ChatScreen instance
        chat_screen = App.get_running_app().root.get_screen("chatscreen")

        # Check remove new chat widget
        chat_screen.remove_new_chat_widget()

        # Read chat history data from JSON file
        data = load_user_data('data/chat_history.json')

        # Get the chat history for the given title
        chat_messages = data.get(title, [])

        # Iterate over the chat history and add ChatBubble widgets to msglist
        for i, message in enumerate(chat_messages):
            sender = "robot" if i % 2 == 0 else "account"
            chat_screen.add_chat_bubble(message, sender)


    def delete(self, title, chat_history_instance):
        chatlist = self.parent
        chatlist.remove_widget(chat_history_instance)

        # Read chat history data from JSON file
        data = load_user_data('data/chat_history.json')

        # Remove chat history entry with the given title
        del data[title]

        # Write modified chat history data back to the JSON file
        with open('data/chat_history.json', 'w') as json_file:
            json.dump(data, json_file)


class NewChat(MDBoxLayout):
    '''A widget for an empty chat'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.chatlist = self.ids['chatlist']

        # Read chat history data from JSON file
        data = load_user_data('data/chat_history.json')
        chat_history = data.keys()

        for item in chat_history:
            chat_history_bbble = ChatHistory(title=item)
            self.chatlist.add_widget(chat_history_bbble)


    def chat_subject(self, subject):
        user_input = self.parent_screen.ids.user_input
        user_input.text = subject
        self.parent_screen.send_message()


class ChatScreen(Screen):
    '''A screen that displays messages with a user'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        #self.chatbot = Chat(pairs, reflections)
        self.msglist = self.ids['msglist']
        self.new_chat = self.ids['new_chat']
        self.new_chat_widget_instance = None  # Instance of NewChat widget
        self.chat_history = []  # List to store Chat messages
        self.chat_bubbles = []  # List to store ChatBubble instances


    def on_enter(self):
        # Create a new chat widget and add it to the screen
        if not self.new_chat_widget_instance:
            new_chat_widget = NewChat()
            new_chat_widget.parent_screen = self
            self.new_chat.add_widget(new_chat_widget)
            self.new_chat_widget_instance = new_chat_widget


    def remove_new_chat_widget(self):
        # Check if the new chat instance is displayed and remove it
        if self.new_chat_widget_instance:
            self.new_chat.remove_widget(self.new_chat_widget_instance)
            self.new_chat_widget_instance = None


    def send_message(self):
        # Get user input and remove leading/trailing whitespaces
        user_input = self.ids.user_input
        user_text = user_input.text.strip()
        user_input.text = ""

        if user_text:
            # remove new chat widget
            self.remove_new_chat_widget()
            self.add_chat_bubble(user_text, sender="account")
            self.get_chatbot_response(user_text)


    def get_chatbot_response(self, user_text):
        # Add typing indicator bubble
        self.add_chat_bubble( message="Typing...", sender="robot")

        # Schedule displaying chatbot's response after a delay
        Clock.schedule_once(lambda dt: self.display_chatbot_response(user_text), 1.0)


    def display_chatbot_response(self, user_text):
        # Get response from the chatbot
        response = generate_response(user_text)

        # Remove typing indicator bubble
        self.msglist.remove_widget(self.chat_bubbles[-1])
        self.chat_bubbles.pop()
        self.chat_history.pop()

        # Add chatbot's response to chat history
        self.add_chat_bubble(response, sender="robot")


    def add_chat_bubble(self, message, sender):
        # creates the chat bubble and adds to the msglist
        if sender == "account":
            icon = "account"
            bubble_color = self.theme_cls.primary_color
        else:
            icon = "robot"
            bubble_color = self.theme_cls.accent_color

        #temparary handle for None message...
        if message == None:
            message = "Sorry I dont understand :("

        if message:
            # Add user's message to chat history
            chat_bubble = ChatBubble(
                msg=message,
                icon=icon,
                bubble_color=bubble_color
            )
            self.msglist.add_widget(chat_bubble)
            self.chat_history.append(message)
            self.chat_bubbles.append(chat_bubble)


    def save_chat(self, title=None):
        # Saving chat history
        messages = self.chat_history

        try:
            # Load the existing data
            with open("data/chat_history.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        if title:
            # If title exists, replace it with new data
            existing_data[title] = messages
        else:
            # Use the first element in messages as the key
            title = messages[0]
            existing_data[title] = messages

            # Write the updated data to the file
            with open("data/chat_history.json", "w") as file:
                json.dump(existing_data, file, indent=4)  # Write the entire data with indentation

            # Clear chat history
            self.chat_history = []


    def home(self):
        # saves and Clears chat history change screens to home
        self.save_chat()
        self.delete_chat()


    def delete_chat(self):
        # Clear chat history
        for chat_bubble in self.chat_bubbles:
            self.msglist.remove_widget(chat_bubble)
        self.chat_bubbles = []

        # Add new chat widget
        self.on_enter()


class MyApp(MDApp):
    def build(self):
        '''Initialize the application and returns the root widget'''
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Green'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.4
        self.title = "A.R.C.H.I.E."
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(ChatScreen(name='chatscreen'))
        return screen_manager

    def switch_theme_style(self):
        self.theme_cls.primary_palette = (
            "Orange" if self.theme_cls.primary_palette == "Blue" else "Blue"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )


if __name__ == '__main__':
    MyApp().run()
