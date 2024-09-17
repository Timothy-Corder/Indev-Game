from AnsiPie import color, up, down, left, right, clear, clearall
from threading import Thread
from time import sleep
import keyboard

class Level:
    def __init__(self,rawLevel:list[str]) -> None:
        for row in rawLevel:
            if len(row) != len(rawLevel[0]):
                raise ValueError('Line length mismatch in level')
        self._impassables = ['g','p']
        self._levelData = rawLevel
        self.width = len(rawLevel[0])
        self.height = len(rawLevel)
    def getFromCoord(self, x, y):
        if self._levelData[y][x] in ['g', 'p']:
            return self._levelData[y][x]
        else: return ' '
    def getPassable(self, x, y):
        if y > 0 and x > 0:
            return (self._levelData[y][x] not in self._impassables)
        else:
            return False

class Vector2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def rounded(self):
        return Vector2(round(self.x), round(self.y))
    def __add__(self, other):
        new = Vector2(self.x, self.y)
        if type(other) == Vector2:
            new.x += other.x
            new.y += other.y
        elif type(other) == int:
            new.x += other
            new.y += other
        else:
            try:
                iter(other)
                canIter = True
                if len(other) == 2:
                    new.x += other[0]
                    new.y += other[1]
            except:
                if not canIter:
                    raise TypeError(f'Invalid operation: Type {type(other)} can\'t be added to type Vector2')
                else:
                    raise TypeError(f'Invalid operation: Objects added to x or y must be numbers')
        return new
    def __eq__(self, value: object) -> bool:
        if type(value) == Vector2:
            return (self.x == value.x and self.y == value.y)
        else:
            try:
                iter(value)
                if len(value) == 2:
                    return (self.x == value[0] and self.y == value[1])
            except:
                return False
    def __str__(self) -> str:
        return f'Vector2(x={self.x} y={self.y})'

class Player:
    def __init__(self, spawn:tuple = (0,1)) -> None:
        self.pos = Vector2(*spawn)
        self.vel = Vector2(0, 0)
        self.onGround = True
    def jump(self, power:int = 1):
        if self.onGround:
            self.vel.y = -power
    def physicsTick(self, level:Level):
        if self.checkCollision(level, round(self.vel.y), 'y', self.pos):
            self.vel.y = self.castRay(level, round(self.vel.y), 'y', self.pos) - 1
        self.pos.y += round(self.vel.y)
        if self.vel.x >= 0:
            velXToOne = 1
        else:
            velXToOne = -1

        if not self.checkCollision(level, round(self.vel.x + velXToOne), 'x', self.pos):
            self.pos.x += round(self.vel.x)
        if self.getHeight(level) < 0:
            pass
            
    def getHeight(self, level:Level):
        return self.castRay(level, level.height, 'y', self.pos) - 1
    def castRay(self, level:Level, distance, direction, source:Vector2, invert = False):
        if distance < 0:
            negative = -1
        else:
            negative = 1
        match direction:
            case 'x':
                for dist in range(abs(distance)):
                    try:
                        if not level.getPassable(source.rounded().x + (negative * dist), source.rounded().y) or (level.getPassable(source.rounded().x + (negative * dist), source.rounded().y) and invert):
                            return (negative * dist)
                    except IndexError:
                        break
                return 99
            case 'y':
                for dist in range(abs(distance)):
                    try:
                        if not level.getPassable(source.rounded().x, source.rounded().y + (negative * dist)) or (level.getPassable(source.rounded().x, source.rounded().y + (negative * dist)) and invert):
                            return (negative * dist)
                    except IndexError:
                        break
                return 99
    def checkCollision(self, level:Level, distance, direction, source:Vector2):
        ray = self.castRay(level, distance, direction, source)
        match direction:
            case 'x':
                return (ray <= level.width)
            case 'y':
                return (ray <= level.height)
            


class Flag:
    def __init__(self) -> None:
        self.active = True
    def switch(self) -> None:
        self.active = not self.active


def main():
    global broadcasts, tickspeed
    level = parseLevel()
    player = Player((2, 1))
    broadcastsAnnot:dict[str,Flag] = {}
    broadcasts = broadcastsAnnot
    tickspeed = 0.0625

    broadcasts['playing'] = Flag()
    
    renderThread = Thread(target=render,kwargs={'level':level,'player':player,'flag':broadcasts['playing'],'debug':True})
    renderThread.start()
    waitForBroadcast(broadcasts['playing'])
    exit()


def checkControls(player:Player):
    if keyboard.is_pressed('up'):
        player.jump(1.2)
    if keyboard.is_pressed('right'):
        player.vel.x = 1
    elif keyboard.is_pressed('left'):
        player.vel.x = -1
    else:
        player.vel.x = 0

def waitForBroadcast(broadcast:Flag):
    while True:
        if broadcast.active:
            sleep(tickspeed)
        else:
            break

def physics(player:Player, level:Level):
    gravity = 0.2

    if not player.onGround:
        player.vel.y += gravity
    else:
        player.vel.y = min(player.vel.y, 0)
    player.physicsTick(level)
    if player.getHeight(level) == 0:
        player.onGround = True
    else:
        player.onGround = False
    checkControls(player)

    
    if player.pos.y >= level._levelData.__len__():
        broadcasts['playing'].switch()

def parseLevel():
    level:list[str] = []
    with open('level1.txt') as f:
        rawLevel = f.readlines()
        for tile in rawLevel:
            level.append(tile.strip('\n'))
    return Level(level)

def render(level:Level, player:Player, flag:Flag, debug = False):
    while True:
        renderHeight = max(level.height, level.height - player.pos.y)
        # renderHeight = level.height
        clear(renderHeight + 3)
        physics(player, level)
        rendered = ''
        for y in range(level.height):
            for x in range(level.width):
                if player.pos == (x, y):
                    rendered +=  color('██',9)
                else:
                    match level.getFromCoord(x,y):
                        case 'g':
                            rendered += color('██',5)
                        case 'p':
                            rendered += color('██',3)
                        case default:
                            rendered += '  '
            rendered += '\n'
        if debug:
            print(player.vel.y, player.pos)
        print(rendered)
        sleep(tickspeed)
        if not flag.active:
            break

if __name__ == '__main__':
    clearall()
    main()