from __future__ import annotations

import os
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from data_collector.elements.types import BlackLabel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from data_collector.configs import get_scaled_down_app_width, get_true_width
# -------------------------------------------

class FinishLayout(BoxLayout):
    def __init__(self, callback: callable, exit_funct : callable, **kwargs):

        l = 15 * get_true_width() / 1600.
        super(FinishLayout, self).__init__(orientation='vertical', size_hint=(1, 0.085),padding=(0, l, 0, l),**kwargs)

        s = 10 * get_true_width() / 1600.
        upper_finish = BoxLayout(orientation='horizontal', size_hint=(1, 0.3),spacing=s)
        note = BlackLabel(text='Target folder:', size_hint=(0.2, 1), font_size=Window.width * 0.02, bold=True)
        self.target_path_input = TextInput(text=f'{os.getcwd()}',
                                           size_hint=(0.7, 1),
                                           font_size=Window.width * 0.02,
                                           multiline=False)
        buffer = BlackLabel(text='', size_hint=(0.075, 1))
        ok_button = self.get_ok_button()
        ok_button.bind(on_press=callback)

        upper_finish.add_widget(note)
        upper_finish.add_widget(self.target_path_input)
        upper_finish.add_widget(ok_button)
        upper_finish.add_widget(buffer)

        self.exit_funct = exit_funct
        self.default_font_size = Window.width * 0.018
        self.feedback_widget = self.get_feedback_widget(font_size=self.default_font_size)
        self.feedback_popup = self.get_feedback_popup()

        self.add_widget(upper_finish)


    def show(self):
        self.feedback_widget.opacity = 1
        self.feedback_popup.open()

    def get_feedback_popup(self):
        container = BoxLayout(orientation='vertical')
        container.add_widget(self.feedback_widget)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        dismiss_button = Button(text='Dismiss', on_press=lambda instance: self.feedback_popup.dismiss())
        exit_button = Button(text='Exit', on_press=self.exit_funct)
        button_layout.add_widget(dismiss_button)
        button_layout.add_widget(exit_button)

        container.add_widget(button_layout)

        # Create and return the popup
        return Popup(title="Success!", content=container, size_hint=(0.95, 0.25),title_align='center', title_size=self.default_font_size)

    @staticmethod
    def get_feedback_widget(font_size: float) -> Widget:
        return Label(size_hint=(1, 1),
                          opacity=0,
                          font_size=font_size)

    @staticmethod
    def get_ok_button() -> Widget:
        ok_button = Button(text="bundle files", size_hint=(0.2, 1))
        ok_button.background_color = (0, 1, 0, 1)  # (R, G, B, A)
        return ok_button
