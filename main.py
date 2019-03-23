from kivy.app import App
from kivy.uix.widget import Widget


class GnGGui(Widget):
    pass


class GnGApp(App):
    def build(self):
        return GnGGui()


if __name__ == '__main__':
    GnGApp().run()
