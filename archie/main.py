import json
import os
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
from chatbot_data import pairs

Builder.load_file('chathistory.kv')
Builder.load_file('chatbubble.kv')
Builder.load_file('newchat.kv')
Builder.load_file('chat.kv')

Window.size = (400, 600)


class ChatBubble(MDBoxLayout):
    '''A widget for the chat bubbles'''

    msg = StringProperty('')
    icon = StringProperty('')
    bubble_color = ObjectProperty()


class ChatHistory(MDBoxLayout):
    '''a widget for displaying saved chats'''

    title = StringProperty('')

    def open(self, title):
        # TODO: Implement open functionality
        print(title)

    def delete(self, title, chat_history_instance):
        chatlist = self.parent
        chatlist.remove_widget(chat_history_instance)

        with open('chat_history.json', 'r') as json_file:
            data = json.load(json_file)

        if title in data:
            del data[title]

        with open('chat_history.json', 'w') as json_file:
            json.dump(data, json_file)


class NewChat(MDBoxLayout):
    '''A widget for an empty chat'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.chatlist = self.ids['chatlist']

        with open('chat_history.json') as json_file:
            data = json.load(json_file)
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
        self.chatbot = Chat(pairs, reflections)
        self.msglist = self.ids['msglist']
        self.chat_bubbles = []  # List to store ChatBubble instances
        self.new_chat = self.ids['new_chat']
        self.new_chat_widget_instance = None  # Instance of NewChat widget
        self.chat_history = []

    def on_enter(self):
        # Create a new chat widget and add it to the screen
        new_chat_widget = NewChat()
        new_chat_widget.parent_screen = self
        self.new_chat.add_widget(new_chat_widget)
        self.new_chat_widget_instance = new_chat_widget

    def send_message(self):
        # Get user input and remove leading/trailing whitespaces
        user_input = self.ids.user_input
        user_text = user_input.text.strip()

        self.chat_maintenance(user_input)

        # Check if the new chat instance is displayed and remove it
        if self.new_chat_widget_instance:
            self.new_chat.remove_widget(self.new_chat_widget_instance)
            self.new_chat_widget_instance = None

        if user_text:
            # Add user's message to chat history
            user_bubble = ChatBubble(
                msg=user_text,
                icon="account",
                bubble_color=self.theme_cls.primary_color
            )

            self.chat_history.append(user_text)

            self.msglist.add_widget(user_bubble)
            self.chat_bubbles.append(user_bubble)
            self.get_chatbot_response(user_text)

    def get_chatbot_response(self, user_text):
        # Add typing indicator bubble
        typing_bubble = ChatBubble(
            msg="Typing...",
            icon="robot",
            bubble_color=self.theme_cls.accent_color
        )
        self.msglist.add_widget(typing_bubble)
        self.chat_bubbles.append(typing_bubble)

        # Schedule displaying chatbot's response after a delay
        Clock.schedule_once(lambda dt: self.display_chatbot_response(user_text), 1.0)

    def display_chatbot_response(self, user_text):
        # Get response from the chatbot
        response = self.chatbot.respond(user_text)
        if response is None:
            response = "Sorry, I don't understand :("

        # Remove typing indicator bubble
        self.msglist.remove_widget(self.chat_bubbles[-1])
        self.chat_bubbles.pop()

        # Add chatbot's response to chat history
        bot_bubble = ChatBubble(
            msg=response,
            icon="robot",
            bubble_color=self.theme_cls.accent_color
        )

        self.chat_history.append(response)

        self.msglist.add_widget(bot_bubble)
        self.chat_bubbles.append(bot_bubble)

    def save_chat(self, title=None):
        # saving chat history
        messages = self.chat_history

        if messages:
            if title:
                chat = {title: messages}
            else:
                title = self.chat_history[0]

            file_path = "chat_history.json"

            try:
                # Load the existing data
                with open(file_path, "r") as file:
                    existing_data = json.load(file)
            except FileNotFoundError:
                existing_data = {}

            # Extend existing data or create a new entry
            existing_data.setdefault(title, []).extend(messages)

            # Write the updated data to the file
            with open(file_path, "w") as file:
                json.dump(existing_data, file, indent=4)  # Write the entire data with indentation

            # Clear chat history
            self.chat_history = []

    def chat_maintenance(self, user_input):
        # Clear user input
        user_input.text = ""

    def home(self):
        # Clear chat history or perform any desired action
        self.save_chat()
        self.delete_chat()

    def delete_chat(self):
        # Clear chat history or perform any desired action
        for chat_bubble in self.chat_bubbles:
            self.msglist.remove_widget(chat_bubble)
        self.chat_bubbles = []

        # Add new chat widget if it's not already displayed
        if not self.new_chat_widget_instance:
            new_chat_widget = NewChat()
            new_chat_widget.parent_screen = self
            self.new_chat.add_widget(new_chat_widget)
            self.new_chat_widget_instance = new_chat_widget


class MyApp(MDApp):
    def build(self):
        '''Initialize the application and return the root widget'''
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Green'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.4
        self.title = "A.R.C.H.I.E."
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(ChatScreen(name='chat'))
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
