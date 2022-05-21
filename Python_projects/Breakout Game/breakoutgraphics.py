"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):
        # attributes
        self.paddle_offset = paddle_offset
        self.ball_radius = ball_radius
        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)
        # Create a paddle
        self.paddle = GRect(width=paddle_width, height=paddle_height)
        self.paddle.filled = True
        self.paddle.color = 'black'
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle, (self.window_width-paddle_width)/2, self.window_height-paddle_offset)
        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.window.add(self.ball, (self.window_width-self.ball_radius)/2, (self.window_height-self.ball_radius)/2)
        # Default initial velocity for the ball
        self.__dy = 0
        self.__dx = 0
        # Initialize our mouse listeners
        onmousemoved(self.paddle_connect)
        self._started = False
        onmouseclicked(self.handle_click)
        # Draw bricks
        for r in range(BRICK_ROWS):
            for c in range(BRICK_COLS):
                self.bricksrc = GRect(brick_width, brick_height)
                self.bricksrc.filled = True
                if r < 2:
                    self.bricksrc.fill_color = 'red'
                    self.bricksrc.color = 'red'
                elif r < 4:
                    self.bricksrc.fill_color = 'orange'
                    self.bricksrc.color = 'orange'
                elif r < 6:
                    self.bricksrc.fill_color = 'yellow'
                    self.bricksrc.color = 'yellow'
                elif r < 8:
                    self.bricksrc.fill_color = 'green'
                    self.bricksrc.color = 'green'
                else:
                    self.bricksrc.fill_color = 'blue'
                    self.bricksrc.color = 'blue'
                self.window.add(self.bricksrc, c*(BRICK_WIDTH+BRICK_SPACING), BRICK_OFFSET+r*(BRICK_HEIGHT+BRICK_SPACING))

    def paddle_connect(self, mouse):           # connect the paddle with mouse to move horizontally
        if self.paddle.width/2 <= mouse.x <= self.window.width-self.paddle.width/2:
            self.paddle.x = mouse.x-self.paddle.width/2
            self.paddle.y = self.window_height-self.paddle_offset

    def handle_click(self, event):             # start the program
        if not self._started:
            self._started = True                # tell the program is started
            self.set_ball_velocity()            # give the ball velocity

    def set_ball_velocity(self):                # define the velocity of the ball
        self.__dy = INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -1 * self.__dx

    def ball_below_window(self):                 # to check if the ball is below the window
        if self.ball.y + self.ball.height >= self.window_height:
            self.reset_ball()                   # when the ball is below the window, reset the position
            self._started = False               # and turn _start = False
            return True                         # when user ask if ball_below_window, return Ture
        else:                                   # is ball is not below the window, return False
            return False

    def reset_ball(self):                       # reset ball position in the middle of the window
        self.ball.x = (self.window_width-self.ball_radius)/2
        self.ball.y = (self.window_height-self.ball_radius)/2
        self.__dy = 0
        self.__dx = 0

    def remove_brick(self):                     # remove brick when the ball touched
        left_upper = self.window.get_object_at(self.ball.x, self.ball.y)
        right_upper = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        left_lower = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        right_lower = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        if left_upper is not None:              # if left_upper of the ball touched the brick, remove it and bounce
            self.__dy = self.__dy*(-1)
            if left_upper is not self.paddle:
                self.window.remove(self.window.get_object_at(self.ball.x, self.ball.y))
        elif right_upper is not None:           # if right_upper of the ball touched the brick, remove it and bounce
            self.__dy = self.__dy*(-1)
            if right_upper is not self.paddle:
                self.window.remove(self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y))
        elif left_lower is not None:            # if left_lower of the ball touched the brick, remove it and bounce
            self.__dy = self.__dy*(-1)
            if left_lower is not self.paddle:
                self.window.remove(self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height))
        elif right_lower is not None:           # if right_lower of the ball touched the brick, remove it and bounce
            self.__dy = self.__dy*(-1)
            if right_lower is not self.paddle:
                self.window.remove(self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height))

    def get_dx(self):           # since __dx is private, need getter to use in break.py
        return self.__dx

    def get_dy(self):           # since __dy is private, need getter to use in break.py
        return self.__dy

    def set_dx(self):           # since __dx is private, need setter to change the value in break.py
        self.__dx = self.__dx*(-1)

    def set_dy(self):           # since __dy is private, need setter to change the value in break.py
        self.__dy = self.__dy*(-1)









