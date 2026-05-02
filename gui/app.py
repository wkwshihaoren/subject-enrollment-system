import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)


from gui.login_window import LoginWindow
class GUIUniApp:
    def run(self):
        app = LoginWindow()
        app.mainloop()


if __name__ == "__main__":
    GUIUniApp().run()
