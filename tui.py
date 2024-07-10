import urwid

class LaunchTUI:
    def __init__(self):
        self.main_menu_items = [
            ('Install Dependencies', self.placeholder),
            ('Install Software', self.placeholder),
            ('Optimizer', self.placeholder),
            ('Run Playbooks', self.placeholder),
            ('Utilities', self.placeholder),
            ('Fresh Setup (Unattended)', self.placeholder),
            ('Magic Menu', self.placeholder),
            ('Exit', self.exit_program)
        ]
        self.logo = self.create_logo()
        self.main_menu = self.create_menu(self.main_menu_items)
        self.footer_text = urwid.Text("Press (Q) to exit, (M) for main menu")

        # Create a Frame with the logo as header, menu as body, and footer
        self.frame = urwid.Frame(
            header=self.logo,
            body=urwid.Padding(self.main_menu, left=2, right=2),
            footer=self.footer_text
        )

    def create_logo(self):
        logo_text = [
            "██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗",
            "██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║",
            "██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║",
            "██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║",
            "███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║",
            "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝"
        ]

        gradient = [
            ('logo_color1', 'dark blue'),
            ('logo_color2', 'light blue'),
            ('logo_color3', 'light magenta'),
            ('logo_color4', 'dark magenta'),
        ]

        logo_widget_list = []
        for i, line in enumerate(logo_text):
            color = gradient[min(i, len(gradient) - 1)][0]
            logo_widget_list.append(urwid.AttrMap(urwid.Text(line, align='center'), color))

        return urwid.Pile(logo_widget_list)

    def create_menu(self, choices):
        body = [urwid.Divider()]
        for choice, callback in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', callback)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def placeholder(self, button):
        self.show_text(f"You selected: {button.label}\nThis feature is not implemented yet.")

    def show_text(self, text):
        text_widget = urwid.Text(text)
        done = urwid.Button(u'Back to Main Menu')
        urwid.connect_signal(done, 'click', self.show_main_menu)
        response_pile = urwid.Pile([text_widget, urwid.Divider(), urwid.AttrMap(done, None, focus_map='reversed')])
        self.frame.body = urwid.Filler(urwid.Padding(response_pile, left=2, right=2))

    def show_main_menu(self, button=None):
        self.frame.body = urwid.Padding(self.main_menu, left=2, right=2)

    def exit_program(self, button=None):
        raise urwid.ExitMainLoop()

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            self.exit_program()
        elif key in ('m', 'M'):
            self.show_main_menu()
        else:
            return False
        return True

    def run(self):
        palette = [
            ('bg', 'black', 'black'),
            ('reversed', 'standout', ''),
            ('logo_color1', 'dark blue', 'black'),
            ('logo_color2', 'light blue', 'black'),
            ('logo_color3', 'light magenta', 'black'),
            ('logo_color4', 'dark magenta', 'black'),
        ]
        loop = urwid.MainLoop(self.frame, palette=palette, unhandled_input=self.unhandled_input)
        loop.run()

if __name__ == "__main__":
    LaunchTUI().run()
