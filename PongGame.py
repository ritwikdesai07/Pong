import turtle
import time
import csv
import pandas as pd
import joblib
import atexit

# Configuration
DATA_COLLECTION_MODE = False  # Set to True for data collection, False for AI mode
BALL_SPEED_FACTOR = 120
PADDLE_SPEED = 5  # Paddle movement speed per frame

# Setup screen
sc = turtle.Screen()
sc.title("Pong Game - Data Collection Mode" if DATA_COLLECTION_MODE else "Pong Game - AI Mode")
sc.setup(width=800, height=600)
sc.bgcolor("black")
sc.tracer(0)

# Score display
score_left = 0
score_right = 0
score_turtle = turtle.Turtle()
score_turtle.speed(0)
score_turtle.color("white")
score_turtle.penup()
score_turtle.hideturtle()
score_turtle.goto(0, 260)
score_turtle.write(f"{score_left}     {score_right}", align="center", font=("Courier", 24, "bold"))

# Center line
line = turtle.Turtle()
line.speed(0)
line.color("white")
line.penup()
line.goto(0, 300)
line.setheading(270)
line.pendown()
line.forward(600)
line.hideturtle()

# Paddle class
class Paddle(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)  # 100px tall, 20px wide
        self.penup()
        self.goto(x, y)
        self.move_speed = PADDLE_SPEED
        self.moving_up = False
        self.moving_down = False

    def start_move_up(self):
        self.moving_up = True
        self.moving_down = False

    def stop_move_up(self):
        self.moving_up = False

    def start_move_down(self):
        self.moving_down = True
        self.moving_up = False

    def stop_move_down(self):
        self.moving_down = False

    def move(self, delta_time):
        if self.moving_up and self.ycor() < 250:
            new_y = min(250, self.ycor() + self.move_speed * delta_time * 100)
            self.sety(new_y)
        if self.moving_down and self.ycor() > -240:
            new_y = max(-240, self.ycor() - self.move_speed * delta_time * 100)
            self.sety(new_y)

# Ball class
class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.dx = 2
        self.dy = 2
        self.speed_factor = BALL_SPEED_FACTOR

    def move(self, delta_time):
        self.setx(self.xcor() + self.dx * delta_time * self.speed_factor)
        self.sety(self.ycor() + self.dy * delta_time * self.speed_factor)

    def reset_position(self):
        self.goto(0, 0)
        # Randomize initial direction slightly
        import random
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, 2])

# Initialize game objects
right_paddle = Paddle(350, 0)
left_paddle = Paddle(-350, 0)
ball = Ball()

# Key bindings for left paddle (Player 1)
sc.listen()
sc.onkeypress(left_paddle.start_move_up, "w")
sc.onkeyrelease(left_paddle.stop_move_up, "w")
sc.onkeypress(left_paddle.start_move_down, "s")
sc.onkeyrelease(left_paddle.stop_move_down, "s")

# Data collection or AI setup
data_file = None
writer = None

if DATA_COLLECTION_MODE:
    try:
        data_file = open("pong_data.csv", "w", newline="")
        writer = csv.writer(data_file)
        game_header = ['ball_x', 'ball_y', 'ball_dx', 'ball_dy', 'paddle_y', 'action']
        writer.writerow(game_header)
        print("Data collection mode: CSV file created successfully")
        
        # Key bindings for right paddle (human player for data collection)
        sc.onkeypress(right_paddle.start_move_up, "Up")
        sc.onkeyrelease(right_paddle.stop_move_up, "Up")
        sc.onkeypress(right_paddle.start_move_down, "Down")
        sc.onkeyrelease(right_paddle.stop_move_down, "Down")
        
        # Ensure file is closed properly when program exits
        def close_file():
            if data_file and not data_file.closed:
                data_file.close()
                print("Data file closed successfully")
        
        atexit.register(close_file)
        
    except Exception as e:
        print(f"Error creating data file: {e}")
        DATA_COLLECTION_MODE = False

else:
    try:
        ai_model = joblib.load("pong_model.pkl")
        feature_names = ai_model.feature_names_in_
        print("AI mode: Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}. Right paddle will not move.")
        ai_model = None
        feature_names = ['ball_x', 'ball_y', 'ball_dx', 'ball_dy', 'paddle_y']

# Timing for delta-time
last_time = time.time()
data_collection_counter = 0
max_data_points = 100000  # Limit data collection to prevent huge files

# Instructions
print("\n" + "="*50)
if DATA_COLLECTION_MODE:
    print("DATA COLLECTION MODE")
    print("Left paddle: W (up) and S (down)")
    print("Right paddle: Arrow Up and Arrow Down")
    print("Play the game to collect training data!")
    print("Data will be saved to 'pong_data.csv'")
