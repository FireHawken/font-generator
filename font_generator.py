import kivy
import numpy as np
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '330')

kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

matrix = np.zeros((7, 11), dtype=np.uint8)
frames = [matrix]
buttons = []
current_frame = 0


class FontConstructor(BoxLayout):

    def __init__(self, **kwargs):
        super(FontConstructor, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.width = 30

        pixels = GridLayout()
        pixels.cols = 11
        pixels.rows = 7
        pixels.width = pixels.cols * 2
        self.add_widget(pixels)

        settings = BoxLayout()
        settings.orientation = 'horizontal'
        settings.size_hint = (1, 0.1)
        self.add_widget(settings)

        filename_label = Label()
        filename_label.text = "File"
        settings.add_widget(filename_label)

        filename_input = TextInput(text='matrix', multiline=False)
        settings.add_widget(filename_input)

        size_label = Label(text="Size")
        settings.add_widget(size_label)

        size_w_input = TextInput(text='11', multiline=False, size_hint_max_x=40)
        settings.add_widget(size_w_input)
        size_h_input = TextInput(text='7', multiline=False, size_hint_max_x=40)
        settings.add_widget(size_h_input)

        def restore_button_state():
            for i in range(0, 7):
                for j in range(0, 11):
                    if frames[current_frame][i][j] == 1:
                        buttons[i][j].state = 'down'
                    else:
                        buttons[i][j].state = 'normal'

        def add_frame(instance):
            frames.append(np.zeros((7, 11), dtype=np.uint8))
            next_frame(instance)

        def rem_frame(instance):
            frames.pop(current_frame)

        def next_frame(instance):
            global current_frame
            if current_frame != len(frames)-1:
                current_frame += 1
                frame_label.text = f'Frame: {current_frame}'
                restore_button_state()

        def prev_frame(instance):
            global current_frame
            if current_frame != 0:
                current_frame -= 1
                frame_label.text = f'Frame: {current_frame}'
                restore_button_state()

        prev_frame_button = Button(text='<<', size_hint_max_x=30, on_press=prev_frame)
        settings.add_widget(prev_frame_button)
        next_frame_button = Button(text='>>', size_hint_max_x=30, on_press=next_frame)
        settings.add_widget(next_frame_button)
        add_frame_button = Button(text='+', size_hint_max_x=30, on_press=add_frame)
        settings.add_widget(add_frame_button)
        remove_frame_button = Button(text='-', size_hint_max_x=30, on_press=rem_frame)
        settings.add_widget(remove_frame_button)

        def process_matrix_changes(instance):
            print(f'The button on  {instance.column}, {instance.row} is being pressed')
            if instance.state == 'down':
                frames[current_frame][instance.row][instance.column] = 1
            else:
                frames[current_frame][instance.row][instance.column] = 0

        def save_callback(instance):
            print(frames)
            np.save(filename_input.text, frames)

        save = Button()
        save.text = "Save"
        save.bind(on_press=save_callback)

        settings.add_widget(save)

        for i in range(0, 7):
            button_row = []
            for j in range(0, 11):
                btn = ToggleButton()
                button_row.append(btn)
                btn.row = i
                btn.column = j
                btn.bind(on_press=process_matrix_changes)
                pixels.add_widget(btn)
            buttons.append(button_row)

        # ----

        def print_debug(instance):
            print(np.asarray(frames))
            print("------------------")

        status = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.add_widget(status)

        debug_button = Button(text='?', size_hint_max_x=30, on_press=print_debug)
        status.add_widget(debug_button)

        frame_label = Label(text=f'Frame: {current_frame}')
        status.add_widget(frame_label)


class FontConstructorApp(App):

    def build(self):
        return FontConstructor()


if __name__ == '__main__':
    FontConstructorApp().run()
