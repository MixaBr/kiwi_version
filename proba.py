from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import random
from kivy.clock import Clock


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

class MainApp(App):
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
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        self.playing_field_size = 5
        self.first_press = True
        self.first_move = random.randint(1, 2)
        self.bot = Bot(None, None, True)

        self.main_layout = BoxLayout(orientation="vertical")
        self.side_layout = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        field_layout = BoxLayout(orientation="vertical")
        
        self.player1_score_label = Label(text=f"Player 1 score {self.player1.score}")
        self.player2_score_label = Label(text=f"Player 2 score {self.player2.score}")
        self.turn_label = Label(text=f"Turn - Player {self.first_move}")



        # label_score1 = Label(text="Score 1")
        # label_score2 = Label(text="Score 2")

        #self.solution = TextInput(multiline=False, readonly=True, halign="right", font_size=55)



        dropdown = DropDown()

        for index in range(10):

            btn = Button(text='Value %d' % index, size_hint_y=None, height=44)

            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Hello', size_hint_y=1)
 
        mainbutton.bind(on_release=dropdown.open)

        self.side_layout.add_widget(mainbutton)
        self.side_layout.add_widget(self.player1_score_label)
        self.side_layout.add_widget(self.player2_score_label)
        self.side_layout.add_widget(self.turn_label)

        # stack_layout = StackLayout(size_hint_x=0.2, size_hint_y=0.1)
        # stack_layout.add_widget(mainbutton)
        # stack_layout.add_widget(label_pla1)
        # stack_layout.add_widget(label_pla2)
        # side_layout.add_widget(stack_layout)
        # # side_layout.add_widget(label_pla1)
        # # side_layout.add_widget(label_pla2)
        # main_layout.add_widget(side_layout)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))


        buttons = [[str(random.randint(0, 9)) for i in range(0, self.playing_field_size)] for j in range(0, self.playing_field_size)]
#            ["7", "8", "9", "/"],
#            ["4", "5", "6", "*"],
#            ["1", "2", "3", "-"],
#            [".", "0", "C", "+"],

        for x, row in enumerate(buttons):
            h_layout = BoxLayout()

            for y, label in enumerate(row):
                button = MyButton(x, y,
                                  text=label,
                                  background_color =(1, 1, 1, 1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5},)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            field_layout.add_widget(h_layout)
        self.main_layout.add_widget(self.side_layout)
        self.main_layout.add_widget(field_layout)


        self.pain_g()
        if self.dir == 0:
            self.pain_x(random.randint(0, self.playing_field_size - 1))
            self.dir = 1
        else:
            self.pain_y(random.randint(0, self.playing_field_size - 1))
            self.dir = 0
        # print("bot_res")
        # self.bot_res()
        # print("после bot_res")
        if self.first_move == 2:
            self.bot_res()
        return self.main_layout

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

    def bot_res(self):
        print("Бот включен")
#        self.bot = Bot(None, None, True)
        print("Думаю первый ход")
        #        time.sleep(5)
        #        if self.first_move == 2:
        #           self.on_button_press()
        #        self.on_button_press(self.bot.bot_junior(self.find_buttons(self.main_layout)))
        self.bot_next_turn()

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
#            exit()

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
    app = MainApp()
    app.run()
