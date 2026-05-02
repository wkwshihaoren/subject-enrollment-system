import os
import sys
from gui.login_window import LoginWindow


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)


class GUIUniApp:
    def run(self):
        app = LoginWindow()
        app.mainloop()


if __name__ == "__main__":
    GUIUniApp().run()
