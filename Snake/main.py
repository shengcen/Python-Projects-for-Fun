## The Snake Game
import turtle as t
from random import *

## WORLD CONFIGURATION
# Window/Main interface
t.title('Snake by Oscar Elva')  # Initial title screen
t.setup(660, 740)
t.tracer(0)
t.update()

# Screen
t.screensize(660, 740, 'white')
blockDist = 20  # Distance between each block

# Status area word
my_count = t.Turtle()
my_count.ht()
my_count.pu()


# Border (up and down)
border_u = t.Turtle()
border_u.ht()
border_u.pu()
border_u.speed(0)
border_d = t.Turtle()
border_d.ht()
border_d.pu()
border_d.speed(0)

# Draw down border
border_d.setposition(250, 200)
border_d.pd()
for i in range(4):
    border_d.right(90)
    border_d.forward(500)

# Draw up border
border_u.setposition(250, 280)
border_u.pd()
border_u.right(90)
border_u.forward(80)
border_u.right(90)
border_u.forward(500)
border_u.right(90)
border_u.forward(80)
border_u.right(90)
border_u.forward(500)


# REUSABLE FUNCTIONS
def getRoundPos(myobj, xy):  # Defined a function to get rounded position, because there was one time
    posX = int(round(myobj.xcor(), 2))  # during testing that a float was off by a very small amount that caused
    posY = int(round(myobj.ycor(), 2))  # a mismatch in the game checks, causing boundary clipping. By defining
    if xy == 'x':
        return posX
    elif xy == 'y':
        return posY
    elif xy == 'xy':
        return (posX, posY)


## Title (Turtle)
# Initialization
title = t.Turtle()
title.pu()
title.ht()
title.color('black')

# render the title
def titleRender():
    title.setpos(-220, 180)
    title.write("Welcome to Oscar's version of Snake ...." \
                , False, align='left', font=('arial', 12, 'bold'))
    title.setpos(-220, 150)
    title.write("You are going to use the 4 arrow keys to move the snake" \
                , False, align='left', font=('arial', 12, 'bold'))
    title.setpos(-220, 130)
    title.write("around the screen, trying to consume all the food items" \
                , False, align='left', font=('arial', 12, 'bold'))
    title.setpos(-220, 110)
    title.write("before the monster catches you ...." \
                , False, align='left', font=('arial', 12, 'bold'))
    title.setpos(-220, 80)
    title.write("Click anywhere on the screen to start the game, have fun !!" \
                , False, align='left', font=('arial', 12, 'bold'))

def myCounterRender():
    my_count.setpos(-220, 220)
    my_count.pd()
    my_count.clear()
    my_count.write('Contact: ' + str(monTailHit) + '      Time: ' + str(round(timeElapsed, 1)) + 's' +
                   '      Motion: Paused',
                   False, align='left', font=('arial', 12, 'bold'))

## Snake (Turtle)
# Initialization
snake = t.Turtle()
snake.pu()
snake.ht()
snake.shape('square')
snake.speed(0)  # Draw speed


## Monster (Turtle)
# Initialization
monster = t.Turtle()
monster.pu()
monster.ht()
monster.speed(0)
monster.color('purple')
monster.shape('square')

# Food (Turtle)
food = t.Turtle()
food.pu()
food.ht()
food.speed(10)


# Directional Headings
up = 90
down = 270
left = 180
right = 0

def turnUp(obj=snake):  # Initially the turn function was going to be used for both snake and monster
    if obj.heading() != down:  # but it was unreliable, so it is only used for the snake now, left it with
        obj.setheading(up)  # obj instead of changing it to snake to keep it modular for future changes.


def turnDown(obj=snake):
    if obj.heading() != up:
        obj.setheading(down)


def turnLeft(obj=snake):
    if obj.heading() != right:
        obj.setheading(left)


def turnRight(obj=snake):
    if obj.heading() != left:
        obj.setheading(right)


