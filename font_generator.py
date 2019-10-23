import kivy
import numpy as np
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '330')

kivy.require('1.11.1')

cols = 11
rows = 7

matrix = np.zeros((rows, cols), dtype=np.uint8)
frames = [matrix]
buttons = []
current_frame = 0


class FontConstructor(BoxLayout):

    def __init__(self, **kwargs):
        super(FontConstructor, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.width = 30

        # end of self init

        def load_callback(instance):
            global frames
            frames = list(np.load(filename_input.text + '.npy'))
            restore_button_state()

        def save_callback(instance):
            np.save(filename_input.text, frames)

        def new_file_callback(instance):
            global matrix, frames, buttons, current_frame, cols, rows
            for button_row in buttons:
                for button in button_row:
                    pixels.remove_widget(button)
            cols = int(size_w_input.text)
            rows = int(size_h_input.text)
            pixels.cols = cols
            pixels.rows = rows
            matrix = np.zeros((rows, cols), dtype=np.uint8)
            frames = [matrix]
            buttons = []
            current_frame = 0
            for i in range(0, rows):
                button_row = []
                for j in range(0, cols):
                    btn = ToggleButton()
                    button_row.append(btn)
                    btn.row = i
                    btn.column = j
                    btn.bind(on_press=process_matrix_changes)
                    pixels.add_widget(btn)
                buttons.append(button_row)
            popup.dismiss()

        content = BoxLayout(orientation='vertical')
        size_holder = BoxLayout(orientation='horizontal', size_hint_max_y=40)
        content.add_widget(size_holder)
        size_label_x = Label(text="Columns:")
        size_holder.add_widget(size_label_x)
        size_w_input = TextInput(text=str(cols), multiline=False, size_hint_max_x=40)
        size_holder.add_widget(size_w_input)
        size_label_y = Label(text="Rows:")
        size_holder.add_widget(size_label_y)
        size_h_input = TextInput(text=str(rows), multiline=False, size_hint_max_x=40)
        size_holder.add_widget(size_h_input)

        button_holder = BoxLayout(orientation='horizontal', size_hint_max_y=40)
        content.add_widget(button_holder)
        create_button = Button(text='Create', on_press = new_file_callback)
        button_holder.add_widget(create_button)
        cancel_button = Button(text='Cancel')
        button_holder.add_widget(cancel_button)



        popup = Popup(title='Select size', content=content, size_hint=(0.8, 0.8),
                      auto_dismiss=False)

        menu = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.add_widget(menu)

        new_file_button = Button(text="New file", on_press=popup.open)
        menu.add_widget(new_file_button)

        save_button = Button(text="Save", on_press=save_callback)
        menu.add_widget(save_button)

        load_button = Button(text="Load", on_press=load_callback)
        menu.add_widget(load_button)

        # -----

        pixels = GridLayout()
        pixels.cols = cols
        pixels.rows = rows
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

        def restore_button_state():
            for i in range(0, rows):
                for j in range(0, cols):
                    if frames[current_frame][i][j] == 1:
                        buttons[i][j].state = 'down'
                    else:
                        buttons[i][j].state = 'normal'

        def add_frame(instance):
            # frames.append(np.zeros((7, 11), dtype=np.uint8))
            frames.append(frames[current_frame].copy())
            next_frame(instance)

        def rem_frame(instance):
            frames.pop(current_frame)

        def next_frame(instance):
            global current_frame
            if current_frame != len(frames) - 1:
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
            if instance.state == 'down':
                frames[current_frame][instance.row][instance.column] = 1
            else:
                frames[current_frame][instance.row][instance.column] = 0

        for i in range(0, rows):
            button_row = []
            for j in range(0, cols):
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
