from AnsiPie import color, up, down, left, right, clear, clearall
from threading import Thread
from time import sleep
import keyboard

class Vector2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
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
    def __str__(self) -> str:
        return f'Vector2(x={self.x} y={self.y})'

class Player:
    def __init__(self, spawn:tuple = (0,1)) -> None:
        self.pos = Vector2(*spawn)
        self.vel = Vector2(0, 0)
        self.onGround = True
    def jump(self, power:int = 2):
        if self.onGround:
            self.vel.y += power
    def physicsTick(self, level):
        self.pos.y += self.vel.y
        if (level[self.pos.x + self.vel.x] <= self.pos.y + 1):
            self.pos.x += self.vel.x

class Flag:
    def __init__(self) -> None:
        self.active = True
    def switch(self) -> None:
        self.active = not self.active


def main():
    global broadcasts, tickspeed
    level, highest = parseLevel()
    player = Player((2, 1))
    broadcasts = {}
    tickspeed = 0.125

    broadcasts['playing'] = Flag()
    
    renderThread = Thread(target=render,kwargs={'level':level,'highest':highest,'player':player,'flag':broadcasts['playing']})
    renderThread.start()
    # render(*parseLevel(), playerPos=player.pos)
    waitForBroadcast(broadcasts['playing'])
    exit()


def checkControls(player:Player):
    if keyboard.is_pressed('up'):
        player.jump()
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

def physics(player:Player, level):
    
    player.physicsTick(level)
    checkControls(player)

    player.vel.y -= 1
    if player.pos.y <= level[player.pos.x] and player.vel.y < 0:
        player.vel.y = 0
        player.onGround = True
    else:
        player.onGround = False
    if player.pos.y < level[player.pos.x]:
        player.pos.y = level[player.pos.x]
    if player.pos.y == 0:
        broadcasts['playing'].switch()

def parseLevel():
    level:list[int] = []
    with open('level1.txt') as f:
        for num in f.readline():
            level.append(int(num))
    highest = sorted(level, reverse=True)[0]
    return level, highest

def render(level, highest, player:Player, flag:Flag):
    while True:
        renderHeight = max(highest, player.pos.y)
        clear(renderHeight + 3)
        physics(player, level)
        rendered = ''
        for row in range(renderHeight + 2).__reversed__():
            for column in range(level.__len__()):
                if level[column] > row:
                    rendered += color('██',5)
                elif column == player.pos.x and row == player.pos.y:
                    rendered +=  color('██',9)
                else:
                    rendered += '  '
            rendered += '\n'
        print(rendered)
        sleep(tickspeed)
        if not flag.active:
            break

if __name__ == '__main__':
    clearall()
    main()