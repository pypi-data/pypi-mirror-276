# AirBag CLI Menu
CLI menu module for python3 by AirBag65

## Getting started
To use the module you should be working within a virtual environment, or ```venv``` for short. If you don't already have one set up you can run one of these commands:

Windows: 
```Bash
python -m venv <name-of-venv>
```
MacOS / Linux: 
```Bash
python3 -m venv <name-of-venv>
```

When your ```venv``` is ready, you enter it with the following command:

Windows:
```bat
<name-of-venv>\Scripts\activate
```
MacOS / Linux: 
```Bash
source <name-of-venv>/bin/activate
```

When you have activated the virtual environment and running from within it, you can install ```airbagclimenu```, with one of the following commands: 

Windows:
```bat
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps airbagclimenu
```
MacOS / Linux: 
```Bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps airbagclimenu
```

## Usage
Make sure to use this exact ```import``` statement for the following to work:
```Python
from airbagclimenu import Menu
```
To create and run the menu, you do as follows:
```Python
menu = Menu.CLIMenu()
menu.run()
```
To add alternatives in the menu you have two options. You can add a function that will execute when that option is chosen, or you can add a submenu, which reveals more options when chosen. 
### add_menu_option(menu_option: MenuOption)
This method takes one parameter which should be of type ```MenuOption```. See example usecase below:
```Python
menu = Menu.CLIMenu()
# You can add a submenu directly by creating it as a parameter like this
menu.add_menu_option(Menu.MenuOption("Submenu 1"))
# Or you can create it as a variable and use the variable as the parameter
option2 = Menu.MenuOption("Submenu 2")
menu.add_menu_opntion(option2)
```
The second option is recommended in order to be able to add even more submenus and functions to the submenu.

### add_func(functionality, title: str)
This method takes two parameters. The first paramter is a function object, and the second is the title that will be displayed in the menu. See usecase below:
```Python
menu = Menu.CLIMenu()
def greet():
    print("Hello There!")

menu.add_func(greet, "Say Hello")
```
The function that is used **must** be parameterless, since there is no way of giving parameters as of now.


## Example Program
```Python
from airbagclimenu import Menu
import random

menu = Menu.CLIMenu()

def roll_die():
    val = random.randint(1,6)
    print(f"You rolled a {val}")

def greet1():
    print("Hello There!")

def greet_all():
    print("Hello, World!")

menu_op = Menu.MenuOption("Greetings")
menu_op.add_func(greet1, "Greet person")
menu_op.add_func(greet_all, "Greet everyone")

menu.add_menu_option(menu_op)
menu.add_func(roll_die, "Roll A Die")
menu.run()
```
The output of this program will be the following:
```
[1] Greetings
[2] Roll A Die
: 1
```
The 1st option was chosen here so the program enters this state:
```
[1] Greet person
[2] Greet everyone
: 1
Hello There!
```

### If you like my work
Feel free to send a small donation via the [GitHub page](https://github.com/Airbag65/CLI-Menu) if you like my work! But by all means, DO NOT feel preasured to do so!!
![paypal qr code](https://github.com/Airbag65/CLI-Menu/blob/main/qrcode.png)
