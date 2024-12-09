from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import os
import json
from kivymd.uix.list import OneLineListItem, ThreeLineListItem
from kivy.uix.scrollview import ScrollView

TODO_FILE = ""
todos = []

Window.size = (400, 700)
KV = '''
<MainScreen>:
    name: "MainScreen"
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar: 
            title: "passripper"
            elevation: 12
            md_bg_color: app.theme_cls.primary_color 
        
        BoxLayout:
            orientation: "vertical"
            #MDLabel:
                #text: "Passwords"
                #halign: "center"

            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    id: data_table_container

        MDBottomAppBar: 
            height: dp(45)  # Adjusted height for visibility
            MDFabBottomAppBarButton:
                md_bg_color: "#232217"
                icon: "plus"
                on_release: app.file_manager_open()

ScreenManager: 
    MainScreen:
'''

class Todo:
    def __init__(self, title, username, password):
        self.title = title
        self.username = username
        self.password = password

class MainScreen(Screen):
    pass

class PassRipperApp(MDApp):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def build(self):
        self.theme_cls.primary_palette = "Green"   
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Green" 
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        self.exit_manager()
        toast(path)
        global TODO_FILE
        TODO_FILE = str(path)
        self.load_todos()
        self.display_data_table()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def load_todos(self):
        global todos
        todos.clear()
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as file:
                data = json.load(file)
                todos.extend(data.get("passwords", []))

    def display_data_table(self):
        container = self.root.get_screen("MainScreen").ids.data_table_container
        container.clear_widgets()

        if todos:
            row_data = [(str(index + 1), item["title"], item["username"], item["password"]) for index, item in enumerate(todos)]

            data_table = MDDataTable(
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.9, 0.8),
                check=True,
                rows_num=10,
                column_data=[
                    ("no", dp(18)),
                    ("title", dp(30)),
                    ("username", dp(30)),
                    ("password", dp(30))
                ],
                row_data=row_data
            )

            data_table.bind(on_check_press=self.check_press)
            data_table.bind(on_row_press=self.row_press)

            container.add_widget(data_table)

    def check_press(self, instance_table, current_row):
        print("Checked:", instance_table, current_row)

    def row_press(self, instance_table, instance_row):
        print("Row pressed:", instance_table, instance_row)

if __name__ == '__main__':
    PassRipperApp().run()
