from pymouse import PyMouse
from pykeyboard import PyKeyboard
from serial import Serial
import sys

' ' # These are the button mappings, put the decodes signals inside the quotes for the button u want to use. eg: mouse_up ="20DF890C"
mouse_up = "" 
mouse_down =""
mouse_right = ""
mouse_left =""
mouse_right_click = ""
mouse_left_click = ""
alt_key = "" 
tap_key = ""
ctrl_key = ""
shift_key = ""
repeat_code = "" # This is the code that the remote sends if a button is pressed for long
enter_key = "" # add as much as u want

alt_press = False # This will be used when we want to create a combo key press
step = 10

def main():
    try: 
        uno = Serial('/dev/ttyACM0') # Connect to the first serial port
    except: 
        try:
            uno = Serial('/dev/ttyACM1') # Connect to the second serial port
        except:
            sys.exit()

    i = uno.inWaiting() # Check how many bytes are in the serial monitor
    uno.read(i) # read all the bytes in the serial monitor

    mouse = PyMouse() # Create the mouse  instance
    keyboard = PyKeyboard() # Create the keyboard instance

    sizeX, sizeY = mouse.screen_size() # get the screen size to know when the mouse have reach the ends of the screen
    
    xmouse , ymouse = mouse.position() # get the current mouse position
    data = uno.readline().strip('\r\n')  # Read data from the arduino but strip out the special characters
    lastButton = data

    while True:
        xmouse, ymouse = mouse.position() # Always get the current mouse position

        if data == mouse_right:
            if xmouse< sizeX: # If the x axis of the mouse is less that the screen size ad it
                xmouse += step
            else:
                xmouse = sizeX
                
        elif data == mouse_left:
            if xmouse > 0:
                xmouse -= step
            else:
                xmouse = 0

        elif data == mouse_up:
            if ymouse < sizeY:
                ymouse += step
            else:
                ymouse = sizeY

        elif data == mouse_down:
            if ymouse > 0:
                ymouse -= step
            else:
                ymouse = 0

        elif data == mouse_left_click:
            mouse.click(xmouse,ymouse,button=1,n=1)

        elif data == mouse_right_click:
            mouse.click(xmouse, ymouse, button=2,n=1)

        elif data == alt_key:
            keyboard.tap_key(keyboard.alt_key)

        elif data == tap_key:
            keyboard.tap_key(keyboard.tap_key)

        elif data == shift_key:
            keyboard.tap_key(keyboard.shift_key)

        elif data == enter_key:
            keyboard.tap_key(keyboard.numpad_keys['Enter'])

        else:
            pass

        mouse.move(xmouse, ymouse) # now move the mouse
        data = uno.readline().strip('\r\n') # read data again


if __name__ == '__main__':
    main()
