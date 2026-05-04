from gui.login_window import LoginWindow


class GUIUniApp:
    def run(self):
        app = LoginWindow()
        app.mainloop()


if __name__ == "__main__":
    GUIUniApp().run()
