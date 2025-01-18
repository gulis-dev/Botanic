import sys
from PyQt6.QtWidgets import QApplication
import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/opt/homebrew/Cellar/qt/6.7.3/share/qt/plugins/platforms"


from browser import Browser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
