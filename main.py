import os
import sys

if __name__ == '__main__':

    sys.path.append(os.path.join(os.path.dirname(__file__), 'osa'))
    from osa.gui import app

    sys.exit(app.run())