def attemptMove():
    global outOfBound
    curX = getRoundPos(snake, 'x')
    curY = getRoundPos(snake, 'y')
    boundary_x = range(-250, 251, 1)
    boundary_y = range(-300, 200 ,1)

    if snake.heading() == up:
        nextY = curY + blockDist  # Used this instead of snake.forward because more reliable, it was often confused because position was returned in floats
        if nextY in boundary_y:  # although since then position is returned rounded with getRoundPos, this movement method is kept for redundancy to ensure
            outOfBound = False  # that the game will function reliably under all conditions.
            snake.sety(nextY)
        else:
            outOfBound = True

    if snake.heading() == down:
        nextY = curY - blockDist
        if nextY in boundary_y:
            snake.sety(nextY)
        else:
            outOfBound = True

    if snake.heading() == left:
        nextX = curX - blockDist
        if nextX in boundary_x:
            outOfBound = False
            snake.setx(nextX)
        else:
            outOfBound = True

    if snake.heading() == right:
        nextX = curX + blockDist
        if nextX in boundary_x:
            outOfBound = False
            snake.setx(nextX)
        else:
            outOfBound = True


# Snake Pause
def pause_unpause():  # Toggle Snake Pause Flag
    global paused
    paused = not paused


# GAME CHECKS
def contactCheck(pos, hazard):
    for i in range(len(hazard)):
        register = hazard[i]
        x = int(register[0])
        y = int(register[1])
        if (x,y) == pos:
            return (hazard[i], i)  # If none is returned there is no collision, otherwise the coordinates are returned, i is returned for indexing the tuple in the list


def statusCheck():  # checks victory condition and updates topbar status
    global snake_status
    global timeElapsed
    global gameOver
    global snakeTailExt
    timeElapsed += (snakeRefSpd / 1000)
    if gameOver or (len(foodPos) == 0 and snakeTailExt):
        gameOver = True
        x,y = snake.position()
        title.setpos(x, y+10)
        if len(foodPos) == 0:
            title.color('red')
            title.write("WINNER !!", False, align='center', font=('arial', 10, 'bold'))
        else:
            title.color('purple')
            title.write("GAME OVER !!", False, align='center', font=('arial', 10, 'bold'))
    else:
        my_count.setpos(-220, 220)
        my_count.pd()
        my_count.clear()
        if paused:
            snake_status = "paused"
        else:
            snake_direction_int = snake.heading()
            if snake_direction_int == 0:
                snake_status = "right"
            elif snake_direction_int == 90:
                snake_status = "up"
            elif snake_direction_int == 180:
                snake_status = "left"
            elif snake_direction_int == 270:
                snake_status = "down"

        my_count.write('Contact: ' + str(monTailHit) + '      Time: ' + str(round(timeElapsed, 1)) + 's' +
                       '      Motion: '+snake_status,
                       False, align='left', font=('arial', 12, 'bold'))

def snakeRender():
    snake.color('white', 'red')  # Sets the snake (turtle) object to display head at start
    snake.st()


def monsterRender():
    monster.st()
    while True:
        posX = int(randint(-12, 12) * blockDist)
        posY = int(randint(-12, 4) * blockDist)  # Max spawn in Y dimension is 4, so it doesn't cover the title
        disX = abs(posX)
        disY = abs(posY)
        if disX >= 9 * blockDist and disY >= 9 * blockDist:  # Breaks the loop when monster spawn is sufficiently far away
            break
    monster.goto(posX, posY)


def foodRender():
    for i in range(9):
        posX = int(randint(-12, 12) * blockDist)
        posY = int(randint(-14, 9) * blockDist)
        food.shape('square')
        food.color('green')
        food.goto(posX, posY)
        stampId = food.stamp()
        foodPos.append([posX, posY, i + 1,
                         stampId])  # The stamp is placed last so that collision detector can be used with different lists
        food.color('white')
        food.goto(posX, posY - 10)  # Centers the number printed on the stamp
        food.write(i + 1, True, align="center", font=("Arial", 12, "bold"))

