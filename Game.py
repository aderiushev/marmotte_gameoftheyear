import cocos
from cocos.actions import *
from Main import Main
from cocos.director import director
from pyglet.window import key as keys
import pyglet
import random

class Hero(cocos.sprite.Sprite):
    baseSpriteAbstractImage = None
    leftStepImage1          = None
    leftStepImage2          = None
    rightStepImage1         = None
    rightStepImage2         = None
    leftJumpImage           = None
    rightJumpImage          = None
    noActionImageLeft       = None
    noActionImageRight      = None

    stepsCompleted          = 0

    move_speed              = 100
    jump_speed              = 400
    gravity                 = -1200
    on_ground               = True
    calcDy                  = False
    moving_direction_vertical = None
    moving_direction_horizontal = None
    wins = 0


    def __init__(self):
        self.baseSpriteAbstractImage = pyglet.resource.image(self.baseSpriteImage)
        
        self.noActionImageLeft = self.baseSpriteAbstractImage.get_region(0, 0, 18, 32)
        self.noActionImageRight = self.noActionImageLeft.get_transform(True)
        
        self.leftStepImage1 = self.baseSpriteAbstractImage.get_region(18, 0, 18, 32)
        self.leftStepImage2 = self.baseSpriteAbstractImage.get_region(36, 0, 18, 32)
        
        self.rightStepImage1 = self.leftStepImage1.get_transform(True)
        self.rightStepImage2 = self.leftStepImage2.get_transform(True)
        
        self.rightjumpImage = self.baseSpriteAbstractImage.get_region(54, 0, 18, 32)
        self.leftStepImage = self.rightjumpImage.get_transform(True)

        super(Hero, self).__init__(self.noActionImageRight)

        self.reload()

    def reload(self):
        free_cells = tilemap.find_cells(free_space='True')
        start_tile = free_cells[random.randint(0, len(free_cells)-1)]
        playerRect = self.get_rect()
        playerRect.midbottom = start_tile.midbottom
        self.position = playerRect.center

class Hero1(Hero):
    baseSpriteImage = 'sprites/hero1_sprite.png'
    CONTROL_LEFT    = keys.LEFT
    CONTROL_RIGHT   = keys.RIGHT
    CONTROL_UP      = keys.UP
    CONTROL_DOWN    = keys.DOWN

    def __init__(self):
        super(Hero1, self).__init__()
        self.do(MoveController())

class Hero2(Hero):
    baseSpriteImage = 'sprites/hero2_sprite.png'
    CONTROL_LEFT    = keys.A
    CONTROL_RIGHT   = keys.D
    CONTROL_UP      = keys.W
    CONTROL_DOWN    = keys.S

    def __init__(self):
        super(Hero2, self).__init__()
        self.do(MoveController())

class Game(cocos.scene.Scene):
    def __init__(self):
        super(Game, self).__init__()
        self.add(GameLayer())

class MoveController(cocos.actions.Action, cocos.tiles.RectMapCollider):
    def start(self):
        self.target.velocity = (0, 0)
        self.keyboard = keys.KeyStateHandler()
        director.window.push_handlers(self.keyboard)

    def step(self, dt):
        global tilemap
        # initial position before step (action, movement)
        dx, dy = self.target.velocity
        # detection of direction (may be LEFT = -1, NOACTION = 0, RIGHT = 1)
        direction = self.keyboard[self.target.CONTROL_RIGHT] - self.keyboard[self.target.CONTROL_LEFT]
        dx = direction * self.target.move_speed * dt
        # setting dy to default gravity value
        dy = dy + self.target.gravity * dt
        # allowing to jump when hero is on ground
        if self.target.on_ground and self.keyboard[self.target.CONTROL_UP]:
            dy = self.target.jump_speed        
        # getting last position settings
        # and creating new ones from it
        last = self.target.get_rect()
        new = last.copy()
        
        new.x += dx
        new.y += dy * dt

        # setting last x position of sprite if it is less or bigger than map size
        if new.x < 0 or new.x + self.target.width > tilemap.px_width:
            new.x = last.x

        """
        small ugly fix.
        did it beacause of:
            on ground dy is always works and has negative value
            so, horizontal moves are blocked by the collision
            here is a fix, setting values to variable calcDy and new.y to and old one
            initialy its False, allows user to go horizontaly
            it changes to True after each horizontal move
            and reverts on each bottom collision in collide_bottom method
        """
        if not self.target.calcDy:
            new.y = last.y
            self.target.calcDy = True


        # calcing new velocity (accelerations, position) to hero
        self.target.velocity = self.collide_map(tilemap, last, new, dy, dx)
        # setting on ground true if old y pos. = new y pos.
        self.target.on_ground = bool(last.y == new.y)

        self.target.position = new.center

        self.setMovementDirections(last, new)
        self.tryDetectWinner()

    def setMovementDirections(self, last, new):
        if new.y > last.y:
            self.target.moving_direction_vertical = self.target.CONTROL_UP
        elif new.y < last.y:
            self.target.moving_direction_vertical = self.target.CONTROL_DOWN
        else:
            self.target.moving_direction_vertical = None

        if new.x > last.x:
            self.target.moving_direction_horizontal = self.target.CONTROL_RIGHT
            self.target.image = self.target.rightStepImage1
        elif new.x < last.x:
            self.target.moving_direction_horizontal = self.target.CONTROL_LEFT
            self.target.image = self.target.leftStepImage1
        else:
            self.target.moving_direction_horizontal = None

    def tryDetectWinner(self):
        x1,y1 = hero1.position
        x2,y2 = hero2.position

        if hero1.moving_direction_vertical == hero1.CONTROL_DOWN:
            if hero1.contains(x2, y2 + 5):
                hero1.wins += 1
                hero2.reload()
        if hero2.moving_direction_vertical == hero2.CONTROL_DOWN:
            if hero2.contains(x1, y1 + 5):
                hero2.wins += 1
                hero1.reload()

    """
        see upper big comment
    """
    def collide_bottom(self, dy):
        self.target.calcDy = False
    
class ScoreLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(ScoreLayer, self).__init__()
        x,y = director.get_window_size()
        self.label = cocos.text.Label('', (0, 0))
        self.add(self.label)
        self.schedule(self.update)

    def update(self, dt):
        text = str(hero1.wins) + ' : ' + str(hero2.wins)
        self.label.element.text = text

class GameLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(GameLayer, self).__init__()
        global tilemap, hero1, hero2
        scroller = cocos.layer.ScrollingManager()
        tilemap = cocos.tiles.load('sprites/map.tmx')['map']

        scroller.add(tilemap)
        self.add(scroller)
        self.add(ScoreLayer())
        hero1 = Hero1()
        hero2 = Hero2()

        self.add(hero1)
        self.add(hero2)
