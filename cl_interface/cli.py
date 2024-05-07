from cl_interface.page import Page


class CLI:
    input_message = "-->"

    def __init__(self, **kwargs):
        self.is_on = True
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.current_page = list(kwargs.items())[0][1]

    def render_page(self):

        self.current_page.call() if not self.current_page.called else None
        self.current_page.called = False
        user_input = input(self.input_message)

        # Handle command
        if user_input and user_input[0] == self.current_page.command_marker:
            user_input = user_input.replace(self.current_page.command_marker, "")
            if user_input in self.current_page.body.keys():
                perform = self.current_page.body[user_input][1]()
                self.current_page = perform if \
                    type(perform) is Page else self.current_page
            else:
                self.current_page.errors.append("Wrong command")

        # Handle text
        elif self.current_page.text_is_allowed:
            self.current_page.text_output = self.current_page.text_handler(user_input)

        else:
            self.current_page.errors.append("Text is not allowed on this page.")

    def mainloop(self):
        """ Main loop. """
        while self.is_on:
            self.render_page()

    def off(self):
        """ Finish CLI. """
        self.is_on = False