else:
    print("AI PLAYING MODE")
    print("Left paddle: W (up) and S (down)")
    print("Right paddle: Controlled by AI")
print("="*50 + "\n")

try:
    # Main game loop
    while True:
        sc.update()

        # Calculate delta_time
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        # Limit delta_time to prevent large jumps
        delta_time = min(delta_time, 0.05)

        # Move paddles and ball
        left_paddle.move(delta_time)
        right_paddle.move(delta_time)
        ball.move(delta_time)

        # AI or data collection for right paddle
        if DATA_COLLECTION_MODE and writer and data_collection_counter < max_data_points:
            # Determine action based on current paddle movement
            action = 0  # No movement
            if right_paddle.moving_up:
                action = 1  # Moving up
            elif right_paddle.moving_down:
                action = 2  # Moving down
            
            # Collect data every few frames to avoid too much redundant data
            if data_collection_counter % 1 == 0:  # Collect every 3rd frame
                game_state = [
                    round(ball.xcor(), 2), 
                    round(ball.ycor(), 2), 
                    round(ball.dx, 2), 
                    round(ball.dy, 2), 
                    round(right_paddle.ycor(), 2), 
                    action
                ]
                writer.writerow(game_state)
                data_file.flush()  # Ensure data is written immediately
                
                if data_collection_counter % 300 == 0:  # Print progress every 100 data points
                    print(f"Data points collected: {data_collection_counter//3}, "
                          f"Action: {action}, Ball: ({ball.xcor():.1f}, {ball.ycor():.1f}), "
                          f"Paddle Y: {right_paddle.ycor():.1f}")
            
            data_collection_counter += 1
            
            # Stop data collection when limit reached
            if data_collection_counter >= max_data_points:
                print(f"Data collection complete! {max_data_points//3} data points collected.")
        
        elif not DATA_COLLECTION_MODE:
            # AI mode
            right_paddle.moving_up = False
            right_paddle.moving_down = False
            
            if ai_model:
                try:
                    current_state = pd.DataFrame([[
                        ball.xcor(), 
                        ball.ycor(), 
                        ball.dx, 
                        ball.dy, 
                        right_paddle.ycor()
                    ]], columns=feature_names)
                    
                    action = ai_model.predict(current_state)[0]
                    
                    # Ensure action is valid
                    if action not in [0, 1, 2]:
                        action = 0
                    
                    right_paddle.moving_up = (action == 1)
                    right_paddle.moving_down = (action == 2)
                    
                except Exception as e:
                    print(f"AI prediction error: {e}")

        # Ball collision with top and bottom walls
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        # Scoring
        if ball.xcor() > 390:
            score_left += 1
            score_turtle.clear()
            score_turtle.write(f"{score_left}     {score_right}", align="center", font=("Courier", 24, "bold"))
            ball.reset_position()
            time.sleep(0.5)  # Shorter pause
            
        if ball.xcor() < -390:
            score_right += 1
            score_turtle.clear()
            score_turtle.write(f"{score_left}     {score_right}", align="center", font=("Courier", 24, "bold"))
            ball.reset_position()
            time.sleep(0.5)  # Shorter pause

        # Paddle collision detection (improved)
        paddle_width = 20
        paddle_height = 100
        ball_radius = 10
        
        # Right paddle collision
        if (ball.xcor() + ball_radius >= right_paddle.xcor() - paddle_width / 2 and
            ball.xcor() - ball_radius <= right_paddle.xcor() + paddle_width / 2 and
            ball.ycor() + ball_radius >= right_paddle.ycor() - paddle_height / 2 and
            ball.ycor() - ball_radius <= right_paddle.ycor() + paddle_height / 2 and
            ball.dx > 0):  # Ball moving towards paddle
            
            ball.setx(right_paddle.xcor() - paddle_width / 2 - ball_radius)
            ball.dx *= -1
            
        # Left paddle collision
        if (ball.xcor() - ball_radius <= left_paddle.xcor() + paddle_width / 2 and
            ball.xcor() + ball_radius >= left_paddle.xcor() - paddle_width / 2 and
            ball.ycor() + ball_radius >= left_paddle.ycor() - paddle_height / 2 and
            ball.ycor() - ball_radius <= left_paddle.ycor() + paddle_height / 2 and
            ball.dx < 0):  # Ball moving towards paddle
            
            ball.setx(left_paddle.xcor() + paddle_width / 2 + ball_radius)
            ball.dx *= -1

        # Small delay to prevent excessive CPU usage
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nGame stopped by user")
finally:
    # Clean up
    if data_file and not data_file.closed:
        data_file.close()
        print("Data file closed")
    print("Game ended")