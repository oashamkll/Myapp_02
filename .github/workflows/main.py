import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp  # Import dp for density-independent pixels
from kivy.uix.popup import Popup

kivy.require('2.1.0')


class ChatMessage(BoxLayout):
    def __init__(self, message, is_user=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = [dp(5), dp(5)]  # Use dp for padding
        self.size_hint_y = None
        self.height = self.minimum_height # self-sizing height
        self.is_user = is_user


        # Bubble styling (different for user and other messages)
        if self.is_user:
            bubble_color = get_color_from_hex("#a0c4ff")  # Light blue
            text_color = get_color_from_hex("#000000") # Black
            self.bubble = MessageBubble(background_color=bubble_color, corner_radius=[dp(18), dp(18), dp(3), dp(18)])
            self.add_widget(self.bubble)

            self.message_label = Label(text=message, color=text_color,
                                       halign='right', valign='center',
                                       text_size=(Window.width * 0.6, None),
                                       size_hint=(None, None),
                                       padding=[dp(10), dp(10)])
            self.bubble.add_widget(self.message_label)
            self.message_label.bind(texture_size=self.message_label.setter('size')) # self sizing label

        else:  # messages from other users
            bubble_color = get_color_from_hex("#d8f3dc")  # Light green
            text_color = get_color_from_hex("#000000") # Black
            self.bubble = MessageBubble(background_color=bubble_color, corner_radius=[dp(18), dp(18), dp(18), dp(3)])
            self.add_widget(self.bubble)
            self.message_label = Label(text=message, color=text_color,
                                        halign='left', valign='center',
                                        text_size=(Window.width * 0.6, None),
                                        size_hint=(None, None),
                                        padding=[dp(10), dp(10)])
            self.bubble.add_widget(self.message_label)
            self.message_label.bind(texture_size=self.message_label.setter('size')) # self sizing label



class MessageBubble(BoxLayout):
    background_color = kivy.properties.ListProperty([1, 1, 1, 1])  # White default
    corner_radius = kivy.properties.ListProperty([dp(10), dp(10), dp(10), dp(10)])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # Just in case.  Content should manage itself.
        if 'background_color' in kwargs:
            self.background_color = kwargs['background_color']
        if 'corner_radius' in kwargs:
             self.corner_radius = kwargs['corner_radius']


    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            kivy.graphics.Color(*self.background_color)
            kivy.graphics.RoundedRectangle(pos=self.pos, size=self.size, radius=self.corner_radius)


class ChatApp(App):
    def build(self):
        # --- Main Layout ---
        main_layout = BoxLayout(orientation='vertical')
        Window.clearcolor = get_color_from_hex("#f8f9fa")  # Very light gray

        # --- Chat Area (ScrollView) ---
        self.chat_scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))  # Auto-adjust height
        self.chat_scroll.add_widget(self.chat_layout)
        main_layout.add_widget(self.chat_scroll)

        # --- Input Area ---
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), padding=dp(5), spacing = dp(5)) # added spacing

        self.message_input = TextInput(
            hint_text="Enter message...",
            multiline=False,
            size_hint_x=0.8,
            background_color = get_color_from_hex("#ffffff"),
            foreground_color = get_color_from_hex("#343a40")
        )
        self.message_input.bind(on_text_validate=self.send_message) # Send on Enter
        input_layout.add_widget(self.message_input)

        send_button = Button(
            text="Send",
            size_hint_x=0.2,
            background_color=get_color_from_hex("#007bff"),  # Bootstrap primary blue
            color=get_color_from_hex("#ffffff"),
            on_press=self.send_message
        )
        input_layout.add_widget(send_button)

        main_layout.add_widget(input_layout)
        return main_layout

    def send_message(self, instance=None): # added instance=None
        message_text = self.message_input.text.strip()
        if message_text:
            # Add user message
            user_message = ChatMessage(message_text, is_user=True)
            self.chat_layout.add_widget(user_message)
            self.message_input.text = ""  # Clear input

            # Simulate a bot response after adding the user message
            self.simulate_bot_response(message_text)

            # Scroll to the bottom after adding the message
            self.chat_scroll.scroll_y = 0

    def simulate_bot_response(self, user_message):
        # Very simple bot logic.  Replace this with your actual bot.
        if "hello" in user_message.lower():
            bot_response = "Hi there!"
        elif "how are you" in user_message.lower():
            bot_response = "I'm doing well, thanks!"
        elif "bye" in user_message.lower():
            bot_response = "Goodbye!"
        else:
            bot_response = "I didn't understand that."

        bot_message = ChatMessage(bot_response, is_user=False)  # is_user=False for bot messages
        self.chat_layout.add_widget(bot_message)


if __name__ == '__main__':
    ChatApp().run()