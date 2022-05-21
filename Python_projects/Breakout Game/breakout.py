"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 1200     # 120 frames per second
NUM_LIVES = 3			    # Number of attempts


def main():
    """
    This is a break out game, user can set the number of bricks, its width, height, numbers; set the size of the ball and paddle
    User can determine how many lives to have by changing the NUM_LIVES in constant
    The game will end when lives = o or all the bricks are removed.
    Enjoy your game!
    """
    graphics = BreakoutGraphics()       # draw the window, ball, bricks, paddle
    lives = NUM_LIVES                   # how many lives user have to play the game
    while True:                         # start the program while user click
        graphics.ball.move(graphics.get_dx(), graphics.get_dy())    # ball move after user click
        if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:  # touch the wall
            graphics.set_dx()
        if graphics.ball.y <= 0:    # when ball touches the roof
            graphics.set_dy()       # bounce
        if graphics.ball_below_window():    # when ball falls under the window
            lives -= 1                      # lives -1
            if lives == 0:                  # when user is out of lives
                break                       # game over
        graphics.remove_brick()             # when ball hits brick, remove the brick
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
