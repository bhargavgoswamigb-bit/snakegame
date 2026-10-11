import turtle
import time
import random

# -------------------------------
# Game Settings
# -------------------------------
delay = 0.1
score = 0
highest_score = 0
bodies = []
paused = False
game_over = False

# -------------------------------
# Main Screen
# -------------------------------
main_screen = turtle.Screen()
main_screen.title("Snake Game")
main_screen.bgcolor("lightblue")
main_screen.setup(width=600, height=600)
main_screen.tracer(0)

# -------------------------------
# Snake Head
# -------------------------------
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# -------------------------------
# Food
# -------------------------------
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.penup()
food.goto(0, 100)

# -------------------------------
# Scoreboard
# -------------------------------
sb = turtle.Turtle()
sb.speed(0)
sb.color("black")
sb.penup()
sb.hideturtle()
sb.goto(0, 260)


def update_scoreboard():
    sb.clear()
    sb.write(
        f"Score: {score}  |  Highest Score: {highest_score}",
        align="center",
        font=("Arial", 16, "bold")
    )


update_scoreboard()

# -------------------------------
# Movement Functions
# -------------------------------
def moveup():
    if head.direction != "down":
        head.direction = "up"


def movedown():
    if head.direction != "up":
        head.direction = "down"


def moveleft():
    if head.direction != "right":
        head.direction = "left"


def moveright():
    if head.direction != "left":
        head.direction = "right"


def toggle_pause():
    global paused

    if not game_over:
        paused = not paused


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)

    elif head.direction == "down":
        head.sety(head.ycor() - 20)

    elif head.direction == "left":
        head.setx(head.xcor() - 20)

    elif head.direction == "right":
        head.setx(head.xcor() + 20)


# -------------------------------
# Random Food Position
# -------------------------------
def place_food():
    x = random.randint(-13, 13) * 20
    y = random.randint(-12, 12) * 20

    # Avoid placing food on the snake.
    while True:
        position = (x, y)

        occupied = (
            position == (int(head.xcor()), int(head.ycor()))
            or any(
                (int(body.xcor()), int(body.ycor())) == position
                for body in bodies
            )
        )

        if not occupied:
            break

        x = random.randint(-13, 13) * 20
        y = random.randint(-12, 12) * 20

    food.goto(x, y)


# -------------------------------
# Reset Game
# -------------------------------
def reset_game():
    global score, delay, game_over

    time.sleep(1)

    head.goto(0, 0)
    head.direction = "stop"

    for body in bodies:
        body.hideturtle()

    bodies.clear()

    score = 0
    delay = 0.1
    game_over = False

    food.goto(0, 100)

    update_scoreboard()


# -------------------------------
# Keyboard Controls
# -------------------------------
main_screen.listen()

main_screen.onkeypress(moveup, "Up")
main_screen.onkeypress(movedown, "Down")
main_screen.onkeypress(moveleft, "Left")
main_screen.onkeypress(moveright, "Right")
main_screen.onkeypress(toggle_pause, "space")

# Also support WASD controls.
main_screen.onkeypress(moveup, "w")
main_screen.onkeypress(movedown, "s")
main_screen.onkeypress(moveleft, "a")
main_screen.onkeypress(moveright, "d")

# -------------------------------
# Main Game Loop
# -------------------------------
try:
    while True:
        main_screen.update()

        if paused:
            time.sleep(0.05)
            continue

        # Move snake body segments.
        for i in range(len(bodies) - 1, 0, -1):
            x = bodies[i - 1].xcor()
            y = bodies[i - 1].ycor()
            bodies[i].goto(x, y)

        # Move first body segment to the old head position.
        if bodies:
            bodies[0].goto(head.xcor(), head.ycor())

        # Move the snake head.
        move()

        # ---------------------------
        # Wall Collision
        # ---------------------------
        if (
            head.xcor() > 280
            or head.xcor() < -280
            or head.ycor() > 280
            or head.ycor() < -280
        ):
            game_over = True

        # ---------------------------
        # Snake Body Collision
        # ---------------------------
        for body in bodies:
            if body.distance(head) < 20:
                game_over = True
                break

        # ---------------------------
        # Game Over
        # ---------------------------
        if game_over:
            sb.clear()
            sb.goto(0, 0)
            sb.write(
                "GAME OVER!\nRestarting...",
                align="center",
                font=("Arial", 22, "bold")
            )

            main_screen.update()
            reset_game()
            continue

        # ---------------------------
        # Food Collision
        # ---------------------------
        if head.distance(food) < 20:
            place_food()

            # Create a new body segment.
            body = turtle.Turtle()
            body.speed(0)
            body.shape("square")
            body.color("darkred")
            body.penup()
            body.goto(head.xcor(), head.ycor())

            bodies.append(body)

            # Increase score.
            score += 10

            if score > highest_score:
                highest_score = score

            # Increase speed gradually.
            delay = max(0.04, delay - 0.002)

            update_scoreboard()

        time.sleep(delay)

except turtle.Terminator:
    pass
