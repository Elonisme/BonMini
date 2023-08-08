"""
This app is created for mini language translation to Chinese.
"""
import toga
import re
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path

def is_chinese_sentence(sentence):
    # 使用正则表达式检查句子中是否包含中文字符
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(chinese_pattern.search(sentence))

def is_english_sentence(sentence):
    # 使用正则表达式检查句子是否只包含英文字母和标点符号
    english_pattern = re.compile(r'^[A-Za-z\s.,!?;]+$')
    return bool(english_pattern.match(sentence))


def mini_init(): 
    resources_folder = Path(__file__).joinpath("../resources").resolve()
    db_filepath = resources_folder.joinpath("mini-han.txt")
    with open(db_filepath,"r",encoding="u8")as f:
        dictionary = f.read().splitlines()
        dictionary = {each.split("\t")[0]:each.split("\t")[1] for each in dictionary}
    return dictionary

def mini2cn(sentence, dictionary):
    if is_english_sentence(sentence):
        sentence = sentence.lower()
        sentence = re.findall(r"[\w']+|[.,!?;]", sentence)
        han = ""
        for word in sentence:
            dic = dictionary.get(word)
            if dic != None:
                han += dic
            else:
                print(word+"单词拼写错误")
                han += "X"
                continue
        return han
    elif is_chinese_sentence(sentence):
        chinese_pattern = re.compile(r'[\u4e00-\u9fa5，。；？！]')
        sentence = chinese_pattern.findall(sentence)
        inverted_dict = {v: k for k, v in dictionary.items()}
        mini = ""
        for word in sentence:
            dic = inverted_dict.get(word)
            if dic != None:
                mini += dic
                mini += " "
            else:
                print(word+"单词拼写错误")
                mini += "误"
                continue
        return mini
    else:
        return "请输入微语或在转义汉语"
        


class BonMini(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "微语or转义汉字: ",
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "转写",
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
            f"转义前: {self.name_input.value}",
            "转义后: "+han
        )



def main():
    return BonMini(app_id="0.0.2", app_name="BonMini")