def drawSnakeDyn():
    global snakeLen
    global snakeTailCount
    global snakeTailPos
    global snakeHeadPos  # Because the head needs to start at someplace, since tailpos requires it in line 149
    global snakeRefSpd
    global snakeTailExt
    if not outOfBound:
        snakeTailPos.append(snakeHeadPos)  # Append (prev)snake head pos as snaketail pos
        snakeHeadPos = (getRoundPos(snake, 'x'), getRoundPos(snake, 'y'))  # Get current position and mark as (new) snake head pos
        collisionHazard = contactCheck(snakeHeadPos, foodPos)

        if collisionHazard != None:  # If there is collision with food (
            snakeLen += collisionHazard[0][2]  # Add length to snake
            food.clearstamp(collisionHazard[0][3])
            del foodPos[collisionHazard[1]]  # Deletes food from the list

        snake.color('blue', 'black')  # Switch to draw snake tail
        snake.stamp()
        snake.color('white', 'red')  # Switch to draw snake head

        if snakeTailCount == snakeLen:
            # Tail fully extended
            snakeTailExt = True
            snakeRefSpd = 250  # moves every 250 ms
            snake.clearstamps(1)
            # delete the end position of the previous tail
            del snakeTailPos[0]
        else:
            # Tail still needs to be further extended
            snakeTailExt = False
            snakeRefSpd = 400  # Snake is slowed to 400ms refresh when tail not fully extended
            snakeTailCount += 1

# Snake (Refresh)
def snakeRefresher():
    global snakeRefSpd
    if not paused and not gameOver:  # Checks if paused or if game is over
        attemptMove()
        drawSnakeDyn()
    t.update()  # design specification asked for manual display update
    statusCheck()
    t.ontimer(snakeRefresher, snakeRefSpd)


# Monster (Refresh)
def monsterRefresher():
    global gameOver
    global monTailHit
    monRefSpd = randint(250, 500)  # Generate random refresh speed (Have tested, it is possible to win with this setting)
    dX = getRoundPos(monster, 'x') - getRoundPos(snake, 'x')
    dY = getRoundPos(monster, 'y') - getRoundPos(snake, 'y')

    if not gameOver:
        if abs(dX) >= abs(dY) :  # if dX > dY, move X, otherwise move Y
            x = getRoundPos(monster, 'x')
            if dX > 0:  # if monster is to right of snake, move left, otherwise move right
                monster.setx(x - blockDist)
            elif dX < 0:
                monster.setx(x + blockDist)

        elif abs(dY) >= abs(dX):
            y = getRoundPos(monster, 'y')
            if dY > 0:  # if monster is above snake, move down, otherwise move up
                monster.sety(y - blockDist)
            elif dY < 0:
                monster.sety(y + blockDist)

    if contactCheck(getRoundPos(monster, 'xy'), [getRoundPos(snake, 'xy')]) != None:  # collision with head
        gameOver = True
    if contactCheck(getRoundPos(monster, 'xy'), snakeTailPos) != None:  # collision with tail
        monTailHit += 1

    t.update()  # design specification asked for manual display update
    t.ontimer(monsterRefresher, monRefSpd)

# Movement Keybinds
t.listen()
t.onkey(turnUp, 'Up')
t.onkey(turnDown, 'Down')
t.onkey(turnLeft, 'Left')
t.onkey(turnRight, 'Right')
t.onkey(pause_unpause, 'space')

# Start Game (On Click)
def clickStart(a, b):
    title.clear()
    t.onscreenclick(None)
    foodRender()
    snakeRefresher()
    monsterRefresher()

if __name__ == "__main__":
    # Snake
    paused = False  # Flag for snake state. (Pause = True, Move = False)
    outOfBound = False
    snakeRefSpd = 250  # Refresh Speed of Snake (move speed)
    snakeLen = 6
    snakeTailCount = 0
    snakeHeadPos = getRoundPos(snake, 'xy')
    snakeTailPos = []  # list of all current positions of snake tail, used for collision detection
    snakeTailExt = False  # Flag for snake tail extension (Fully extended = True)
    # Monster
    monTailHit = 0  # Times that monster collides with snake tail

    # Food
    foodPos = []  # List of all food positions

    # World
    gameOver = False
    timeElapsed = 0

    titleRender()
    myCounterRender()
    snakeRender()
    monsterRender()
    t.update()
    t.onscreenclick(clickStart)
    t.mainloop()
