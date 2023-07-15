#!/usr/bin/env python3

import pynput
from os import system
from time import sleep
import signal
from ball import *
import cursor
from sys import argv
from sys import stdout


# Prevent user input from being displayed on the terminal
def hide_stdin():
    system("stty -echo")
    cursor.hide()

# Allow user input to be displayed on the terminal
def show_stdin():
    system("stty echo")
    cursor.show()

VERSION = "0.1.1"

def clear_terminal():
    # Clear terminal
    print("\x1b[1;1H\x1b[2J", end="")

def end(code = 0):
    # Show the cursor and exit
    show_stdin()
    print_at(0, height, "\n\nBye!\n\n")

    quit(code)

def ctrl_c(*args, **kwargs):
    end(0)

signal.signal(signal.SIGINT, ctrl_c)

def main():
    speed = 5
    gravity = 50
    increase = False
    auto = False
    restitution = 0.8
    air_frictions = True
    ball_count = 1
    show_paths = False
    hearts = False


    argv.pop(0)
    while len(argv) > 0:
        arg = argv.pop(0)
        match arg:
            case "-h" | "--help":
                # If -h is used, print help message and exit
                bar = f"{PURPLE}━━━━━━━━━━━━━━━━━{RESET}"
                print()
                print(f"{BG_PURPLE} Bouncing Balls {RESET}")
                print(bar)
                print(f"Author: {PURPLE}SkwalExe <Leopold Koprivnik>{RESET}")
                print(f"Github: {PURPLE}https://github.com/SkwalExe{RESET}")
                print(bar)
                print(f"A simple program making balls bounce in your terminal.")
                print(bar)
                print(f"Options:")
                print(f"\t{PURPLE}-h, --help : {YELLOW}Show this help message and exit")
                print(f"\t{PURPLE}-v, --version : {YELLOW}Show the version number and exit")
                print(f"\t{PURPLE}-c, --cursor : {YELLOW}Using this option will make the cursor and stdin visible again and exit")
                print(f"\t{PURPLE}-s, --speed : {YELLOW}Set the speed of the ball from 1 to 10 (default: {speed})")
                print(f"\t{PURPLE}-g, --gravity : {YELLOW}Set the gravity of the ball from 0 to 100 (default: {gravity})")
                print(f"\t{PURPLE}-i, --increase : {YELLOW}When using the arrow keys, increase the speed in the direction of the arrow instead of setting it to a predefined value (default: {increase})")
                print(f"\t{PURPLE}-a, --auto : {YELLOW}Automatically make the ball move")
                print(f"\t{PURPLE}-n, --no-air-frictions : {YELLOW}Don't apply air frictions to the ball")
                print(f"\t{PURPLE}-r, --restitution : {YELLOW}Set the restitution of the ball from 0 to 10 (default: {restitution})")
                print(f"\t{PURPLE}-b, --balls : {YELLOW}Number of balls to spawn (default: {ball_count}")
                print(f"\t{PURPLE}-p, --path : {YELLOW}Show the path of the balls")
                print(f"\t{PURPLE}-t, --hearts : {YELLOW}Use little hearts instead of blocks to draw the balls")

                print(bar)
                print(f"Controls:")
                print(f"\t{PURPLE}Esc : {YELLOW}Quit the game")
                print(f"\t{PURPLE}Space : {YELLOW}Make the selected ball go crazy")
                print(f"\t{PURPLE}Up Arrow : {YELLOW}Make the selected ball go up")
                print(f"\t{PURPLE}Down Arrow : {YELLOW}Make the selected ball go down")
                print(f"\t{PURPLE}Left Arrow : {YELLOW}Make the selected ball go left")
                print(f"\t{PURPLE}Right Arrow : {YELLOW}Make the selected ball go right")
                print(f"\t{PURPLE}[F] : {YELLOW}Make ALL the balls go crazy")
                print(f"\t{PURPLE}[R] : {YELLOW}Reset the selected ball")
                print(f"\t{PURPLE}[N] : {YELLOW}Spawn a new ball")
                print(f"\t{PURPLE}[C] : {YELLOW}Change the selected ball")
                print(f"\t{PURPLE}[G] : {YELLOW}Disable/Enable gravity (overwriten if -g option is 0)")
                print(f"\t{PURPLE}[D] : {YELLOW}Delete the selected ball")
                print(f"\t{PURPLE}[E] : {YELLOW}Erase the paths")
                print(f"\t{PURPLE}[P] : {YELLOW}Show/Hide the paths")
                print(f"\t{PURPLE}[H] : {YELLOW}Use blocks/hearts to draw the balls")
                print(f"\t{PURPLE}[S] : {YELLOW}Stop the selected ball at its current position by setting its speed to 0")
                
                print(bar)
                print(f"Additional information:")
                print(f"\t{PURPLE}You can set the gravity to 0!{RESET}")
                print(f"\t{PURPLE}If you want to keep your cursor and stdin visible after the game, exit with ESC instead of Ctrl+C (also, see -c option){RESET}")
                print(f"\t{PURPLE}If you encounter any bugs, please report them on the Github repository or at koprivnik@skwal.net{RESET}")
                print()
                
                quit(0)

            case "-v" | "--version":
                # If -v is used, print the version number and exit
                print(f"{BG_PURPLE} Bouncing Balls {RESET}")
                print(f"Version: {PURPLE}{VERSION}{RESET}")
                quit(0)
            case "-c" | "--cursor":
                # If -c is used, show the cursor and exit
                show_stdin()
                quit(0)
                
            case "-s" | "--speed":
                # If -s is used, set the speed of the balls
                if len(argv) == 0:
                    # If there is no argument, print an error message and exit
                    print(f"{RED}Error: {YELLOW}Missing argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                arg = argv.pop(0)
                try:
                    # Try to convert the argument to an integer
                    speed = int(arg)
                except ValueError:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                # Make sure the speed is in the correct range
                if speed < 1 or speed > 10:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}speed value (-s){RESET}")
                    quit(1)

            case "-g" | "--gravity":
                # If -g is used, set the gravity of the balls
                if len(argv) == 0:
                    # If there is no argument, print an error message and exit
                    print(f"{RED}Error: {YELLOW}Missing argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                arg = argv.pop(0)
                try:
                    # Try to convert the argument to an integer
                    gravity = int(arg)
                except ValueError:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                # Make sure the gravity is in the correct range
                if gravity < 0 or gravity > 100:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}gravity value (-g){RESET}")
                    quit(1)
            case "-i" | "--increase":
                # If -i is used, set increase to True
                increase = True
            case "-a" | "--auto":
                # If -a is used, set auto to True
                auto = True
            case "-n" | "--no-air-frictions":
                # If -n is used, set air_frictions to False
                air_frictions = False
            case "-r" | "--restitution":
                # If -r is used, set the force restitution of the edges of the terminal
                if len(argv) == 0:
                    # If there is no argument, print an error message and exit
                    print(f"{RED}Error: {YELLOW}Missing argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                arg = argv.pop(0)
                try:
                    # Try to convert the argument to an integer
                    restitution = int(arg) / 10
                except ValueError:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                # Make sure the restitution is in the correct range
                if restitution < 0 or restitution > 1:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}restitution value (-r){RESET}")
                    quit(1)
            case "-b" | "--balls":
                # If -b is used, set the number of balls to spawn
                if len(argv) == 0:
                    # If there is no argument, print an error message and exit
                    print(f"{RED}Error: {YELLOW}Missing argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                arg = argv.pop(0)
                try:
                    # Try to convert the argument to an integer
                    ball_count = int(arg)
                except ValueError:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}{arg}{RESET}")
                    quit(1)
                # There must be at least 1 ball
                if ball_count < 1:
                    print(f"{RED}Error: {YELLOW}Invalid argument for {PURPLE}ball count (-b){RESET}")
                    quit(1)

            case "-p" | "--path":
                # If -p is used, set show_paths to True
                show_paths = True

            case "-t" | "--hearts":
                # If -h is used, set hearts to True
                hearts = True
                
            case _:
                # If the argument is unknown, print an error message and exit
                print(f"{RED}Error: {YELLOW}Unknown argument : {PURPLE}{arg}{RESET}")
                quit(1)

    hide_stdin()


    stop = False
    gravity_disabled = False

    # Create a new ball object
    def new_ball():
        return Ball(0 if gravity_disabled else gravity, restitution, air_frictions, show_paths, hearts)
    
    # Index of the selected ball
    selected_ball = 0

    # List of all the balls
    balls = []

    # Create the balls
    for i in range(ball_count):
        balls.append(new_ball())
        
    # Tell the selected ball that it is selected
    balls[selected_ball].select()

    # Set the initial speed of the balls to make them move and make all of them visible
    for ball in balls:
        ball.dx = randint(-3000, 3000) / 1000
        # If gravity is disabled, make the balls go up or down we dont care
        # But if gravity is enabled, make the balls go up so the user can see the effect of gravity
        # *Satisfying*
        ball.dy = randint(-3000, 3000 if balls[0].gravity == 0 else -1000) / 1000
    
    

    # Select the next ball in the list
    def change_selected():
        nonlocal selected_ball
        nonlocal balls
        # Tell the previous ball that it is not selected anymore
        balls[selected_ball].unselect()
        selected_ball = (selected_ball + 1) % len(balls)
        # Tell the new ball that it is now selected
        balls[selected_ball].select()

    def on_press(key):
        nonlocal stop
        nonlocal balls
        nonlocal show_paths
        nonlocal selected_ball
        nonlocal hearts
        nonlocal gravity_disabled
        if key == pynput.keyboard.Key.space:
            # When space is pressed, make the selected ball "go crazy"
            balls[selected_ball].wtf()
        elif key == pynput.keyboard.Key.esc:
            # When ESC is pressed, stop the game
            stop = True
        elif key == pynput.keyboard.Key.up:
            # When up arrow is pressed, make the selected ball go up 
            # or increase its up velocity if -i is used
            if increase:
                balls[selected_ball].dy += -1.5
            else:
                balls[selected_ball].dy = -1
        elif key == pynput.keyboard.Key.down:
            # When down arrow is pressed, make the selected ball go down 
            # or increase its down velocity if -i is used
            if increase:
                balls[selected_ball].dy += 1
            else:
                balls[selected_ball].dy = 1
        elif key == pynput.keyboard.Key.left:
            # When left arrow is pressed, make the selected ball go left
            # or increase its left velocity if -i is used
            if increase:
                balls[selected_ball].dx += -1
            else:
                balls[selected_ball].dx = -1
        elif key == pynput.keyboard.Key.right:
            # When right arrow is pressed, make the selected ball go right
            # or increase its right velocity if -i is used
            if increase:
                balls[selected_ball].dx += 1
            else:
                balls[selected_ball].dx = 1
        elif key == pynput.keyboard.KeyCode.from_char("r"):
            # When r is pressed, hide the selected ball and replace it with a blank one
            balls[selected_ball].draw_1()
            balls[selected_ball] = new_ball()
            balls[selected_ball].select()
        elif key == pynput.keyboard.KeyCode.from_char("n"):
            # When n is pressed, append a new ball to the list
            balls.append(new_ball())
            ball = balls[-1]
            # Also set the initial speed of the ball to make it move and make it visible
            ball.dx = randint(-3000, 3000) / 1000
            ball.dy = randint(-3000, 3000 if balls[0].gravity == 0 else -1000) / 1000
        elif key == pynput.keyboard.KeyCode.from_char("c"):
            # When c is pressed, select the next ball in the list
            change_selected()
        elif key == pynput.keyboard.KeyCode.from_char("f"):
            # When f is pressed, make all the balls "go crazy"
            for ball in balls:
                ball.wtf()
        elif key == pynput.keyboard.KeyCode.from_char("g"):
            # When g is pressed, disable/enable gravity
            # And also tell all the balls to disable/enable gravity
            gravity_disabled = not gravity_disabled
            for ball in balls:
                ball.set_gravity(0 if gravity_disabled else gravity)
        elif key == pynput.keyboard.KeyCode.from_char("d"):
            # When d is pressed, delete the selected ball
            # But only if there is more than 1 ball

            if len(balls) > 1:
                # Hide the ball before deleting it
                balls[selected_ball].draw_1()
                balls.pop(selected_ball)
            
                # Select the first ball
                selected_ball = 0
                balls[selected_ball].select()

        elif key == pynput.keyboard.KeyCode.from_char("e"):
            # When e is pressed, erase the paths
            # It clears the terminal but the balls will instantly redraw themselves in the next frame
            clear_terminal()

        elif key == pynput.keyboard.KeyCode.from_char("p"):
            # When p is pressed, show/hide the paths
            # Also tell all the balls to show/hide their paths
            show_paths = not show_paths
            for ball in balls:
                ball.show_path = show_paths
            clear_terminal()
        
        elif key == pynput.keyboard.KeyCode.from_char("h"):
            # When h is pressed, use blocks/hearts to draw the balls
            # Also tell all the balls to use blocks/hearts to draw themselves
            hearts = not hearts
            for ball in balls:
                ball.use_heart = hearts
        
        elif key == pynput.keyboard.KeyCode.from_char("s"):
            # When s is pressed, stop the selected ball at its current position
            balls[selected_ball].dx = 0
            balls[selected_ball].dy = 0
                

    i = 0
    clear_terminal()
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        while not stop:

            for ball in balls:
                if auto and (i + 1) % 2000 == 0:
                    ball.wtf()
                ball.update()    

            # Hide all the previous positions of the balls
            for ball in balls:
                ball.draw_1()

            # Draw all the balls
            for ball in balls:
                ball.draw_2()

            # Redraw the selected ball so it is on top of the others
            balls[selected_ball].draw_2()

            # Flush the stdout buffer so the terminal is updated
            stdout.flush()

            i += 1
            sleep(0.005 * (11 - speed))


        end()

if __name__ == "__main__":
    main()