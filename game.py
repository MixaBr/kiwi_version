import random
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar


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
        "options":["3x3", "5x5", "10x10", "15x15",  "20x20",  "25x25"]
    },
    {
        "type": "options",
        "title": "Bot power",
        "desc": " ",
        "section": "Game setting",
        "key": "power",
        "options":["Junior", "Midl", "Super"]
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
        Logger.info("game.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
                "game.py: MySettingsWithTabbedPanel.on_config_change: "
                "{0}, {1}, {2}, {3}".format(config, section, key, value))


class Bot:
    def __init__(self, i, j, on_bot, **kwargs):
        super().__init__(**kwargs)
        self.i = i
        self.j = j
        self.on_bot = on_bot

    def bot_junior(self, botom):
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
        self.side_layout = None
        self.bootom_btn_layout = None
        self.buttons = None
        self.btn_new_game = None
        self.field_layout = None
        self.player1_score_label = None
        self.player2_score_label = None
        self.turn_label = None
        self.playing_field_size = None
        self.dir = random.randint(0, 1)
        self.color = [1, 0, 0, 1]
        self.player1 = Player(0)
        self.player2 = Player(0)
        self.first_press = True
        self.first_move = random.randint(1, 2)
        self.number_of_moves = 0
        self.bot = None
        self.game_set = {"Player to Player": 1, "Player to Bot": 2, "OnLine": 3}
        self.game_field = {"3x3": 3, "5x5": 5, "10x10": 10, "15x15": 15,  "20x20": 20,  "25x25": 25}
        self.bot_power = {"Junior": 1, "Midl": 2, "Super": 3}
        self.game_mode = None
        self.size = None
        self.power = None
        self.num_game_mode = None
        self.num_bot_power = None

    def build(self):

        self.config.read("game.ini")
        self.game_mode = self.config.get("Game setting", "game_mode")
        self.size = self.config.get("Game setting", "size")
        self.power = self.config.get("Game setting", "power")

        self.num_game_mode = self.game_set[self.game_mode]
        self.playing_field_size = self.game_field[self.size]
        self.num_bot_power = self.bot_power[self.power]

        self.first_press = True
#        self.first_move = random.randint(1, 2)
        self.bot = Bot(None, None, True)

# Создание окна игры, управляющих кнопок
        self.settings_cls = MySettingsWithTabbedPanel
        self.main_layout = Builder.load_string(kv)

        self.main_layout = BoxLayout(orientation="vertical")
        self.side_layout = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        self.bootom_btn_layout = BoxLayout(orientation="horizontal", size_hint_y=0.1)
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
        self.bootom_btn_layout.add_widget(self.btn_new_game)

        self.num_create_play_fild()
        self.create_field_game()
        self.main_layout.add_widget(self.side_layout)
        self.main_layout.add_widget(self.field_layout)
        self.main_layout.add_widget(self.bootom_btn_layout)

        self.pain_g()
        if self.dir == 0:
            self.pain_x(random.randint(0, self.playing_field_size - 1))
            self.dir = 1
        else:
            self.pain_y(random.randint(0, self.playing_field_size - 1))
            self.dir = 0

        if self.num_game_mode == 1:
            pass
        elif self.num_game_mode == 2:
            self.player2_score_label.text = f"Bot score {self.player2.score}"
            if self.first_move == 2:
                self.turn_label.text = f"Turn - Bot"
                Clock.schedule_once(lambda _: self.bot_next_turn(), 5)

        elif self.num_game_mode == 3:
            pass

        return self.main_layout

    def num_create_play_fild(self):
        self.buttons = [[str(random.randint(0, 9)) for i in range(0, self.playing_field_size)]
                        for j in range(0, self.playing_field_size)]

    def del_widget_play_fild(self):
        self.field_layout.clear_widgets()

    def scr_create_play_fild(self):
        self.num_create_play_fild()
        self.create_field_game()
        self.dir = random.randint(0, 1)
        self.pain_g()
        if self.dir == 0:
            self.pain_x(random.randint(0, self.playing_field_size - 1))
            self.dir = 1
        else:
            self.pain_y(random.randint(0, self.playing_field_size - 1))
            self.dir = 0

    def crate_new_play_fild(self):
        self.num_create_play_fild()
        for element in self.find_buttons(self.field_layout):

            element.text = str(self.buttons[element.i][element.j])

    def new_game_p(self, x=None):

        self.player1.score = 0
        self.player2.score = 0
        self.first_move = random.randint(1, 2)
        self.dir = random.randint(0, 1)
        self.player1_score_label.text = f"Player 1 score {self.player1.score}"
        self.turn_label.text = f"Turn - Player {self.first_move}"
        if self.num_game_mode == 2:
            self.player2_score_label.text = f"Bot score {self.player2.score}"
        else:
            self.player2_score_label.text = f"Player 2 score {self.player2.score}"
        self.crate_new_play_fild()
        self.dir = random.randint(0, 1)
        self.pain_g()
        if self.dir == 0:
            self.pain_x(random.randint(0, self.playing_field_size - 1))
            self.dir = 1
        else:
            self.pain_y(random.randint(0, self.playing_field_size - 1))
            self.dir = 0
        if self.num_game_mode == 2:
            self.player2_score_label.text = f"Bot score {self.player2.score}"
            if self.first_move == 2:
                self.turn_label.text = f"Turn - Bot"
                Clock.schedule_once(lambda _: self.bot_next_turn(), 5)
        else:
            self.player2_score_label.text = f"Player 2 score {self.player2.score}"

#        elif self.num_game_mode == 3:
            pass

    def create_field_game(self):
        for x, row in enumerate(self.buttons):
            h_layout = BoxLayout()

            for y, label in enumerate(row):
                button = MyButton(x, y,
                                  text=label,
                                  background_color=(1, 1, 1, 1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5},)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.field_layout.add_widget(h_layout)

    def build_config(self, config):

        config.setdefaults('Game setting', {'game_mode': 'Player to Bot', 'size': '5x5', 'power':'Junior'})

    def build_settings(self, settings):
        settings.add_json_panel('Game setting', self.config, data=json)

    def on_config_change(self, config, section, key, value):
        Logger.info("game.py: App.on_config_change: {0}, {1}, {2}, {3}".format(config, section, key, value))
        if section == "Game setting":
            if key == "game_mode":
                self.num_game_mode = self.game_set[value]
                if self.num_game_mode == 1:
                    self.new_game_p()
                elif self.num_game_mode == 2:
                    self.new_game_p()
                elif self.num_game_mode == 3:
                    pass
            elif key == "size":
                self.playing_field_size = self.game_field[value]
                self.del_widget_play_fild()
                self.scr_create_play_fild()
                self.new_game_p()

        # # if section == "Field size":
        #     if key == "text":
        #         self.main_layout.ids.label.text = value
        #     elif key == 'font_size':
        # #         self.main_layout.ids.label.font_size = float(value)

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
        self.on_button_press(self.bot.bot_junior(self.find_buttons(self.main_layout)))

    def on_button_press(self, instance):
        if instance.text != "X" and instance.background_color == [1, 0, 0, 1]:
            self.number_of_moves += 1
            if self.first_move == 1:
                self.player1.score += int(instance.text)
                self.first_move = 2
                self.player1_score_label.text = f"Player 1 score {self.player1.score}"

                if self.num_game_mode == 2:
                    self.turn_label.text = f"Turn - Bot"
                    Clock.schedule_once(lambda _: self.bot_next_turn(), 5)
                else:
                    self.turn_label.text = f"Turn - Player {self.first_move}"

#                    self.player2_score_label.text = f"Bot score {self.player2.score}"
            else:
                self.player2.score += int(instance.text)
                self.first_move = 1
                if self.num_game_mode == 2:
                    self.player2_score_label.text = f"Bot score {self.player2.score}"
                    self.turn_label.text = f"Turn - Player {self.first_move}"
                else:
                    self.player2_score_label.text = f"Player 2 score {self.player2.score}"
                    self.turn_label.text = f"Turn - Player {self.first_move}"
            instance.text = "X"
            self.change_button(instance)
        if self.game_over():
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