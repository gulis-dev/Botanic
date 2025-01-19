import json
from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QProgressBar, QHBoxLayout, \
    QToolButton, QTabWidget, QMenu, QLabel, QTableWidgetItem, QScrollArea, QTableWidget, \
    QHeaderView
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon

import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/opt/homebrew/Cellar/qt/6.7.3/share/qt/plugins/platforms"


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia okna głównego
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

        # Przycisk Menu
        self.menu_button = QToolButton(self)
        self.menu_button.setIcon(QIcon("assets/icons/menu_icon.svg"))
        self.menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu_button.setArrowType(Qt.ArrowType.NoArrow)
        self.menu_button.setStyleSheet("""
            QToolButton {
                color: white;
                border-radius: 17px;
                padding: 8px;
                border: none;
                margin: 5px;
            }
            QToolButton::menu-indicator { 
                image: none;  /* Usuwa wskaźnik strzałki */
                width: 0px;   /* Ustawia szerokość wskaźnika na 0 */
            }
            QToolButton:hover {
                background-color: #524025;
            }
            QToolButton:pressed {
                background-color: #8c5400; 
            }
        """)

        # Menu Rozwijane
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2c2c2c;
                border: 1px solid #444;
                padding: 5px;
                border-radius: 5px;
            }
            QMenu::item {
                color: white;
                padding: 7px 35px;  /* Odstępy wewnętrzne */
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: #524025;  /* Kolor podświetlenia */
            }
        """)


        # Opcja 1: Nowa karta
        history_action = menu.addAction("New card")
        history_action.triggered.connect(lambda: self.add_new_tab("https://www.google.com"))

        # Opcja 2: Historia
        history_action = menu.addAction("History")
        history_action.triggered.connect(self.show_history_on_new_tab)

        # Opcja 3: Cookies
        cookies_action = menu.addAction("Cookies")
        cookies_action.triggered.connect(self.show_cookies)

        # Dodanie menu do przycisku
        self.menu_button.setMenu(menu)

        self.address_layout.addWidget(self.menu_button)

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

        # Lista na ciasteczka
        self.cookies = []

        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)

        if browser:
            cookie_store = browser.page().profile().cookieStore()
            cookie_store.cookieAdded.connect(self.on_cookie_added)

        self.load_cookies()



    """
    ****************************************************************
    PASEK NARZĘDZI
    ****************************************************************
    """

    def navigate_to_url(self):
        """
        Metoda, która przechodzi na adres URL wpisany w pasek adresu. Jeśli adres nie zaczyna się od 'http://' lub 'https://',
        automatycznie dodaje 'https://'. Używa QWebEngineView, aby ustawić URL w bieżącej karcie przeglądarki.
        """
        url = self.address_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        browser = self.tab_widget.currentWidget()
        if browser:
            browser.setUrl(QUrl(url))

    def navigate_home(self):
        """
        Metoda, która ustawia adres URL na stronę główną (Google) w aktywnej karcie. Używa QWebEngineView do ustawienia URL.
        """
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser:
            browser.setUrl(QUrl("https://www.google.com"))

    def reload_page(self):
        """
        Metoda, która odświeża aktualną stronę w przeglądarce. Ponownie ładuje stronę w QWebEngineView w bieżącej karcie.
        """
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser:
            browser.reload()

    def on_load_started(self):
        """
        Metoda wywoływana na początku ładowania strony, ustawia pasek postępu na 0 i sprawia, że pasek postępu jest widoczny.
        """
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)


    def update_address_bar(self, url):
        """
        Metoda, która aktualizuje tekst w pasku adresu, ustawiając URL bieżącej strony. Używa obiektu QUrl do uzyskania tekstu URL.
        """
        self.address_bar.setText(url.toString())

    def go_back(self):
        """
        Metoda, która umożliwia przejście do poprzedniej strony w historii. Sprawdza, czy historia przeglądarki może cofnąć się.
        """
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser and browser.history().canGoBack():
            browser.back()

    def go_forward(self):
        """
        Metoda, która umożliwia przejście do następnej strony w historii. Sprawdza, czy historia przeglądarki może przejść do przodu.
        """
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)
        if browser and browser.history().canGoForward():
            browser.forward()

    def on_url_changed(self, url):
        """
        Metoda, która zapisuje historię przeglądania do pliku JSON. Pobiera historię z QWebEngineView i zapisuje URL oraz znacznik czasu.
        """
        self.save_history()
        self.address_bar.setText(url.toString())

    def update_tab_info(self, browser):
        """
        Metoda, która aktualizuje tytuł karty, skracając go, jeśli jest zbyt długi.
        Używa metody `setTabText` na odpowiedniej karcie, aby wyświetlić skrócony tytuł.
        """
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
        """
        Metoda, która dodaje nową kartę do przeglądarki. Inicjuje instancję QWebEngineView z domyślnym URL-em, ustawia
        połączenia do zmiany URL-a i załadowania strony oraz zarządza ciasteczkami.
        """
        if isinstance(url, str):
            browser = QWebEngineView()
            browser.setUrl(QUrl(url))

            browser.urlChanged.connect(self.on_url_changed)

            browser.loadFinished.connect(lambda ok, browser=browser: self.update_tab_info(browser))

            cookie_store = browser.page().profile().cookieStore()
            cookie_store.cookieAdded.connect(self.on_cookie_added)

            container = QWidget(self)
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 10, 0, 0)
            layout.addWidget(browser)

            index = self.tab_widget.addTab(container, "New card")
            self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        """
        Metoda, która zamyka kartę na podstawie jej indeksu, pod warunkiem, że nie jest to jedyna karta.
        """
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def switch_tab(self, index):
        """
        Metoda, która przełącza na kartę o podanym indeksie i aktualizuje pasek adresu, aby odzwierciedlał URL bieżącej strony.
        """
        container = self.tab_widget.widget(index)
        browser = container.findChild(QWebEngineView)
        if browser:
            self.update_address_bar(browser.url())

    """
    ****************************************************************
    HISTORIA
    ****************************************************************
    """


    def show_history_on_new_tab(self):
        """
        Metoda, która otwiera historię przeglądania na nowej karcie. Pokazuje tabelę z URL-ami i znacznikami czasowymi
        oraz umożliwia otwieranie wybranych stron z historii.
        """
        history_widget = QWidget(self)
        history_layout = QVBoxLayout(history_widget)

        table_widget = QTableWidget(self)
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(["URL", "Timestamp"])

        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table_widget.setSortingEnabled(True)
        table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


        table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QTableWidget::item {
                background-color: #333;
                border: 1px solid #444;
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #524025;
            }
            QHeaderView::section {
                background-color: #404040;
                color: white;
                border: 1px solid #444;
                padding: 5px;
            }
            QScrollArea {
                border: none;
            }
        """)

        try:
            with open('data/history.json', 'r') as file:
                data = json.load(file)
                history_list = data.get("history", [])

                if not history_list:
                    label = QLabel("Brak historii przeglądania.", self)
                    history_layout.addWidget(label)
                else:
                    history_list.reverse()

                    # Dodawanie danych do tabeli
                    table_widget.setRowCount(len(history_list))
                    for row, entry in enumerate(history_list):
                        url = entry["url"]
                        timestamp = entry["timestamp"]
                        if len(url) >= 50:
                            url = url[:50] + "..."
                        table_widget.setItem(row, 0, QTableWidgetItem(url))
                        table_widget.setItem(row, 1, QTableWidgetItem(timestamp))

                        table_widget.item(row, 0).setData(Qt.ItemDataRole.UserRole, url)
                        table_widget.item(row, 0).setFlags(
                            table_widget.item(row,0).flags() | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        except FileNotFoundError:
            print("Nie znaleziono pliku z historią.")
            label = QLabel("Nie znaleziono pliku z historią.", self)
            history_layout.addWidget(label)

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(table_widget)
        scroll_area.setWidgetResizable(True)

        history_layout.addWidget(scroll_area)

        index = self.tab_widget.addTab(history_widget, "History")
        self.tab_widget.setCurrentIndex(index)

        table_widget.itemClicked.connect(self.open_url_from_table)

    def open_url_from_table(self, item):
        """
        Metoda, która otwiera stronę w nowej karcie, bazując na wybranym URL-u z tabeli historii.
        """
        url = item.data(Qt.ItemDataRole.UserRole)
        if url:
            self.add_new_tab(url)

    def save_history(self):
        """
        Metoda, która zapisuje historię przeglądania do pliku JSON. Zapisuje URL i znacznik czasu każdej odwiedzonej strony.
        """
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)

        if browser:
            history = browser.history()
            new_history_item = None
            for i in range(history.count()):
                history_item = history.itemAt(i)
                url = history_item.url().toString()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_history_item = {"url": url, "timestamp": timestamp}

            history_list = []
            try:
                with open('data/history.json', 'r') as file:
                    data = json.load(file)
                    history_list = data.get("history", [])
            except FileNotFoundError:
                print("Nie znaleziono pliku z historią.")

            if new_history_item and new_history_item not in history_list:
                history_list.append(new_history_item)

            with open('data/history.json', 'w') as file:
                json.dump({"history": history_list}, file, indent=4)

    def open_url_from_history(self, url):
        """
        Metoda, która ustawia URL strony w bieżącej karcie na podstawie URL-a z historii.
        """
        container = self.tab_widget.currentWidget()
        browser = container.findChild(QWebEngineView)

        if browser:
            browser.setUrl(QUrl(url))

    """
    ****************************************************************
    PLIKI COOKIES
    ****************************************************************
    """


    def save_cookies(self):
        """
        Metoda, która zapisuje ciasteczka przeglądarki do pliku JSON. Tworzy folder 'data', jeśli nie istnieje.
        """
        if not os.path.exists('data'):
            os.makedirs('data')

        with open('data/cookies.json', 'w') as file:
            json.dump(self.cookies, file, indent=4)

        print("Ciasteczka zostały zapisane.")

    def load_cookies(self):
        """
        Metoda, która wczytuje ciasteczka z pliku JSON, jeśli plik istnieje i zawiera dane. W przypadku błędów
        wyświetla komunikat i ustawia listę ciasteczek na pustą.
        """
        try:
            if not os.path.exists('data/cookies.json') or os.path.getsize('data/cookies.json') == 0:
                print("Plik cookies.json nie istnieje lub jest pusty.")
                self.cookies = []
                return

            with open('data/cookies.json', 'r') as file:
                self.cookies = json.load(file)

            print(f"Załadowano {len(self.cookies)} ciasteczek.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Nie udało się wczytać ciasteczek: {e}")
            self.cookies = []

    def closeEvent(self, event):
        """
        Metoda, która zapisuje ciasteczka przy zamknięciu aplikacji.
        """
        self.save_cookies()
        super().closeEvent(event)

    def show_cookies(self):
        """
        Metoda, która wyświetla zapisane ciasteczka w tabeli na nowej karcie. Tabela zawiera kolumny z nazwą, wartością, domeną,
        ścieżką, informacjami o bezpieczeństwie i HTTPOnly ciasteczek.
        """
        container = QWidget(self)
        layout = QVBoxLayout(container)

        table = QTableWidget(self)
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Name", "Value", "Domain", "Path", "Secure", "HTTP Only"])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        if not self.cookies:
            layout.addWidget(QLabel("Brak zapisanych cookies."))
        else:
            table.setRowCount(len(self.cookies))

            for row, cookie in enumerate(self.cookies):
                table.setItem(row, 0, QTableWidgetItem(cookie["name"]))
                table.setItem(row, 1, QTableWidgetItem(cookie["value"]))
                table.setItem(row, 2, QTableWidgetItem(cookie["domain"]))
                table.setItem(row, 3, QTableWidgetItem(cookie["path"]))
                table.setItem(row, 4, QTableWidgetItem(str(cookie["secure"])))
                table.setItem(row, 5, QTableWidgetItem(str(cookie["httpOnly"])))

            layout.addWidget(table)

        index = self.tab_widget.addTab(container, "Cookies")
        self.tab_widget.setCurrentIndex(index)

    def on_cookie_added(self, cookie):
        """
        Metoda, która jest wywoływana po dodaniu ciasteczka, zbiera dane ciasteczka i dodaje je do listy przechowywanych ciasteczek.
        """
        try:
            self.cookies.append({
                "name": cookie.name().data().decode('utf-8', errors='ignore'),
                "value": cookie.value().data().decode('utf-8', errors='ignore'),
                "domain": cookie.domain(),
                "path": cookie.path(),
                "secure": cookie.isSecure(),
                "httpOnly": cookie.isHttpOnly(),
                "expiration": cookie.expirationDate().toString(Qt.DateFormat.ISODate)
            })
        except Exception as e:
            print(f"Błąd podczas dodawania ciasteczka: {e}")

