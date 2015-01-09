from cocos.director import director

window_width = 20 * 32
window_height = 10 * 32

class Main():
    def __init__(self):
        from MainMenu import MainMenu
        director.init(window_width, window_height, do_not_scale = True)
        director.run(MainMenu())

if __name__ == '__main__': 
    Main()