from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QProgressBar, QHBoxLayout, \
    QToolButton, QTabWidget
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

        # Pasek narzędzi i pasek adresu (nad kartami)
        self.address_layout = QHBoxLayout()
        self.layout.addLayout(self.address_layout)

        # Pasek narzędzi z przyciskami
        self.toolbar_layout = QHBoxLayout()
        self.address_layout.addLayout(self.toolbar_layout)

        # Styl przycisków
        button_style = """
            QToolButton {
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
                background-color: #8c5400; 
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

        self.address_layout.addWidget(self.address_bar)

        # Widget z kartami
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.switch_tab)

        tab_style = """
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #404040;
                padding: 5px 15px;
                margin-right: 5px;
                border-radius: 10px;
            }
            QTabBar::tab:selected {
                background-color: #696969;
                border-color: #a1a1a1;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #525252;
            }
        """
        self.tab_widget.setStyleSheet(tab_style)

        # Dodanie widgetu kart poniżej paska narzędzi
        self.layout.addWidget(self.tab_widget)

        # Dodanie przycisku do dodawania nowych kart
        self.new_tab_button = QToolButton(self)
        self.new_tab_button.setIcon(QIcon("assets/icons/new_tab_icon.svg"))
        self.new_tab_button.setStyleSheet(button_style)
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab("https://www.google.com"))
        self.toolbar_layout.addWidget(self.new_tab_button)

        # Dodanie pierwszej karty
        self.add_new_tab()

        # Pasek postępu
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        browser = self.tab_widget.currentWidget()
        if browser:
            browser.setUrl(QUrl(url))

    def navigate_home(self):
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser:
            browser.setUrl(QUrl("https://www.google.com"))

    def reload_page(self):
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser:
            browser.reload()

    def on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

    def on_load_finished(self, ok):
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)

    def update_address_bar(self, url):
        self.address_bar.setText(url.toString())

    def go_back(self):
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser and browser.history().canGoBack():
            browser.back()

    def go_forward(self):
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser and browser.history().canGoForward():
            browser.forward()

    def on_url_changed(self, url):
        self.address_bar.setText(url.toString())

    def update_tab_info(self, browser):
        title = browser.page().title()
        max_title_length = 15
        final_title = title
        if len(title) >= max_title_length:
            final_title = ""
            for i in range(0, max_title_length):
                final_title += title[i]
            final_title += "..."
        index = self.tab_widget.indexOf(browser.parent())

        if index != -1:
            self.tab_widget.setTabText(index, final_title)

    def add_new_tab(self, url="https://www.google.com"):
        if isinstance(url, str):
            browser = QWebEngineView()
            browser.setUrl(QUrl(url))

            browser.urlChanged.connect(self.on_url_changed)

            browser.loadFinished.connect(lambda ok, browser=browser: self.update_tab_info(browser))

            container = QWidget(self)
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 10, 0, 0)
            layout.addWidget(browser)

            index = self.tab_widget.addTab(container, "New card")
            self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def switch_tab(self, index):
        container = self.tab_widget.widget(index)
        browser = container.findChild(QWebEngineView)
        if browser:
            self.update_address_bar(browser.url())

