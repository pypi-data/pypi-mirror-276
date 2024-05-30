import os
import types


class IllegalArgumentError(ValueError):
    pass

class MenuOption:
    pass

class MenuOption:
    def __init__(self, title: str):
        self.title = title
        self.menu_options = {}

    def add_menu_option(self, menu_option: MenuOption) -> None:
        if not isinstance(menu_option, MenuOption):
            raise IllegalArgumentError("Argument must be of type 'CLIMenu'")
        self.menu_options[len(self.menu_options) + 1] = menu_option

    def add_func(self, functionality, title: str):
        if not isinstance(functionality, types.FunctionType):
            raise IllegalArgumentError("Argument must be of type 'Function'")
        self.menu_options[len(self.menu_options) + 1] = [title, functionality]

    def run(self, clear_screen = True):
        if clear_screen:
            os.system("cls" if os.name == "nt" else "clear")
        for key, val in self.menu_options.items():
            if isinstance(val, MenuOption):
                print(f"[{key}] {val.title}")
            else:
                print(f"[{key}] {val[0]}")
        choice = int(input(": "))
        if choice not in self.menu_options.keys():
            print("Not a valid option")
            return
        chosen_option = self.menu_options[choice]
        if isinstance(chosen_option, MenuOption):
            chosen_option.run(clear_screen)
        else:
            chosen_option[1]()


class CLIMenu:
    def __init__(self, quit_stmt = True):
        self.quit_stmt = quit_stmt
        self.menu_options = {}

    def add_menu_option(self, menu_option: MenuOption) -> None:
        if not isinstance(menu_option, MenuOption):
            raise IllegalArgumentError("Argument must be of type 'CLIMenu'")
        self.menu_options[len(self.menu_options) + 1] = menu_option

    def add_func(self, functionality, title: str):
        if not isinstance(functionality, types.FunctionType):
            raise IllegalArgumentError("Argument must be of type 'Function'")
        self.menu_options[len(self.menu_options) + 1] = [title, functionality]

    def run(self, clear_screen = True) -> None:
        if self.quit_stmt:
            self.menu_options[len(self.menu_options) + 1] = ("Quit", "")
            _quit = self.quit_stmt
            while _quit:
                if clear_screen:
                    os.system("cls" if os.name == "nt" else "clear")
                for key, val in self.menu_options.items():
                    if isinstance(val, MenuOption):
                        print(f"[{key}] {val.title}")
                    else:
                        print(f"[{key}] {val[0]}")
                choice = int(input(": "))
                if choice not in self.menu_options.keys():
                    print("Not a valid option")
                    _quit = False
                chosen_option = self.menu_options[choice]
                if isinstance(chosen_option, MenuOption):
                    chosen_option.run(clear_screen)
                elif isinstance(chosen_option, tuple):
                    print("Quitting")
                    _quit = False
                else:
                    chosen_option[1]()
        else:
            if clear_screen:
                os.system("cls" if os.name == "nt" else "clear")
            for key, val in self.menu_options.items():
                if isinstance(val, MenuOption):
                    print(f"[{key}] {val.title}")
                else:
                    print(f"[{key}] {val[0]}")
            choice = int(input(": "))
            if choice not in self.menu_options.keys():
                print("Not a valid option")
                return
            chosen_option = self.menu_options[choice]
            if isinstance(chosen_option, MenuOption):
                chosen_option.run(clear_screen)
            elif isinstance(chosen_option, tuple):
                print("Quitting")
                return
            else:
                chosen_option[1]()




