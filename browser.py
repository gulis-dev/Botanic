from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QProgressBar, QHBoxLayout, QToolButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon

import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/opt/homebrew/Cellar/qt/6.7.3/share/qt/plugins/platforms"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Botanic Web Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Centralny widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout główny
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Pasek narzędzi i pasek adresu
        self.address_layout = QHBoxLayout()
        self.layout.addLayout(self.address_layout)

        # Pasek narzędzi z przyciskami
        self.toolbar_layout = QHBoxLayout()
        self.address_layout.addLayout(self.toolbar_layout)

        # Styl przycisków
        button_style = """
            QToolButton {
                 /* Pomarańczowy kolor */
                color: white;
                border-radius: 17px;
                padding: 8px;
                border: none;
                margin: 5px;
            }
            QToolButton:hover {
                background-color: #524025;
            }
            QToolButton:pressed {
                background-color: #8c5400;  /* Ciemniejszy pomarańczowy */
            }
        """

        # Przycisk Wstecz
        self.back_button = QToolButton(self)
        self.back_button.setIcon(QIcon("assets/icons/back_icon.svg"))
        self.back_button.setStyleSheet(button_style)
        self.back_button.clicked.connect(self.go_back)
        self.toolbar_layout.addWidget(self.back_button)

        # Przycisk Do przodu
        self.forward_button = QToolButton(self)
        self.forward_button.setIcon(QIcon("assets/icons/forward_icon.svg"))
        self.forward_button.setStyleSheet(button_style)
        self.forward_button.clicked.connect(self.go_forward)
        self.toolbar_layout.addWidget(self.forward_button)

        # Przycisk Odśwież
        self.reload_button = QToolButton(self)
        self.reload_button.setIcon(QIcon("assets/icons/reload_icon.svg"))
        self.reload_button.setStyleSheet(button_style)
        self.reload_button.clicked.connect(self.reload_page)
        self.toolbar_layout.addWidget(self.reload_button)

        # Przycisk Idź
        self.home_button = QToolButton(self)
        self.home_button.setIcon(QIcon("assets/icons/home_icon.svg"))
        self.home_button.setStyleSheet(button_style)
        self.home_button.clicked.connect(self.navigate_home)
        self.toolbar_layout.addWidget(self.home_button)

        # Pasek adresu
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Wpisz adres URL...")
        self.address_bar.setStyleSheet("""
            QLineEdit {
                border-radius: 14px;
                padding: 5px;
                margin: 10px;
                padding-left: 30px
            }
        """)
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        self.address_layout.addWidget(self.address_bar)

        # Pasek postępu
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        # Przeglądarka
        self.browser = QWebEngineView(self)
        self.browser.loadStarted.connect(self.on_load_started)
        self.browser.loadFinished.connect(self.on_load_finished)
        self.browser.urlChanged.connect(self.update_address_bar)
        self.layout.addWidget(self.browser)

        # Domyślna strona
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def reload_page(self):
        self.browser.reload()

    def on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

    def on_load_finished(self, ok):
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)

    def update_address_bar(self, url):
        self.address_bar.setText(url.toString())

    def go_back(self):
        if self.browser.history().canGoBack():
            self.browser.back()

    def go_forward(self):
        if self.browser.history().canGoForward():
            self.browser.forward()
