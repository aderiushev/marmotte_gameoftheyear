import cocos
from Main import Main
from Game import Game
from cocos.director import director
from cocos.menu import *
from cocos.layer import *

class MainMenu(cocos.scene.Scene):
    def __init__(self):
        MainMenuLayer = MultiplexLayer(GameMenu())
        super(MainMenu, self).__init__(MainMenuLayer)

class GameMenu(Menu):
    def __init__(self):
        # call superclass with the title
        super(GameMenu, self).__init__("myGame")

        #pyglet.font.add_directory('.')

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = 'Arial'
        self.font_title['font_size'] = 21

        self.font_item['font_name'] = 'Arial'
        self.font_item['font_size'] = 15
        self.font_item_selected['font_name'] = 'Arial'
        self.font_item_selected['font_size'] = 17

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []
        items.append(MenuItem('New Game', self.on_new_game))
        items.append(MenuItem('Options', self.on_options))
        items.append(MenuItem('Scores', self.on_scores))
        items.append(MenuItem('Quit', self.on_quit))

        self.create_menu(items, shake(), shake_back())

    def on_new_game(self):
        director.push(Game())

    def on_options(self):
        pass

    def on_scores(self):
        pass

    def on_quit(self):
        pass