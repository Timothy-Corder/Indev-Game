import os
os.system("")

def escOut():
    print('\033[1m'+'\033[4m'+"\nThese are the escape codes for ANSI\n\n"+'\033[24m')
    print ("'\\033[XXm\', where XX is the chosen color code")

    for i in range(30,37+1):
        print ("\033[%dm%d\t\t\033[%dm%d" % (i,i,i+60,i+60))

    print ("\033[39m\\033[49m - Reset colour")
    print ("\\033[2K - Clear Line")
    print ("\\033[<L>;<C>H OR \\033[<L>;<C>f puts the cursor at line L and column C.")
    print ("\\033[<N>A - Move the cursor up N lines")
    print ("\\033[<N>B - Move the cursor down N lines")
    print ("\\033[<N>C - Move the cursor forward N columns")
    print ("\\033[<N>D - Move the cursor backward N columns")
    print ("\\033[2J - Clear the screen, move to (0,0)")
    print ("\\033[K - Erase to end of line")
    print ("\\033[s - Save cursor position")
    print ("\\033[u - Restore cursor position")
    print (" ")
    print ("\\033[4m  Underline on")
    print ("\\033[24m Underline off")
    print ("\\033[1m  Bold on")
    print ("\\033[21m Bold off\033[0m")
    input("")

def funcOut():
    print(
        "AnsiPie functions:\n\n"
        +color("AnsiPie",6)+"."+color("clear",8)+color("(",7)+color("lines",14)+color(")",7)+" - Clears the specified amount of lines from the output.\n"
        +color("AnsiPie",6)+"."+color("clearall",8)+color("(",7)+color("",14)+color(")",7)+" - Clears the screen's output.\n"
        +color("AnsiPie",6)+"."+color("color",8)+color("(",7)+color("string",14)+","+color("color",14)+color(")",7)+" - Returns the specified string in the chosen color.\n"
        +color("AnsiPie",6)+"."+color("effect",8)+color("(",7)+color("string",14)+","+color("color",14)+color(")",7)+" - Returns the specified string with the chosen effect applied.")
    input("")
    return None

def cancel():
    return None

def help():
    try:
        option=int(input("Welcome to AnsiPie! How can I help? | 1. ANSI Escape Codes | 2. ANSI Module Functions | 3. Cancel | : "))-1
        options = {
            0 : escOut,
            1 : funcOut,
            2 : cancel,
        }
        if(option==2):
            print("I hope I was helpful")
            return None
        options[option]()
        help()
    except:
        help()

def clear(lines: int):
    """Clears the specified amount of lines from the output logs using AnsiPie\n
        \tExample:\n
        \n
        \tprint("1")\n
        \tprint("2")\n
        \tprint("3")\n
        \n
        \tAnsiPie.clear(2)
        \n
        \tWould output:\n
        \n
        \t1"""
    MOVE_CURSOR = '\033[1A'
    CLEAR_LINE = '\033[2K'
    for i in range(lines):
        print(MOVE_CURSOR, end=CLEAR_LINE)

def clearall():
    CLEAR_ALL = '\033[2J'
    print(CLEAR_ALL, end='\r')

def color(input: str, color: int):
    """Returns the provided string colorized with the color specified
    \nColor codes:
     0 - Reset Color
    \n
     1 - Dark Grey    ---    2 - Light Grey\n
     3 - Dark Red     ---    4 - Light Red\n
     5 - Dark Green   ---    6 - Light Green\n
     7 - Dark Yellow  ---    8 - Light Yellow\n
     9 - Dark Blue    ---   10 - Light Blue\n
    11 - Dark Purple  ---   12 - Light Purple\n
    13 - Dark Cyan    ---   14 - Light Cyan\n
    15 - Dark White   ---   16 - Light White\n
    \n
    \tExample:\n
    \tprint(AnsiPie.color("This Color", 12))\n
    \n
    \tWould output the words "This Color" in Light Purple"""
    RESET = '\033[39m'

    DGR = '\033[30m'
    LGR = '\033[90m'

    DR = '\033[31m'
    LR = '\033[91m'
    
    DG = '\033[32m'
    LG = '\033[92m'
    
    DY = '\033[33m'
    LY = '\033[93m'
    
    DB = '\033[34m'
    LB = '\033[94m'
    
    DP = '\033[35m'
    LP = '\033[95m'
    
    DC = '\033[36m'
    LC = '\033[96m'
    
    DW = '\033[37m'
    LW = '\033[97m'
    
    colors = {
        0:RESET,
        1:DGR,
        2:LGR,
        3:DR,
        4:LR,
        5:DG,
        6:LG,
        7:DY,
        8:LY,
        9:DB,
        10:LB,
        11:DP,
        12:LP,
        13:DC,
        14:LC,
        15:DW,
        16:LW,
    }
    output = colors[color]+input+colors[0]
    return output

#for i in range(0, 21):
#    if i != 0:
#        print(str(i) * i)
#    else:
#        print(str(i))
if __name__ == '__main__':
    help()
    clear(1)
#print(color("Red ",4)+"+ "+color("Green ",6)+"+ "+color("White ",16)+"= Christmas!!")
def effect(input: str, format: int):
    """Returns the provided string with the specified effect applied
    \nEffect codes:
     0 - Clear Format\n
    \n
     1 - Underline\n
     2 - Bold
    \n
    \tExample:\n
    \tprint(AnsiPie.effect("BOLD TEXT", 2))\n
    \n
    \tWould output the words "BOLD TEXT" in bold"""
    RESET = '\033[0m'

    UNDRLN = '\033[4m'
    BOLD = '\033[1m'

    formats = {
        0:RESET,
        1:UNDRLN,
        2:BOLD,
    }
    output = formats[format]+input+formats[0]
    return output
def up(amount: int):
    UP = '\033[1A'
    for i in range(amount):
        print(UP,end='\r')
def down(amount: int):
    DOWN = '\033[1B'
    for i in range(amount):
        print(DOWN,end='\r')
def right(amount: int):
    RIGHT = '\033[1C'
    for i in range(amount):
        print(RIGHT,end='\r')
def left(amount: int):
    LEFT = '\033[1D'
    for i in range(amount):
        print(LEFT,end='\r')

def runTest():
    try:
        block = "██"
        print(block*3)
        print(block*3)
        print('\r'+block*3)
        right()
        left()
        up()
        down()
        print(effect(block,0))
        print(effect(block,1))
        print(effect(block,2))
        print(color(block,1))
        print(color(block,2))
        print(color(block,3))
        print(color(block,4))
        print(color(block,5))
        print(color(block,6))
        print(color(block,7))
        print(color(block,8))
        print(color(block,9))
        print(color(block,10))
        print(color(block,11))
        print(color(block,12))
        print(color(block,13))
        print(color(block,14))
        print(color(block,15))
        print(color(block,16))
        clear(5)
        clearall()
        return True
    except:
        return False