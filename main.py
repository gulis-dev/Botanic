import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prosta Przeglądarka")
        self.setGeometry(100, 100, 1200, 800)

        # Centralny widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Pasek adresu
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Wpisz adres URL...")
        self.address_bar.returnPressed.connect(self.navigate_to_url)

        # Przyciski na pasku
        self.layout.addWidget(self.address_bar)

        # Przeglądarka
        self.browser = QWebEngineView(self)
        self.layout.addWidget(self.browser)

        # Pasek narzędzi
        self.toolbar_layout = QHBoxLayout()
        self.layout.addLayout(self.toolbar_layout)

        self.reload_button = QPushButton("Odśwież", self)
        self.reload_button.clicked.connect(self.reload_page)
        self.toolbar_layout.addWidget(self.reload_button)

        self.go_button = QPushButton("Przejdź", self)
        self.go_button.clicked.connect(self.navigate_to_url)
        self.toolbar_layout.addWidget(self.go_button)

        # Ustawiamy początkowy URL
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))

    def reload_page(self):
        self.browser.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
