
from guizero import App, Text

# We need to import PiAnalog codes in order to have the data from the phototransistors converted into something understandable.
# These three scripts need to be in the same folder for the import to work.
from PiAnalog1 import *
from PiAnalog2 import *
import time, math
import multiprocessing

# Here is the place where we define all the variables, that will be called upon in other functions.
start = PiAnalog1()
end = PiAnalog2()
multiplier = 2000 # increase to make sensor more senstitive
compare = 0
last_light1 = 0

# x is a variable that will later be the trigger to start and stop the timer.
# if its divisible by 2, with no remainder, the timer will start. 
# if x isnt divisible by 2, the timer will stop
x  = 0
clock = 0


# This part of the code runs the pianalog script its linked to. 
# So gets the light value given by the phototransitor that measures when the car passes on the start line.
def light1_from_r():
    global last_light1
    light1 = 1/math.sqrt(start.read_resistance()) * multiplier
    if light1 > 100:
        light1 = 100
    # This checks if the light value changed from the regular light value. 
    # If it changes the x value by 1, making it positive and the timer to start.
    if last_light1 != light1:
        x += 1
    else:
        last_light1 = light1
    print(light1)


# This function works the same way as the previouse one, using the phototransistor that is located at the finish line
def light2_from_r():
    light2 = 1/math.sqrt(end.read_resistance()) * multiplier
    if light2 > 100:
        light2 = 100
    # If the light changes from the original light, the x value will increase, making the value odd, and stopping the timer
    if last_light2 != light2:
        x += 1
    else:
        last_light2 = light2
    print(light2)


# this function gets the x values from other functions and then checks if its even or odd
# This function starts the timer when x is even and stops it, when x turns odd. 
# After the clock is done, we calculate and print the speed, using 1 meter as a distance between phototransistors
def timer():
    global light2
    global x
    global clock
    while x%2 == 0:
        clock += 1
        time.sleep(1)
        # change the 1 here for your distance between the start and finish line
        print(f"The speed of your vehicle is {1 / clock * 3.6 }km/hour")


# this is multiporcessing. It runs all the functions at the same time.
if __name__ == "__main__":
    p1 = multiprocessing.Process(target=light2_from_r)
    p1.start()

    p2 = multiprocessing.Process(target=light1_from_r)
    p2.start()

    p3 = multiprocessing.Process(target=timer)
    p3.start()


