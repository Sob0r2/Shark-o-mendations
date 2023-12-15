from functools import partial

from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineRightIconListItem, IRightBodyTouch
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox

from Backend.final_results import Final_Results
from Text import Text

Config.set('kivy', 'exit_on_escape', '0')
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class GenresScreen(MDScreen):
    listcreator = None
    checkbox_states = {}
    i = -1
    def show_dialog(self):
        self.dialog = MDDialog(
            title=Text.genres_text(),
            md_bg_color=(0.8, 0.8, 0.8, 1),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=self.close_dialog,
                ),
            ],
        )
        self.dialog.open()
    def iterate_checkboxes(self,ex):
        self.listcreator = Final_Results()
        if ex != 1: self.i += 1
        for list_item in self.ids.list_items.children:
            right_container = list_item.ids._right_container
            for child in reversed(right_container.children):
                if isinstance(child, RightCheckbox):
                    if ex == 1:
                        if self.listcreator.act_genres[child.id] == 1: child.active = True
                        else: child.active = False
                    else:
                        if self.i % 2 == 0:
                            self.listcreator.act_genres[child.id] = 0
                            child.active = False
                        else:
                            self.listcreator.act_genres[child.id] = 1
                            child.active = True

    def on_enter(self, *args):
        self.listcreator = Final_Results()
        self.ids.list_items.clear_widgets()

        for label in sorted(self.listcreator.genres):
            self.text = label
            list_item = OneLineRightIconListItem(
                text=f"[size=26][font=Graphics/Healing Sunday.ttf][color=#002A55]{label}[/font][/size][/color]",
            )
            checkbox = RightCheckbox(id=label,size_hint=(None, None), size=(48, 48))
            checkbox.active = True
            checkbox.on_release = partial(self.listcreator.click_button, checkbox)
            list_item.ids._right_container.add_widget(checkbox)
            self.ids.list_items.add_widget(list_item)
        self.iterate_checkboxes(1)

    def exit(self):
        self.listcreator.delete_changes()
        self.iterate_checkboxes(1)
        final_screen = self.manager.get_screen("finalscreen")
        final_screen.on_enter()
        self.parent.current = "finalscreen"

    def commit_changes(self):
        if self.listcreator.check_empty():
            self.show_dialog()
        else:
            self.listcreator.return_filtered()
            self.listcreator.on_entry()
            final_screen = self.manager.get_screen("finalscreen")
            final_screen.on_enter()
            self.parent.current = "finalscreen"

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key_down)

    def on_key_down(self, window, key, *largs):
        if key == 27:
            self.parent.current = "finalscreen"
            return True

    def close_dialog(self, value, *args):
        self.dialog.dismiss()
