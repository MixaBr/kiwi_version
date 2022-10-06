from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import random
from kivy.clock import Clock
from kivy.uix.settings import SettingsWithSidebar
from kivy.logger import Logger
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox

# We first define our GUI
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Setting'
        on_release: app.open_settings()
    Label:
        id: label
        text: 'Setting'
'''

# This JSON defines entries we want to appear in our App configuration screen
json = '''
[
    {
        "type": "options",
        "title": "Game mode",
        "desc": " ",
        "section": "Game setting",
        "key": "game_mode",
        "options":["Player to Player", "Player to Bot", "OnLine"]
    },
    {
        "type": "options",
        "title": "Field size",
        "desc": " ",
        "section": "Game setting",
        "key": "size",
        "options":["3x3", "5x5", "10x10"]
    }
]'''


class Container(BoxLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.menu()

    # def menu(self):
    #     menu = ActionBar()
    #     aw = ActionView()
    #
    #     menu.add_widget(aw)
    #     #aw.add_widget(bt)
    #     self.add_widget(menu)


class Player:
    def __init__(self, score):
        self.score = score

class MyButton(Button):
   def __init__(self, i, j, **kwargs):
     super().__init__(**kwargs)
     self.i = i
     self.j = j


class MySettingsWithTabbedPanel(SettingsWithSidebar):
    def on_close(self):
        Logger.info("proba.py: MySettingsWithTabbedPanel.on_close")
    def on_config_change(self, config, section, key, value):
        Logger.info(
                "proba.py: MySettingsWithTabbedPanel.on_config_change: "
                "{0}, {1}, {2}, {3}".format(config, section, key, value))
class Bot:
    def __init__(self, i, j, on_bot, **kwargs):
        super().__init__(**kwargs)
        self.i = i
        self.j = j
        self.on_bot = on_bot


    def bot_junior(self, botom):
        print("bot_junior", botom)
        btn = []
        for i in botom:
            if i.background_color == [1, 0, 0, 1]:
                btn.append(i)
        min = btn[0].text
        btn_min = btn[0]
        for i in btn:
            if min > i.text:
                min = i.text
                btn_min = i
        return btn_min

    def bot_midl(self):
        pass

    def bot_super(self):
        pass

class GameApp(App):
    use_kivy_settings = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = None
        self.playing_field_size = None
        self.dir = random.randint(0, 1)
        self.color = [1, 0, 0, 1]
        self.player1 = Player(0)
        self.player2 = Player(0)
        self.first_press = True
        self.first_move = random.randint(1, 2)
        self.number_of_moves = 0
        self.bot = None

    def build(self):

        self.playing_field_size = 25
        self.first_press = True
        self.first_move = random.randint(1, 2)
        self.bot = Bot(None, None, True)

# Создание окна игры, управляющих кнопок
        self.settings_cls = MySettingsWithTabbedPanel
        self.main_layout = Builder.load_string(kv)
        # label = self.main_layout.ids.label
        # label.text = self.config.get('Game setting', 'text')


        self.main_layout = BoxLayout(orientation="vertical")
        self.side_layout = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        self.bootob_btn_layout = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        self.field_layout = BoxLayout(orientation="vertical")

        self.player1_score_label = Label(text=f"Player 1 score {self.player1.score}")
        self.player2_score_label = Label(text=f"Player 2 score {self.player2.score}")
        self.turn_label = Label(text=f"Turn - Player {self.first_move}")
        mainbutton = Button(text='Setting (or press F1)', size_hint_y=1)
        mainbutton.bind(on_release=app.open_settings)
        self.btn_new_game = Button(text='New Game', size_hint_y=1)
        self.btn_new_game.bind(on_release=self.new_game_p)
        self.side_layout.add_widget(mainbutton)
        self.side_layout.add_widget(self.player1_score_label)
        self.side_layout.add_widget(self.player2_score_label)
        self.side_layout.add_widget(self.turn_label)
        self.bootob_btn_layout.add_widget(self.btn_new_game)

        self.num_create_play_fild()
        self.create_field_game()


        self.main_layout.add_widget(self.side_layout)
        self.main_layout.add_widget(self.field_layout)
        self.main_layout.add_widget(self.bootob_btn_layout)

#Эти 3 строчки нужны при изменении размера игрового поля
        # self.del_widget_play_fild()
        # self.playing_field_size = 20
        # self.scr_create_play_fild()




        self.pain_g()
        if self.dir == 0:
            self.pain_x(random.randint(0, self.playing_field_size - 1))
            self.dir = 1
        else:
            self.pain_y(random.randint(0, self.playing_field_size - 1))
            self.dir = 0

        if self.first_move == 2:
            self.bot_next_turn()
        return self.main_layout

    def num_create_play_fild(self):
        self.buttons = [[str(random.randint(0, 9)) for i in range(0, self.playing_field_size)] for j in
                    range(0, self.playing_field_size)]

    def del_widget_play_fild(self):
        self.field_layout.clear_widgets()

    def scr_create_play_fild(self):
        self.num_create_play_fild()
        self.create_field_game()

    def crate_new_play_fild(self):
        self.num_create_play_fild()
        print(self.buttons)
        for element in self.find_buttons(self.field_layout):

            element.text = str(self.buttons[element.i][element.j])



    def new_game_p(self, x=None):

        self.player1.score = 0
        self.player2.score = 0
        self.first_move = random.randint(1, 2)
        self.dir = random.randint(0, 1)
        self.player1_score_label.text = f"Player 1 score {self.player1.score}"
        self.player2_score_label.text = f"Player 2 score {self.player2.score}"
        self.turn_label.text = f"Turn - Player {self.first_move}"

        self.crate_new_play_fild()

        self.dir = random.randint(0, 1)
        self.pain_g()
        if self.dir == 0:
            self.pain_x(random.randint(0, self.playing_field_size - 1))
            self.dir = 1
        else:
            self.pain_y(random.randint(0, self.playing_field_size - 1))
            self.dir = 0

        if self.first_move == 2:
            Clock.schedule_once(lambda _: self.bot_next_turn(), 5)



    def create_field_game(self):
        for x, row in enumerate(self.buttons):
            h_layout = BoxLayout()

            for y, label in enumerate(row):
                button = MyButton(x, y,
                                  text=label,
                                  background_color =(1, 1, 1, 1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5},)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.field_layout.add_widget(h_layout)

    # def build_config(self, config):
    #     """
    #     Set the default values for the configs sections.
    #     """
    #     config.setdefaults('Game setting', {'text': 'Hello', 'font_size': 20})


    def build_settings(self, settings):
        settings.add_json_panel('Game setting', self.config, data=json)


    def on_config_change(self, config, section, key, value):
        Logger.info("proba.py: App.on_config_change: {0}, {1}, {2}, {3}".format(config, section, key, value))

        # if section == "Game setting":
        #     if key == "bool":
        #         print("Key menu", value)
        #     elif key == 'bool':
        #         self.main_layout.ids.label.font_size = float(value)
        # # if section == "Field size":
        #     if key == "text":
        #         self.main_layout.ids.label.text = value
        #     elif key == 'font_size':
        #         self.main_layout.ids.label.font_size = float(value)

    def close_settings(self, settings=None):
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(GameApp, self).close_settings(settings)





    def find_buttons(self, widget):
        buttons = []
        for child in widget.children:

            if isinstance(child, MyButton):
                buttons.append(child)
            else:
                buttons.extend(self.find_buttons(child))
        return buttons

    def find_buttons_all(self, widget):
        buttons = []
        for child in widget.children:
            buttons.append(child)
        return buttons

    def change_button(self, instance):
        ind_x = instance.i
        ind_y = instance.j
#        bottuns_1 = self.find_buttons(self.main_layout)
        self.pain_g()
        if self.dir == 0:
            self.pain_x(ind_x)
            self.dir = 1
        else:
            self.pain_y(ind_y)
            self.dir = 0

    def pain_x(self, x):
        bottuns_1 = self.find_buttons(self.main_layout)
        for elements in bottuns_1:
            if elements.i == x:
                elements.background_color = [1, 0, 0, 1]

    def pain_y(self, y):
        bottuns_1 = self.find_buttons(self.main_layout)
        for elements in bottuns_1:
            if elements.j == y:
                elements.background_color = [1, 0, 0, 1]

    def pain_g(self):

        bottuns_1 = self.find_buttons(self.main_layout)
        for elements in bottuns_1:
            elements.background_color = [1, 1, 1, 1]


    def bot_next_turn(self):
        print("Думаю bot_next_turn")
#        #        return self.bot.bot_junior(self.find_buttons(self.main_layout))
        self.on_button_press(self.bot.bot_junior(self.find_buttons(self.main_layout)))

    def on_button_press(self, instance):
        if instance.text != "X" and instance.background_color == [1, 0, 0, 1]:
            self.number_of_moves += 1
            if self.first_move == 1:
                print("Ход игрока - ", self.first_move)
                self.player1.score += int(instance.text)
                self.first_move = 2
                self.player1_score_label.text = f"Player 1 score {self.player1.score}"
                self.turn_label.text = f"Turn - Player {self.first_move}"
                Clock.schedule_once(lambda _: self.bot_next_turn(), 5)
            else:
                print("Ход бота", self.first_move)
                self.player2.score += int(instance.text)
                self.first_move = 1
                self.player2_score_label.text = f"Player 2 score {self.player2.score}"
                self.turn_label.text = f"Turn - Player {self.first_move}"
#            self.sum += int(instance.text)
            print("score", self.player1.score, self.player2.score)
            instance.text = "X"
            self.change_button(instance)
        if self.game_over():

            print("True")

            winner = None
            if self.player1.score < self.player2.score:
                winner = 'Выиграл Player 1!'
            elif self.player1.score > self.player2.score:
                winner = 'Выиграл Player 2!'
            elif self.player1.score == self.player2.score:
                winner = 'Ооопс!!! Ничья!!!!'
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=50)
            popup.add_widget(victory_label)
            popup.open()


 #           exit()

    def game_over(self):

        a1 = []
        if self.number_of_moves == self.playing_field_size * self.playing_field_size:
            return True
        bottuns_1 = self.find_buttons(self.main_layout)
        for elements in bottuns_1:
            if elements.text == "X" and elements.background_color == [1, 0, 0, 1]:
                a1.append(elements)
        if len(a1) == self.playing_field_size:
            return True


if __name__ == "__main__":
    app = GameApp()
    app.run()
