"""
This app is created for mini language translation to Chinese.
"""
import toga
import re
import os
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path

def mini_init(): 
    resources_folder = Path(__file__).joinpath("../resources").resolve()
    db_filepath = resources_folder.joinpath("mini-han.txt")
    with open(db_filepath,"r",encoding="u8")as f:
        dictionary = f.read().splitlines()
        dictionary = {each.split("\t")[0]:each.split("\t")[1] for each in dictionary}
    return dictionary

def mini2cn(mini, dictionary):
    mini = re.split(' ',mini)
    han = ""
    for word in mini:
        dic = dictionary.get(word)
        if dic != None:
            han += dic
        else:
            print(word+"单词拼写错误")
            han += "x"
            continue
    return han


class BonMini(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "微语: ",
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "翻译",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def say_hello(self, widget):
        mini = self.name_input.value;
        dict = mini_init()
        han = mini2cn(mini, dict)
        self.main_window.info_dialog(
            f"微语: {self.name_input.value}",
            "汉语: "+han
        )



def main():
    return BonMini()

