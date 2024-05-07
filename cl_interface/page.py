import subprocess
import os
import colorama
colorama.init()


def merge_dictionaries(dict1: dict, dict2: dict):
    """ Merge two dictionaries depending on their fullness. """
    if dict1 and dict2:  # Merge dictionaries
        return {**dict1, **dict2}
    elif dict1 and not dict2:
        return dict1
    else:
        return dict2


def clear_console():  # Clears console output depending on OS
    subprocess.call("clear" if os.name == "posix" else "cls", shell=True)


class Page:
    """ The class represents a one page of a Command Line Interface. It consists of title and body with named list of
     actions."""
    command_marker = "#"
    error_marker = "\033[31m[ERROR]\033[0m"
    text_output_marker = "\033[32mResult:\033[0m"

    def __init__(self, text_is_allowed=False, numeric_commands=True, title="", text_handler=None,
                 actions: dict = None, **kwargs: tuple):
        """ Definition of the Page is possible with several ways. All parameters are optional.

        For title
            title - str, Information, placed on top of the page.
        For body | Can be passed simultaneously
             actions - dict, For a single command use following format:
                       {command (str): (command_title (str), method (function))};

             **kwargs - tuple, For a single command use following format:
                        command=(command_title (str), method (function)).

        text_is_allowed - bool, Allow text input on the page.
        numeric_commands - bool, Despite passed names of commands all actions will be numerated and numbers will be set
        as command names.

        text_handler - function, Method to handle text user input.

        * Inappropriate arguments may cause an errors."""

        # Other parameters
        self.numeric_commands = numeric_commands
        self.called = False
        self.errors = []
        self.text_is_allowed = text_is_allowed

        # Text handler
        self.text_handler = text_handler if callable(text_handler) or not text_handler\
            else self.errors.append("Text handler must be callable")

        # Title, Body and Output Window
        self.title = f"\033[34m{title}\033[0m\nStart command with {self.command_marker}\n"
        self.body = {}
        self.text_output = ""

        arg_dict = merge_dictionaries(actions, kwargs)

        self.add_commands(actions=arg_dict)

    def call(self):
        clear_console()

        # Print out the page
        print(self.title)
        print(f"{self.text_output_marker} {self.text_output}\n") if self.text_output else None
        for command, value in self.body.items():
            print(f"{command}: {value[0]}")
        print()
        self.print_errors()
        self.errors = []

        self.called = True
        return self

    def add_commands(self, actions: dict = None, **kwargs: tuple):
        """ Creates body of the page. Can be used separately from an instantiation if actions or **kwargs weren't
         passed."""

        body = merge_dictionaries(actions, kwargs)

        # Error check. Stops self.body forming if error was occurred.
        for key, value in body.items():
            if not isinstance(key, str):  # Check if keys are strings
                self.errors.append("Keys must be strings")
                break
            if not isinstance(value, tuple):  # Check for tuple data type of body values
                self.errors.append("Values for keys must be tuples")
                break
            elif len(value) != 2:  # Check for length of 2 of each tuple
                self.errors.append("Values must be tuple with length of 2, where 1st element is name of an \n"
                                   f"{(len(self.error_marker) + 1)*" "}action (str) and 2nd is action itself (function)"
                                   )
                break
            elif not isinstance(value[0], str):  # First value of the tuple must be a string
                self.errors.append("Name of the action must be a string")
                break
            elif not callable(value[1]):  # Second value of the tuple must be a function
                self.errors.append("Action method must be callable")
                break

            self.body[key] = value  # Assign right formed value to a command
        self.numerate_commands() if self.numeric_commands else None

    def numerate_commands(self):
        """ Rewrite command names with numbers. """
        to_return = self.body.copy()
        i = 1
        for command in self.body:
            to_return[str(i)] = to_return.pop(command)
            i += 1
        self.body = to_return

    def print_errors(self):
        """ Prints out all errors that are on this page."""
        for error in self.errors:
            print(f"{self.error_marker if self.errors else ''} {error}")

    def update_output(self, new_output: str):
        self.text_output = new_output
